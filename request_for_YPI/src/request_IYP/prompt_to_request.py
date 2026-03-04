# src/request_IYP/prompt_to_request.py
from typing import Dict, Any
from langfuse import observe

from src.request_IYP.generat_request import generate_cypher_for_request
from src.request_IYP.request_testing import execute_cypher_test
from src.request_IYP.analyse_results_request import analyse_research_result, analyze_and_correct_query
from src.request_IYP.probes_execution import execute_multiple_probes
from src.utils.logger import logger

def _perform_research_cycle(user_intent: str, analysis: Dict[str, Any], current_context: str, probe_count: int, logger_active: bool) -> Dict[str, Any]:
    """
    Gère une itération complète de la phase exploratoire (RESEARCH).
    Retourne un dictionnaire indiquant la prochaine action ('SUCCESS', 'NEW_QUERY', ou 'SKIP')
    ainsi que le contexte et l'historique mis à jour.
    """
    research_intent = analysis.get("corrected_query", "")
    
    # 1. Validation de l'intention
    if not research_intent or not research_intent.strip():
        if logger_active: logger.error("❌ [Research] Intent vide reçu de l'analyse")
        return {"status": "SKIP"}
    
    # 2. Gestion des requêtes trop vagues (Fallback)
    vague_patterns = ["investigate the required", "investigate required", "check the data", "find out more"]
    if any(pattern in research_intent.lower() for pattern in vague_patterns):
        if logger_active:
            logger.warning(f"⚠️ [Research] Intent trop vague détecté: '{research_intent[:100]}'")
            logger.info("🔄 [Research] Forçage d'une correction directe...")
            
        if analysis.get("message"):
            gen_result = generate_cypher_for_request(
                f"{user_intent} - Context: {analysis.get('message', '')}",
                additional_context=current_context
            )
            if gen_result.get("possible") and gen_result.get("queries"):
                queries = gen_result["queries"]
                return {"status": "NEW_QUERY", "query": queries[0] if isinstance(queries, list) else queries}
        return {"status": "SKIP"}

    # 3. Génération des probes de recherche
    if logger_active: logger.info(f"🔍 [Research] Intent: {research_intent[:150]}...")
    research_gen = generate_cypher_for_request(research_intent, research=True, additional_context=current_context)
    
    if not research_gen.get("possible") or not research_gen.get("queries"):
        if logger_active: logger.error("❌ [Research] Impossible de générer des probes")
        return {"status": "SKIP"}

    # Formatage des probes
    r_queries = research_gen.get("queries")
    if isinstance(r_queries, list):
        r_queries = "".join(r_queries) if len(r_queries[0]) == 1 else "; ".join(r_queries)
    if not r_queries or not isinstance(r_queries, str) or not r_queries.strip():
        return {"status": "SKIP"}

    # 4. Exécution des probes
    results_research = execute_multiple_probes(r_queries)
    if not results_research:
        if logger_active: logger.warning("⚠️ [Research] Aucun résultat de probe")
        return {"status": "SKIP"}

    # 5. Extraction de connaissances et mise à jour du contexte
    if logger_active: logger.info("🧠 [Research] Analyse des découvertes...")
    new_facts = analyse_research_result(results_research)
    
    new_context = current_context
    if new_facts and new_facts.strip():
        new_context += f"\n\n--- RESEARCH #{probe_count} ---\n{new_facts}"
        if logger_active: logger.success(f"🧠 [Research] Nouvelles connaissances acquises:\n   {new_facts[:200]}...")
    else:
        if logger_active: logger.warning("⚠️ [Research] Aucune nouvelle information extraite")

    # 6. Création de l'entrée d'historique
    history_entry = {
        "attempt": f"RESEARCH-{probe_count}",
        "query": f"[{len(results_research)} probes exécutées]",
        "success": any(p["success"] for p in results_research),
        "error": None,
        "count": sum(p["count"] for p in results_research),
        "data_sample": [p["data_sample"] for p in results_research if p["data_sample"]],
        "research_details": results_research
    }

    # 7. Régénération de la requête principale
    if logger_active: logger.info("🔄 [Research] Régénération de la requête principale avec contexte enrichi...")
    gen_result = generate_cypher_for_request(user_intent, additional_context=new_context)
    
    if gen_result.get("possible") and gen_result.get("queries"):
        queries = gen_result["queries"]
        final_query = queries[0] if isinstance(queries, list) else queries
        if logger_active: logger.success("✅ [Research] Requête principale mise à jour")
        return {"status": "SUCCESS", "query": final_query, "context": new_context, "history_entry": history_entry}
    
    return {"status": "SKIP"}


@observe()
def process_user_request_with_retry(user_intent: str, max_retries: int = 5, logger_active: bool = False) -> Dict[str, Any]:
    if logger_active:
        logger.section(f"Pipeline de traitement")
        logger.info(f"📝 Intent: '{user_intent}'")
    
    # === INITIALISATION ===
    gen_result = generate_cypher_for_request(user_intent)
    if not gen_result.get("possible"):
        if logger_active: logger.error("❌ [Pipeline] Requête impossible à traduire en Cypher")
        return {"status": "IMPOSSIBLE", "message": gen_result.get("explanation")}
    
    current_queries = gen_result.get("queries", [])
    current_query = current_queries[0] if isinstance(current_queries, list) and current_queries else (current_queries if isinstance(current_queries, str) else "")
    
    if logger_active: logger.info(f"🎯 [Pipeline] Requête initiale générée : {current_query[:100]}...")

    history = []
    research_context = ""
    attempt = 1
    probe_count = 0
    max_probes = 10
    
    # === BOUCLE PRINCIPALE ===
    while attempt <= max_retries:
        if logger_active: logger.info(f"🔄 [Tentative {attempt}/{max_retries}]")
        
        # 1. Exécution
        exec_res = execute_cypher_test(current_query)
        history.append({
            "attempt": attempt, "query": current_query, "success": exec_res.get("success"),
            "error": exec_res.get("error"), "count": exec_res.get("count", 0), "data_sample": exec_res.get("data", [])[:3]
        })
        
        if exec_res.get("success") and logger_active:
            logger.success(f"✅ [Tentative {attempt}] Succès: {exec_res.get('count', 0)} ligne(s)")
        elif logger_active:
            logger.warning(f"⚠️ [Tentative {attempt}] Échec: {exec_res.get('error', 'Unknown error')[:100]}...")
            
        # 2. Analyse
        effective_context = research_context + ("\n\n[SYSTEM NOTICE: RESEARCH LIMIT REACHED.]" if probe_count >= max_probes else "")
        analysis = analyze_and_correct_query({"user_intent": user_intent, "history": history, "additional_context": effective_context})
        status = analysis.get("status")
        
        if logger_active: logger.info(f"🧠 [Analyse] Statut: {status} | Explication: {analysis.get('message', 'N/A')[:100]}...")
        
        # 3. Routing (Stratégie)
        if status == "VALID":
            if logger_active: logger.success("✅ [Pipeline] Requête VALIDÉE !")
            return {
                "status": "SUCCESS", "final_query": current_query, "data": exec_res.get("data", []),
                "attempts": attempt, "research_cycles": probe_count
            }
            
        elif status == "CORRECTED":
            if analysis.get("corrected_query"):
                current_query = analysis["corrected_query"]
            attempt += 1
            
        elif status == "RESEARCH":
            probe_count += 1
            
            # Limite atteinte
            if probe_count > max_probes:
                if logger_active: logger.warning(f"🛑 Limite de {max_probes} recherches atteinte")
                if analysis.get("corrected_query"):
                    current_query = analysis["corrected_query"]
                    attempt += 1
                    continue
                return {
                    "status": "FAILED", "reason": "Max research probes reached", 
                    "attempts": attempt, "research_cycles": probe_count, "history": history
                }

            # Lancement de la sous-routine de recherche
            if logger_active: logger.section(f"Research Mode (Probe {probe_count}/{max_probes})")
            research_result = _perform_research_cycle(user_intent, analysis, research_context, probe_count, logger_active)
            
            # Traitement de la sortie de la sous-routine
            if research_result["status"] == "SUCCESS":
                current_query = research_result["query"]
                research_context = research_result["context"]
                history.append(research_result["history_entry"])
                # On ne fait PAS attempt += 1, on repasse la nouvelle requête générée !
            elif research_result["status"] == "NEW_QUERY":
                current_query = research_result["query"]
                attempt += 1
            else:
                attempt += 1
        
        else:
            attempt += 1 # Sécurité pour les status inconnus
            
    # === ÉCHEC FINAL ===
    if logger_active: logger.error(f"❌ [Pipeline] Échec après {max_retries} tentatives")
    return {
        "status": "FAILED", "user_intent": user_intent, "history": history,
        "attempts": attempt - 1, "research_cycles": probe_count, "reason": "Max retries reached"
    }
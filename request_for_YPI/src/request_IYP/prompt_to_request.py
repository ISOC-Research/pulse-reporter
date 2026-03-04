from typing import Dict, Any, List, Union
from langfuse import observe
from src.request_IYP.generat_request import generate_cypher_for_request
from src.request_IYP.request_testing import execute_cypher_test
from src.request_IYP.analyse_results_request import analyse_research_result, analyze_and_correct_query
from src.request_IYP.probes_execution import execute_multiple_probes
from src.utils.logger import logger


def _format_probes(queries: Union[str, List[str], None]) -> Union[str, None]:
    if not queries: return None
    if isinstance(queries, list): return "".join(queries) if len(queries[0]) == 1 else "; ".join(queries)
    return queries if isinstance(queries, str) and queries.strip() else None

def _extract_single_query(queries: Union[str, List[str], None]) -> str:
    if not queries: return ""
    return queries[0] if isinstance(queries, list) else queries

def _log(active: bool, level: str, msg: str):
    if active: getattr(logger, level)(msg)


def _perform_research_cycle(user_intent: str, analysis: Dict[str, Any], current_context: str, probe_count: int, logger_active: bool) -> Dict[str, Any]:
    intent = analysis.get("corrected_query", "").strip()
    r_gen = generate_cypher_for_request(intent, research=True, additional_context=current_context)
    
    probes_query = _format_probes(r_gen.get("queries"))
    if not r_gen.get("possible") or not probes_query: 
        return {"status": "SKIP"}

    results = execute_multiple_probes(probes_query)
    if not results: return {"status": "SKIP"}

    facts = analyse_research_result(results)
    new_context = current_context + (f"\n\n--- RESEARCH #{probe_count} ---\n{facts}" if facts and facts.strip() else "")

    final_gen = generate_cypher_for_request(user_intent, additional_context=new_context)
    final_query = _extract_single_query(final_gen.get("queries"))
    
    if final_gen.get("possible") and final_query:
        return {
            "status": "SUCCESS", "query": final_query, "context": new_context,
            "history_entry": {
                "attempt": f"RESEARCH-{probe_count}",
                "query": f"[{len(results)} probes exécutées]",
                "success": any(p.get("success") for p in results),
                "error": None, "count": sum(p.get("count", 0) for p in results),
                "data_sample": [p.get("data_sample") for p in results if p.get("data_sample")],
                "research_details": results
            }
        }
    return {"status": "SKIP"}

# ==========================================
# PIPELINE PRINCIPAL
# ==========================================
@observe()
def process_user_request_with_retry(user_intent: str, max_retries: int = 5, logger_active: bool = False) -> Dict[str, Any]:
    gen_result = generate_cypher_for_request(user_intent)
    
    if not gen_result.get("possible"):
        _log(logger_active, "error", "❌ [Pipeline] Requête impossible à traduire en Cypher")
        return {"status": "IMPOSSIBLE", "message": gen_result.get("explanation")}

    # Utilisation du helper existant plutôt que la longue condition inline
    current_query = _extract_single_query(gen_result.get("queries"))
    _log(logger_active, "info", f"🎯 [Pipeline] Requête initiale générée : {current_query[:100]}...")

    history, research_context = [], ""
    attempt, probe_count, max_probes = 1, 0, 10
    
    while attempt <= max_retries:
        _log(logger_active, "info", f"🔄 [Tentative {attempt}/{max_retries}]")
        
        # 1. Exécution
        exec_res = execute_cypher_test(current_query)
        history.append({
            "attempt": attempt, "query": current_query, "success": exec_res.get("success"),
            "error": exec_res.get("error"), "count": exec_res.get("count", 0), 
            "data_sample": exec_res.get("data", [])[:3]
        })
        
        _log(logger_active, "success" if exec_res.get("success") else "warning", 
             f"✅ Succès: {exec_res.get('count', 0)} ligne(s)" if exec_res.get("success") else f"⚠️ Échec: {str(exec_res.get('error'))[:100]}...")
            
        # 2. Analyse
        effective_context = research_context + ("\n\n[SYSTEM NOTICE: RESEARCH LIMIT REACHED.]" if probe_count >= max_probes else "")
        analysis = analyze_and_correct_query({"user_intent": user_intent, "history": history, "additional_context": effective_context})
        status, corrected_query = analysis.get("status"), analysis.get("corrected_query")
        
        _log(logger_active, "info", f"🧠 [Analyse] Statut: {status} | Explication: {analysis.get('message', 'N/A')[:100]}...")
        
        # 3. Routing (Stratégie)
        if status == "VALID":
            _log(logger_active, "success", "✅ [Pipeline] Requête VALIDÉE !")
            return {"status": "SUCCESS", "final_query": current_query, "data": exec_res.get("data", []), "attempts": attempt, "research_cycles": probe_count}
            
        if status == "RESEARCH":
            probe_count += 1
            if probe_count > max_probes:
                _log(logger_active, "warning", f"🛑 Limite de {max_probes} recherches atteinte")
                if corrected_query:
                    current_query = corrected_query
                    attempt += 1
                    continue
                return {"status": "FAILED", "reason": "Max research probes reached", "attempts": attempt, "research_cycles": probe_count, "history": history}

            _log(logger_active, "info", f"🔍 Research Mode (Probe {probe_count}/{max_probes})")
            research_result = _perform_research_cycle(user_intent, analysis, research_context, probe_count, logger_active)
            
            if research_result["status"] == "SUCCESS":
                current_query, research_context = research_result["query"], research_result["context"]
                history.append(research_result["history_entry"])
                continue # On boucle sans incrémenter "attempt"
            
            if research_result.get("status") == "NEW_QUERY":
                current_query = research_result["query"]
                
        elif status == "CORRECTED" and corrected_query:
            current_query = corrected_query

        # Si ce n'est pas VALID, et que ce n'est pas un SUCCESS de Research, on consomme une tentative
        attempt += 1 

    _log(logger_active, "error", f"❌ [Pipeline] Échec après {max_retries} tentatives")
    return {"status": "FAILED", "user_intent": user_intent, "history": history, "attempts": attempt - 1, "research_cycles": probe_count, "reason": "Max retries reached"}
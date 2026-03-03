import json
import os
from langfuse import observe

from src.utils.paths import get_prompt_path
from src.request_IYP.prompt_to_request import process_user_request_with_retry
from src.utils.llm import get_llm, call_llm_chain
from src.utils.logger import logger

@observe(name="Interface_Utilisateur")
def generate_response_with_IYP(query_intent: str, logger_active: bool = False) -> dict:
    """Generates a response for a given user intent using the IYP system.
    Returns:
        dict: {'status'     : 'valide'|'invalide',
            'cypher_query'  : str|None,
            'raw_results'   : list|None,
            'interpretation': str|None,
            'error_message' : str|None}
    """
    if logger_active:    logger.info(f"Processing intent: {query_intent}")
    
    pipeline_result = process_user_request_with_retry(query_intent, logger_active=logger_active)
    
    if pipeline_result.get("status") == "SUCCESS":
        return {'status'    : 'valide',
            'cypher_query'  : pipeline_result.get("final_query"),
            'raw_results'   : pipeline_result.get("data"),
            'interpretation': _interpret_results(query_intent, pipeline_result.get("data"), logger_active=logger_active),
            'error_message' : None}
    else:
        error_msg = pipeline_result.get("message") or pipeline_result.get("reason", "Unknown pipeline error")
        if logger_active:    logger.error(f"Interface failed to retrieve valid data: {error_msg}")
        return {'status'    : 'invalide',
            'cypher_query'  : None,
            'raw_results'   : None,
            'interpretation': None,
            'error_message' : error_msg}
    


@observe(name="Interpret_Results", as_type="generation")
def _interpret_results(intent: str, data: list, logger_active: bool = False) -> str:
    """Asks the LLM to interpret the raw results of the Cypher query in the context of the user's original intent."""
    
    if not data:    return "No results found for the given query."
        
    safe_data = data[:100] 
    data_json = json.dumps(safe_data, indent=2, ensure_ascii=False)
    
    if len(data) > 100 and logger_active:    logger.warning(f"Data truncated for LLM: 100 rows kept out of {len(data)}")

    try:
        interpretation = call_llm_chain(
            llm                   = get_llm("smart"),
            system_prompt_path    = get_prompt_path(os.path.join("IYP", "interpret_results_system.txt")),
            human_prompt_template = get_prompt_path(os.path.join("IYP", "interpret_results_human.txt")),
            variables             = {"intent": intent, "data_json": data_json}
        )
        return interpretation
        
    except Exception as e:
        if logger_active:    logger.error(f"Error during result interpretation: {e}")
        return "Sorry, an error occurred while interpreting the results."
    

import os
import yaml
from pathlib import Path
from langfuse import get_client
from src.utils.logger import logger


def load_text_file(path: str) -> str:
    """Lit un fichier texte brut (ex: prompt, .cypher)."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_smart_prompt(file_path: str) -> str:
    prompt_name = Path(file_path).stem 
    
    try:
        langfuse = get_client()
        lf_prompt = langfuse.get_prompt(prompt_name)
        
        logger.info(f"☁️ Prompt '{prompt_name}' chargé depuis Langfuse.")
        return lf_prompt.compile()
        
    except Exception as e:
        logger.warning(f"⚠️ Impossible de charger le prompt '{prompt_name}' depuis Langfuse: {e}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"❌ Erreur critique : Le fichier prompt {file_path} est introuvable.")
        return ""

def load_yaml_file(path: str) -> dict:
    """Lit un fichier de configuration YAML."""
    if not os.path.exists(path):
        print(f"⚠️ Warning: YAML template not found at {path}")
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
    

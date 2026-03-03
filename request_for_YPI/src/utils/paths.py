from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

PROMPTS_DIR = PROJECT_ROOT / "prompt" 

def get_prompt_path(filename: str) -> str:

    prompt_path = PROMPTS_DIR / filename
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Le fichier prompt est introuvable : {prompt_path}")
        
    return str(prompt_path)
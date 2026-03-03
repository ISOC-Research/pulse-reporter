from dotenv import load_dotenv
from src.request_IYP.interface import generate_response_with_IYP

from src.request_IYP.interface import generate_response_with_IYP

# L'import correct pour Langfuse v3
from langfuse import get_client

if __name__ == "__main__":
    load_dotenv()
    
    print(generate_response_with_IYP(
        "Quels opérateurs étrangers détiennent une position dominante sur le marché en France ?", 
        logger_active=True
    ))
    langfuse = get_client()
    langfuse.flush()

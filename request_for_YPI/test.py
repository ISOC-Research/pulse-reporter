from dotenv import load_dotenv
from langfuse import get_client
from src.request_IYP.interface import generate_response_with_IYP

if __name__ == "__main__":
    load_dotenv()
    
    print(generate_response_with_IYP(
        "What is the market share in England of the largest French internet service provider?"
, 
        logger_active=True
    ))
    langfuse = get_client()
    langfuse.flush()

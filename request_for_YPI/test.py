from dotenv import load_dotenv
from src.request_IYP.interface import generate_response_with_IYP
from langfuse import get_client

if __name__ == "__main__":
    load_dotenv()
    
    print(generate_response_with_IYP(
        "quelles sont les parts de marché en angleterre du plus gros internet provider français ?", 
        logger_active=True
    ))
    langfuse = get_client()
    langfuse.flush()

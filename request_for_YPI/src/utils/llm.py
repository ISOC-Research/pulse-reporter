# src/utils/llm.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(mode_or_model: str = "smart", temperature: float = 0.2): 
    if mode_or_model == "fast":
        model_name = "gemini-2.5-flash-lite"
        temperature = 0.1
    elif mode_or_model == "smart":
        model_name = "gemini-2.5-flash-lite"
        temperature = 0.2
    elif mode_or_model == "reasoning":
        model_name = "gemini-2.0-flash-thinking-exp"
        temperature = 0
    elif mode_or_model == "report_redaction":
        model_name = "gemini-3-pro-preview"
        temperature = 0.3
    elif mode_or_model == "question":
        model_name = "gemini-3-flash-preview"
    else:
        # Fallback
        model_name = "gemini-2.5-flash-lite"
        temperature = 0.2

    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        return llm
    except Exception as e:
        print(f"❌ Error in the loading of the model {model_name}: {e}")
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.2,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
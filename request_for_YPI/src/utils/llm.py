import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.utils.loaders import load_text_file
from src.utils.logger import logger
from langfuse.langchain import CallbackHandler 

def call_llm_chain(llm, system_prompt_path: str, human_prompt_template: str, variables: dict, callbacks: list = None) -> str:
    try:
        system_prompt = load_text_file(system_prompt_path)
        human_prompt  = load_text_file(human_prompt_template)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt)
        ])
        
        chain = prompt | llm
        
        langfuse_handler = CallbackHandler()
        
        if callbacks is None:
            callbacks = [langfuse_handler]
        else:
            callbacks.append(langfuse_handler)

        response = chain.invoke(variables, config={"callbacks": callbacks})
        
        return response.content.strip()
    except Exception as e:
        logger.error(f"Error in the calling of the LLM (chain) : {e}")
        raise

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
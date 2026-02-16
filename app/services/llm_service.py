import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b", 
        api_key=groq_api_key,    
        temperature=0.0,            
        max_tokens=4000,            
        max_retries=2              
    )


import requests
import os
from logger import logger


URL:str =  "http://localhost:11434/api/chat"
MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME", "phi3:mini")
def chatRequest(messages:dict)-> str:
    print(f"regular print;Chat Request: MODEL_NAME={MODEL_NAME}")
    logger.debug(f"Chat Request: MODEL_NAME={MODEL_NAME}")
    payload = {
        "model":MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options":{"temperature":0.0}
    }
    resp = requests.post(URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["message"]["content"]


             
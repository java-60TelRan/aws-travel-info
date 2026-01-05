
import requests



URL:str =  "http://localhost:11434/api/chat"
MODEL_NAME: str = "phi3"
def chatRequest(messages:dict)-> str:
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


             
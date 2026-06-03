import requests

OLLAMA_CHAT_URL = "http://ollama:11434/api/generate"

def generate_response(prompt: str):
    res = requests.post(
        OLLAMA_CHAT_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]

import requests

OLLAMA_CHAT_URL = "http://ollama:11434/api/generate"


def generate_answer(prompt: str, model: str = "llama3.2"):
    try:
        res = requests.post(
            OLLAMA_CHAT_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        return res.json().get("response", "")

    except Exception as e:
        print("❌ LLM error:", e)
        return "Error generating response"

import requests
from config.settings import OLLAMA_CHAT_URL, OLLAMA_MODEL


class LLMService:

    def __init__(self):
        self.url = OLLAMA_CHAT_URL
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str) -> str:
        try:
            res = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "options": {
                        "num_predict": 200  # 🔥 limit response length
                    }
                },
                timeout=120
            )

            res.raise_for_status()
            data = res.json()

            return data.get("response", "")

        except requests.RequestException as e:
            return f"LLM request failed: {str(e)}"

        except Exception as e:
            return f"Unexpected error: {str(e)}"
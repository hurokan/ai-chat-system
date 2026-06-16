import requests
from config.settings import OLLAMA_CHAT_URL, OLLAMA_MODEL


class LLMService:

    def __init__(self):
        self.url = OLLAMA_CHAT_URL
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str) -> str:

        res = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        print("OLLAMA RAW RESPONSE:", res.text)  # 🔥 DEBUG

        res.raise_for_status()
        data = res.json()

        # 🔥 SAFE EXTRACTION
        return (
            data.get("response")
            or data.get("message")
            or data.get("text")
            or ""
        )
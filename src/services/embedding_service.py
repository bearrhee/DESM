import os
import requests
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": os.getenv("HTTP_REFERER", "https://github.com/bear/deas").strip(),
            "X-Title": os.getenv("X_TITLE", "DEAS_Agent").strip()
        }

    def get_embedding(self, text: str, model: str = "text-embedding-3-small"):
        """
        OpenRouter를 통해 텍스트 임베딩을 가져옵니다.
        (참고: OpenRouter는 OpenAI SDK와 호환되거나 직접 API 호출 가능)
        """
        # OpenAI SDK를 사용하는 것이 정신 건강에 이롭지만, 
        # API 직접 호출 방식으로 구현하여 제어권 확보
        payload = {
            "model": model,
            "input": text
        }
        
        response = requests.post(f"{self.base_url}/embeddings", headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()['data'][0]['embedding']

if __name__ == "__main__":
    service = EmbeddingService()
    # test_emb = service.get_embedding("Hello world")
    # print(len(test_emb))

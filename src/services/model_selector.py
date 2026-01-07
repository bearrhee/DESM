import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ModelSelector:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": os.getenv("HTTP_REFERER", "").strip(),
            "X-Title": os.getenv("X_TITLE", "").strip()
        }

    def select_model(self, task_type: str):
        """
        태스크 유형에 따라 적합한 모델을 선택합니다.
        .env의 LLM_MODEL이 상위 우선순위를 가집니다.
        """
        env_model = os.getenv("LLM_MODEL")
        if env_model:
            return env_model
            
        if task_type == "simple":
            return "google/gemini-2.0-flash-exp:free"
        elif task_type == "complex":
            return "anthropic/claude-3.5-sonnet"
        else:
            return "openai/gpt-4o-mini"

    def get_completion(self, prompt: str, task_type: str = "simple"):
        model = self.select_model(task_type)
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
            if response.status_code != 200:
                 print(f"DEBUG: OpenRouter Error {response.status_code}: {response.text}")
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error calling OpenRouter: {e}")
            return "죄송합니다. 현재 상담 시스템에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."

if __name__ == "__main__":
    selector = ModelSelector()
    # print(selector.get_completion("안녕하세요?"))
    pass

import requests
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENROUTER_API_KEY").strip()
url = "https://openrouter.ai/api/v1/auth/key"

headers = {
    "Authorization": f"Bearer {key}"
}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

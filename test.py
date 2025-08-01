import os
import requests
from dotenv import load_dotenv

# Load .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("HUGGINGFACE_API_KEY")
print("DEBUG: HUGGINGFACE_API_KEY =", api_key)

def ask_bot(prompt):
    if not api_key:
        return "API key not set."

    # ✅ FIXED URL
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        response.raise_for_status()
        data = response.json()
        return data[0]["generated_text"]
    except requests.exceptions.HTTPError:
        return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Unexpected error: {e}"

if __name__ == "__main__":
    print(ask_bot("What is affiliate marketing?"))

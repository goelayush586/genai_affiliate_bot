import os
import requests
from dotenv import load_dotenv

load_dotenv()

response_scores = {}

def ask_bot(prompt):
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }

    resp = requests.post(API_URL, headers=headers, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        return data[0].get("generated_text", "")
    return f"Error {resp.status_code}: {resp.text}"

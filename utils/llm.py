import requests
import time

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
    "Content-Type": "application/json"
}

def call_llm(prompt, temperature=0.7, max_tokens=2000):
    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct:novita",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    for _ in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code != 200:
                print("Error:", response.text)
                time.sleep(2)
                continue
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("Exception:", e)
            time.sleep(2)
    return "⚠️ Model failed to respond"

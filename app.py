import base64
from io import BytesIO
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()
api_key = os.getenv("api_key")

def check_output(output):
    output = output.split("\n\n")
    if len(output)<2:
        return False   
    return True

def generate_alt_text(sample, image_base64, prompt):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are an AI assistant that generates structured alt text following strict formatting rules. Do not deviate from the given guidelines."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt+sample},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
            ]}
        ],
        "max_tokens": 300
    }

    retries = 0
    max_retries = 5
    wait_time=2

    while retries < max_retries:
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            data = response.json()
            print(data)
            content = data['choices'][0]['message']['content']
            if check_output(content):
                return content
            print(content)
        except Exception as e:
            print(f"Attempt {retries+1} failed: {e}")
            retries+=1
            time.sleep(wait_time)
            wait_time+=1
    return "failed to fetch response after multiple attempts"

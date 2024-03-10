import os
from dotenv import load_dotenv
import requests
import json
load_dotenv("env/.env")
org_key=os.getenv('OPENAI_ORG_ID')
api_key = os.getenv('OPENAI_API_KEY')




def call_gpt4_turbo(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        "model": "gpt-4-0125-preview",
        "messages": [{"role": "user", "content": message},
          {"role": "system", "content": "You are a voice assistant who responds to user voice input. Formulate your answers for voice responses, be concise but friendly. Try to keep your responses under 30 seconds."}],
        "temperature": 0.7,
        "max_tokens": 256
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

    response_json = response.json()
    assistant_message = response_json['choices'][0]['message']['content']
    return assistant_message

user_input = input("Enter your message: ")
print(call_gpt4_turbo(user_input))
import requests

# OpenAI API URL
url = "https://api.openai.com/v1/chat/completions"

# Dein API-Schlüssel
api_key = ""

# Header mit Authorization
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Daten für den POST-Request
data = {
    "model": "gpt-4o-mini", 
    "messages": [
        {"role": "system", "content": "You are an assistant that generates bedtime stories."},
        {"role": "user", "content": "Tell me a three sentence bedtime story about a unicorn."}
    ],
    "max_tokens": 300
}

# Sende den POST-Request
response = requests.post(url, headers=headers, json=data)

# Überprüfe die Antwort
if response.status_code == 200:
    print("Response:", response.json()["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}, {response.text}")
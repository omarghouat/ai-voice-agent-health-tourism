import requests

def generate_response(prompt):
    response = requests.post('http://localhost:11434/api/generate', json={
        "model": "llama3",
        "prompt": prompt
    })
    return response.json()['response']

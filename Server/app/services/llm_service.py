import requests

def send_data_to_server_LLM(url: str, question: str, system_prompt: str):
    payload = {
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": question}]},
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=None)
        return response.json()
    except Exception as e:
        return {"error": f"Error sending LLM application: {e}"}

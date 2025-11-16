import requests

def send_data_to_server_LLM(url: str, question: str, system_prompt: str):
    """
    Sends a question and a system prompt to an LLM server endpoint.

    Args:
        url (str): The target server URL.
        question (str): The user's input or query.
        system_prompt (str): The system-level instruction for the LLM.

    Returns:
        dict: The parsed JSON response from the server, or an error message.
    """
    payload = {
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": question}]},
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=None)

        # Log raw response for debugging
        print("=== RAW RESPONSE STATUS ===")
        print(response.status_code)

        print("=== RAW RESPONSE TEXT ===")
        print(response.text)  # Most important for debugging

        # Try to parse JSON response
        return response.json()

    except Exception as e:
        return {"error": f"Error sending LLM request: {e}"}
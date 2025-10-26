import requests

def send_data_to_server_search(url: str, keywords: list):
    payload = {"query": keywords}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        return response.json()
    except Exception as e:
        return {"error": f"שגיאה בשליחת הבקשה לשרת חיפוש: {e}"}

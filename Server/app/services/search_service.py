import requests

# def send_data_to_server_search(url: str, keywords: list):
#     payload = {"query": keywords}
#     headers = {"Content-Type": "application/json"}
#     try:
#         response = requests.post(url, json=payload, headers=headers, timeout=None)
#         return response.json()
#     except Exception as e:
#         return {"error": f"Error sending request to search server: {e}"}

from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "MyStrongPassword123!"),
    use_ssl=False
)

# keywords = ["machine learning", "AI", "neural networks"]
def send_data_to_server_search(url: str, keywords: list):
    merged_results = {}

    for keyword in keywords:
        query = {
            "size": 20,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["title^2", "text"],  # title מקבל פי2  משקל
                    "type": "best_fields"
                }
            }
        }

        response = client.search(index="wikipedia", body=query)

        for hit in response["hits"]["hits"]:
            doc_id = hit["_id"]
            score = hit["_score"]
            source = hit["_source"]
            title = source.get("title", "No Title")
            text = source.get("text", "")  # עד 500 תווים כדי לא להעמיס

            if doc_id not in merged_results or merged_results[doc_id]["score"] < score:
                merged_results[doc_id] = {"title": title, "score": score, "text": text}

    # מיון לפי score ולקיחת 5 המובילים
    top5 = sorted(merged_results.values(), key=lambda x: x["score"], reverse=True)[:5]

    # for doc in top5:
    #     print(f"\nTitle: {doc['title']} | Score: {doc['score']:.3f}")
    #     print(f"Text: {doc['text']}")
    #     print("-" * 80)
    return {"results": top5}
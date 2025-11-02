from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "MyStrongPassword123!"),
    use_ssl=False
)
def send_data_to_server_search(url: str, keywords: list):
    merged_results = {}

    for keyword in keywords:
        query = {
            "size": 20,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["title^2", "text"], 
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
            text = source.get("text", "")

            if doc_id not in merged_results or merged_results[doc_id]["score"] < score:
                merged_results[doc_id] = {"title": title, "score": score, "text": text}

    top5 = sorted(merged_results.values(), key=lambda x: x["score"], reverse=True)[:5]
    return {"results": top5}
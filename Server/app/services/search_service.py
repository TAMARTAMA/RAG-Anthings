from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "MyStrongPassword123!"),
    use_ssl=False
)
def send_data_to_server_search( keywords: list):
    body = {
        "size": 10,
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": kw,
                            "fields": ["title^2", "text"],
                            "type": "best_fields"
                        }
                    } for kw in keywords
                ],
                "minimum_should_match": 1  
            }
        }
    }
    try:
        res = client.search(index="wikipedia", body=body)

        hits = res.get("hits", {}).get("hits", [])
        results = [
            {
                "title": hit["_source"].get("title", "No Title"),
                "score": hit.get("_score", 0),
                "url": hit["_source"].get("url", "No URL")  # 👈 נוסף שדה URL
            }
            for hit in hits
        ]
        return {"results": results}
    except Exception as e:
        return {"error": f"Error sending request to search server: {e}"}
        
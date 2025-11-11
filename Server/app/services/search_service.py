from opensearchpy import OpenSearch

# ----------------------------------------
# OpenSearch client configuration
# ----------------------------------------
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "MyStrongPassword123!"),
    use_ssl=False
)


# ----------------------------------------
# Search for keywords in a given index
# ----------------------------------------
def send_data_to_server_search(keywords: list, index_name: str):
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
                    }
                    for kw in keywords
                ],
                "minimum_should_match": 1
            }
        }
    }

    try:
        if client.indices.exists(index=index_name):
            res = client.search(index=index_name, body=body)
        else:
            res = client.search(index="wikipedia", body=body)

        hits = res.get("hits", {}).get("hits", [])
        results = [
            {
                "title": hit["_source"].get("title", "No Title"),
                "score": hit.get("_score", 0),
                "url": hit["_source"].get("url", "No URL")
            }
            for hit in hits
        ]
        return {"results": results}

    except Exception as e:
        return {"error": f"Error sending request to search server: {e}"}


# ----------------------------------------
# Create index if it does not exist
# ----------------------------------------
def create_index_if_not_exists(index_name: str):
    try:
        if not client.indices.exists(index=index_name):
            body = {
                "settings": {
                    "index": {"number_of_shards": 1, "number_of_replicas": 0}
                },
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "text": {"type": "text"},
                        "user_id": {"type": "keyword"}
                    }
                }
            }
            client.indices.create(index=index_name, body=body)
            print(f"Created new index: {index_name}")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"Error creating index {index_name}: {e}")


# ----------------------------------------
# Add documents to index
# ----------------------------------------
def add_documents_to_index(index_name: str, documents: list[dict]):
    """
    Each document should be a dict:
    {'title': 'Paris', 'text': 'Capital of France'}
    """
    try:
        create_index_if_not_exists(index_name)
        for doc in documents:
            client.index(index=index_name, id=doc.get("title"), body=doc)
            client.indices.refresh(index=index_name)
        print(f"Added {len(documents)} documents to index '{index_name}'")
    except Exception as e:
        print(f"Error indexing documents to {index_name}: {e}")


# ----------------------------------------
# Delete an existing index
# ----------------------------------------
def delete_index(index_name: str):
    try:
        if client.indices.exists(index=index_name):
            client.indices.delete(index=index_name)
            print(f"Deleted index: {index_name}")
        else:
            print(f"Index '{index_name}' does not exist.")
    except Exception as e:
        print(f"Error deleting index {index_name}: {e}")


# ----------------------------------------
# List all indexes in the system
# ----------------------------------------
def list_all_indexes():
    try:
        indexes = list(client.indices.get_alias(index="*").keys())
        return indexes
    except Exception as e:
        print(f"Error fetching indexes: {e}")
        return []

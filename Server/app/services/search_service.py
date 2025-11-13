from opensearchpy import OpenSearch, TransportError, AuthorizationException

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
    """
    מבצע חיפוש לפי רשימת מילות מפתח באינדקס מסוים.
    """
    body = {
        "size": 8,
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
            # חיפוש בברירת מחדל אם האינדקס לא קיים
            res = client.search(index="wikipedia", body=body)

        hits = res.get("hits", {}).get("hits", [])
        results = [
            {
                "title": hit["_source"].get("title", "No Title"),
                "score": hit.get("_score", 0),
                "url": hit["_source"].get("url", "No URL"),
                "text" :hit["_source"].get("text","No Text")
            }
            for hit in hits
        ]
        return {"results": results}

    except Exception as e:
        return {"error": f"Error sending request to search server: {e}"}


# ----------------------------------------
# Create index if it does not exist
# ----------------------------------------
def create_index_if_not_exists(index_name: str) -> bool:
    """
    יוצר אינדקס חדש אם אינו קיים.
    מחזיר True אם הצליח, אחרת מעלה Exception.
    """
    print(f"🔗 Connected to: {client.transport.hosts}")
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

            response = client.indices.create(index=index_name, body=body)
            if not response.get("acknowledged"):
                raise Exception(f"Index creation for '{index_name}' not acknowledged.")
            print(f"✅ Created new index: {index_name}")
            return True
        else:
            print(f"ℹ️ Index '{index_name}' already exists.")
            return True

    except AuthorizationException as e:
        print(f"🚫 Authorization error: {e}")
        raise
    except TransportError as e:
        print(f"❌ OpenSearch transport error while creating '{index_name}': {e}")
        raise
    except Exception as e:
        print(f"❌ General error creating index '{index_name}': {e}")
        raise


# ----------------------------------------
# Add documents to index
# ----------------------------------------
def add_documents_to_index(index_name: str, documents: list[dict]) -> bool:
    """
    מוסיף מסמכים לאינדקס ומדפיס אם נוצרו בפועל.
    """
    try:
        create_index_if_not_exists(index_name)
        success_count = 0
        fail_count = 0

        for doc in documents:
            try:
                res = client.index(index=index_name, id=doc.get("title"), body=doc)
                # בדיקה לפי התשובה מהשרת
                result = res.get("result", "")
                if result in ["created", "updated"]:
                    success_count += 1
                else:
                    fail_count += 1
                    print(f"⚠️  Failed to insert doc '{doc.get('title')}', server result: {result}")
            except Exception as e:
                fail_count += 1
                print(f"❌ Error inserting document '{doc.get('title')}': {e}")

        client.indices.refresh(index=index_name)

        # בדיקה כמה באמת יש באינדקס
        count_response = client.count(index=index_name)
        total_docs = count_response["count"]

        print(f"✅ Added {success_count} documents, failed {fail_count}.")
        print(f"📦 Total documents currently in index '{index_name}': {total_docs}")

        # אם נכשלו מסמכים — הסבר
        if fail_count > 0:
            print("⚠️ חלק מהמסמכים לא נכנסו לאינדקס. ייתכן שהייתה בעיה בהרשאות, "
                  "חסימת כתיבה (read-only cluster block), או שם אינדקס לא תקין.")

        return success_count > 0 and fail_count == 0

    except Exception as e:
        print(f"❌ Error indexing documents to '{index_name}': {e}")
        raise

# ----------------------------------------
# Delete an existing index
# ----------------------------------------
def delete_index(index_name: str) -> bool:
    """
    מוחק אינדקס קיים מ־OpenSearch.
    מחזיר True אם נמחק בהצלחה, False אם לא נמצא.
    במקרי כשל – זורק חריגה עם פירוט השגיאה.
    """
    try:
        if client.indices.exists(index=index_name):
            response = client.indices.delete(index=index_name)
            acknowledged = response.get("acknowledged", False)

            if acknowledged:
                print(f"🗑️ Deleted index: {index_name}")
                return True
            else:
                # OpenSearch החזיר תגובה אך לא אישר את המחיקה
                raise Exception(f"Delete request for index '{index_name}' not acknowledged by OpenSearch.")

        else:
            print(f"ℹ️ Index '{index_name}' does not exist.")
            return False

    except Exception as e:
        print(f"❌ Error deleting index '{index_name}': {e}")
        raise Exception(f"Failed to delete index '{index_name}': {str(e)}")


# ----------------------------------------
# List all indexes in the system
# ----------------------------------------
def list_all_indexes() -> list[str]:
    """
    מחזיר רשימה של כל האינדקסים הקיימים במערכת.
    """
    try:
        indexes = list(client.indices.get_alias(index="*").keys())
        print(f"📦 Found {len(indexes)} indexes.")
        return indexes
    except Exception as e:
        print(f"❌ Error fetching indexes: {e}")
        return []


# ----------------------------------------
# Debug mode (manual execution)
# ----------------------------------------
if __name__ == "__main__":
    print("Existing indexes:", list_all_indexes())
    try:
        # דוגמת הרצה
        create_index_if_not_exists("test-index")
    except Exception as err:
        print(f"⚠️ Exception caught: {err}")

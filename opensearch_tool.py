from mcp_instance import mcp
from opensearchpy import OpenSearch
import os
client = OpenSearch(
    hosts=[{'host': os.getenv("OPENSEARCH_HOST"), 'port': 443}],
    http_auth=(os.getenv("OPENSEARCH_USER"), os.getenv("OPENSEARCH_PASS")),
    use_ssl=True
)
@mcp.tool("search_products", description="Search products in OpenSearch by natural language query")
def search_products(query: str):
    try:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "barcode", "ref", "description"],
                    "fuzziness": "AUTO"
                }
            }
        }
        results = client.search(index="products", body=body)
        return {"status": "success", "products": results.get("hits", {}).get("hits", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}
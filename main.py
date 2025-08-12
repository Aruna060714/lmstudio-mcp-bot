from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
from pydantic import BaseModel
import uvicorn, logging
from typing import Dict
from supabase_tool import supabase
from opensearch_tool import client as opensearch_client
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
class MCPRequest(BaseModel):
    tool: str
    args: Dict[str, str]
@app.post("/mcp/call")
async def mcp_call(request: Request):
    raw_body = await request.body()
    logger.info(f"Raw incoming body: {raw_body.decode(errors='ignore')}")
    try:
        parsed = MCPRequest.parse_raw(raw_body)
    except Exception as e:
        logger.error(f"Failed to parse request body: {e}")
        raise HTTPException(status_code=422, detail=f"Invalid request body: {e}")
    tool, args = parsed.tool, parsed.args
    if tool == "fetch_product_by_code":
        try:
            code = args.get("code", "").strip()
            if not code:
                raise HTTPException(status_code=400, detail="Missing 'code' in arguments")
            all_products = supabase.table("products_new2").select("*").execute()
            logger.info(f"All products in DB: {[(p.get('barcode'), p.get('ref')) for p in all_products.data]}")
            response = supabase.table("products_new2") \
                .select("id, title, barcode, ref, image") \
                .or_(f"barcode.eq.{code},ref.eq.{code}") \
                .execute()
            if not response.data:
                return {
                    "status": "not_found",
                    "debug": {
                        "searched_code": code,
                        "available_barcodes": [p.get('barcode') for p in all_products.data],
                        "available_refs": [p.get('ref') for p in all_products.data]
                    }
                }
            product = response.data[0]
            return {"status": "success", "product": {k: product.get(k) for k in ["id", "title", "barcode", "ref", "image"]}}
        except Exception as e:
            logger.error(f"Error in fetch_product_by_code: {e}")
            return {"status": "error", "message": str(e)}
    elif tool == "search_products":
        try:
            query = args.get("query", "").strip()
            if not query:
                raise HTTPException(status_code=400, detail="Missing 'query' in arguments")
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "image", "price", "description"],
                        "fuzziness": "AUTO"
                    }
                }
            }
            response = opensearch_client.search(index="products", body=search_body, size=10)
            hits = response.get("hits", {}).get("hits", [])
            if not hits:
                return {
                    "status": "not_found",
                    "debug": {
                        "searched_query": query,
                        "total_hits": response.get("hits", {}).get("total", {}).get("value", 0)
                    }
                }
            products = [
                {**{k: hit["_source"].get(k) for k in ["id", "title","image", "description", "rate"]},
                 "score": hit["_score"],
                 "description": hit["_source"].get("description", "N/A"),
                 "rate": hit["_source"].get("rate", "N/A")}
                for hit in hits
            ]
            return {"status": "success", "products": products, "total": response.get("hits", {}).get("total", {}).get("value", 0)}
        except Exception as e:
            logger.error(f"Error in search_products: {e}")
            return {"status": "error", "message": str(e)}
    else:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")
@app.get("/")
async def health_check():
    return {"status": "running", "endpoints": ["POST /mcp/call"]}
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
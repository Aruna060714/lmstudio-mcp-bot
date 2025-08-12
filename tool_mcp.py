from dotenv import load_dotenv
import requests, logging, sys
load_dotenv()
logging.basicConfig(level=logging.INFO)
def run_tests(title, tool, test_cases, result_key):
    print("\n" + "="*40)
    print(f"{title.upper()} RESULTS")
    print("="*40)
    all_passed = True
    for case in test_cases:
        print(f"\nSearching by {case['type']}: {case['input']}")
        try:
            resp = requests.post("http://localhost:8000/mcp/call",
                                 json={"tool": tool, "args": {case['type']: case['input']}},
                                 timeout=10)
            data = resp.json()
            if resp.status_code != 200:
                print(f" Error: HTTP {resp.status_code}"); all_passed = False; continue
            if data.get("status") == "not_found":
                print(" Product not found" if tool == "fetch_product_by_code" else " No products found")
                all_passed = False; continue
            if data.get("status") != "success":
                print(f"API Error: {data.get('message','Unknown error')}"); all_passed = False; continue
            results = data.get(result_key, [])
            if not results:
                print(" Empty product data"); all_passed = False; continue
            if tool == "fetch_product_by_code":
                p = results
                print("Product found:"); 
                print(f"ID: {p.get('id')}\nTitle: {p.get('title')}\nBarcode: {p.get('barcode')}\nReference: {p.get('ref')}\nImage: {p.get('image')}")
            else:
                print(f"Found {len(results)} product(s):")
                for idx, p in enumerate(results, 1):
                    print(f"Product {idx}:")
                    print(f"ID: {p.get('id')}\nTitle: {p.get('title')}\ndescription: {p.get('description','N/A')}\nImage: {p.get('image')}\nScore: {p.get('score')}\nrate: {p.get('rate','N/A')}")
        except Exception as e:
            print(f" {title.split()[0]} failed: {e}"); all_passed = False
    return all_passed
if __name__ == "__main__":
    lookup_passed = run_tests(
        "Product Lookup", "fetch_product_by_code",
        [{"input": "3664142565543", "type": "code"},
         {"input": "22361022", "type": "code"}],
        "product"
    )
    search_passed = run_tests(
        "Product Search", "search_products",
        [{"input": "monitor", "type": "query"},
         {"input": "Samsung", "type": "query"}],
        "products"
    )
    overall_passed = lookup_passed and search_passed
    sys.exit(0 if overall_passed else 1)
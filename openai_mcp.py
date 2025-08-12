from openai import OpenAI
import requests
import json
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)
MODEL_NAME = "qwen2-math-7b-instruct"
MCP_SERVER_NAME = "product-search"
API_URL = "http://localhost:8000/mcp/call"
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_product_by_code",
            "description": "Fetch product details by barcode or reference code from the MCP server.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The barcode or reference code to look up."
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products using a natural language query from the MCP server.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string."
                    }
                },
                "required": ["query"]
            }
        }
    }
]
def main():
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are connected to an MCP server named '{MCP_SERVER_NAME}'. "
                    "When given a query, call the appropriate MCP tool and return the result."
                )
            },
            {
                "role": "user",
                "content": "Find product details for barcode 3664142565543"
            }
        ]
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )
        response_message = resp.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                print(f"\nTool Call Detected: {tool_name} with args {tool_args}")
                payload = {"tool": tool_name, "args": tool_args}
                try:
                    api_response = requests.post(API_URL, json=payload, timeout=10)
                    api_response.raise_for_status()
                    tool_result = api_response.json()
                    print("\nAPI Response:\n", tool_result)
                except requests.exceptions.RequestException as e:
                    print("\nAPI Error:\n", {"status": "error", "message": str(e)})
    except Exception as e:
        print("Error while querying MCP server:", e)
if __name__ == "__main__":
    main()
# Product Search System

A comprehensive product search system that integrates with Supabase for product data storage and OpenSearch for efficient searching capabilities.

## Features

- **Product Lookup**: Fetch product details by barcode or reference code  
- **Product Search**: Search products using natural language queries  
- **API Integration**: RESTful API endpoints for both operations  
- **Testing Suite**: Built-in testing tool to verify functionality  
- **OpenAI Integration**: Optional integration with OpenAI for natural language processing  

## System Components

| Component               | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `main.py`               | FastAPI-based server handling product lookup and search requests            |
| `tool_mcp.py`           | Automated testing of product lookup and search functionality                |
| `opensearch_tool.py`    | Handles product search operations with fuzzy matching                       |
| `supabase_tool.py`      | Manages connection to Supabase database for product data                    |
| `mcp_instance.py`       | FastMCP implementation for the product search system                        |
| `openai_mcp.py`         | Optional component for natural language processing of queries               |

## Installation
1. Install dependencies:

    pip install fastapi uvicorn supabase opensearch-py python-dotenv requests openai
## Usage
|    Command	        |      Description                  |
|-----------------------|-----------------------------------|
|python main.py	        |Start the main API server          |
|python tool_mcp.py	    |Run test suite                     |
|python mcp_server.py	|Launch MCP server (port 8001)      |
|python openai_mcp.py   |(tested with LM Studio)            |

## Example Workflow:
1. The script sends a sample query: "Find product details for barcode 3664142565543"
2. The LLM determines this requires a fetch_product_by_code operation
3. The system calls your MCP server and returns:
    - Detected tool call
    - API response with product details

# API Documentation
**Endpoint**  **Method**	  

/mcp/call	-    POST	 

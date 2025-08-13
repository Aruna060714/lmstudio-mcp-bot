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
1. Create and activate a virtual environment
- From your project folder, run:
**python -m venv venv**
    python – the Python interpreter installed on your system
    -m venv – tells Python to run the built-in virtual environment module
    venv – the folder name where the virtual environment will be stored (you can name it anything, but venv is common)
- Activate the Virtual Environment :
**venv\Scripts\activate**
- Verify Activation
 If the environment is activated, your terminal prompt will show (venv) at the start:
**(venv) D:\SB\product_search_bot>**
- Deactivate the Virtual Environment
  When done, run:
**deactivate**
2. Install dependencies:
    pip install fastapi uvicorn supabase opensearch-py python-dotenv requests openai
3. Set up .env file
Create a .env file in the project root using the template below.
.env Template
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key

# OpenSearch Configuration
OPENSEARCH_HOST=your_opensearch_host
OPENSEARCH_PORT=9200
OPENSEARCH_USER=your_username
OPENSEARCH_PASS=your_password
## LM Studio Model Details
This system is tested with **Qwen2-Math-7B-Instruct** model in LM Studio.
    You can replace it with any other chat/instruction-tuned model in LM Studio by updating the MODEL_NAME in openai_mcp.py.
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
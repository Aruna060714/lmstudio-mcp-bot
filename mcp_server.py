from dotenv import load_dotenv
load_dotenv()
from mcp_instance import mcp
import supabase_tool
import opensearch_tool
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8001)
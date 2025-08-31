from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location:str)->str:
    """
    Get weather for specific location
    """

    return f"It's always sunny in {location}"

if __name__ == "__main__":
    mcp.run(transport="sse")
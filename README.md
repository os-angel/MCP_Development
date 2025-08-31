# Tutorial: MCP Servers with FastMCP

This project is a comprehensive tutorial on how to create **Model Context Protocol (MCP) Servers** using the `FastMCP` library. Here you'll find practical examples of how to build MCP servers that can integrate with AI tools like Claude.

## What is MCP?

The **Model Context Protocol (MCP)** is an open protocol that allows AI applications to securely access external data and tools. MCP servers act as bridges between AI models and external resources like databases, APIs, file systems, etc.

## Transport Methods: STDIO vs SSE

### STDIO (Standard Input/Output)
- **What is it?**: Uses the system's standard input and output for communication
- **How it works**: Client and server exchange JSON messages through stdin/stdout
- **Advantages**: 
  - Simple to implement
  - Ideal for command-line tools
  - Lower latency for simple operations
- **Disadvantages**: 
  - Synchronous communication
  - Only works within the same process or child processes
- **Typical usage**: Local tools, scripts, direct integrations

```python
# Example: Math Server using STDIO
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### SSE (Server-Sent Events)
- **What is it?**: Web protocol that allows the server to send real-time updates to the client
- **How it works**: Establishes a persistent HTTP connection for data streaming
- **Advantages**:
  - Asynchronous communication
  - Support for multiple simultaneous clients
  - Ideal for web applications
  - Allows streaming of long responses
- **Disadvantages**:
  - More complex to configure
  - Requires HTTP server
  - Higher network overhead
- **Typical usage**: Web applications, real-time dashboards, multiple clients

```python
# Example: Weather Server using SSE
if __name__ == "__main__":
    mcp.run(transport="sse")
```

## Project Setup

### Prerequisites
- Python 3.13+
- uv (recommended) or pip

### Installation

```bash
# Clone the repository
git clone <your-repository>
cd Project2

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or if using uv:
uv sync
```

### Environment Variables Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
LANGCHAIN_API_KEY=your_langchain_key_here
LANGCHAIN_TRACING=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=mcp-test
```

## Included MCP Servers

### 1. Math Server (`servers/math_server.py`)

A simple server that provides basic mathematical operations using **STDIO**:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")  # ← STDIO Transport
```

**Features:**
- Tools: `add()` and `multiply()`
- Transport: **STDIO** - Ideal for direct integration with Claude Desktop
- Synchronous communication through stdin/stdout

### 2. Weather Server (`servers/weather_server.py`)

A server that simulates a weather service using **SSE**:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Gets weather for a specific location"""
    return f"It's always sunny in {location}"

if __name__ == "__main__":
    mcp.run(transport="sse")  # ← SSE Transport
```

**Features:**
- Tools: `get_weather()`
- Transport: **SSE** - Allows multiple clients and asynchronous communication
- Async function for non-blocking operations

## When to Use Each Transport

| Criteria | STDIO | SSE |
|----------|-------|-----|
| **Complexity** | Low | Medium |
| **Multiple clients** | No | Yes |
| **Communication** | Synchronous | Asynchronous |
| **Claude Desktop Integration** | Native | Requires additional configuration |
| **Web applications** | Not recommended | Ideal |
| **Data streaming** | Limited | Excellent |
| **Latency** | Low | Medium |

## How to Run the Servers

### Math Server (STDIO)
```bash
cd servers
python math_server.py
# Runs and waits for stdin input
```

### Weather Server (SSE)
```bash
cd servers
python weather_server.py
# Runs as HTTP server, accessible via web
```

## Claude Desktop Integration

To use these servers with Claude Desktop, add the following configuration to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "math": {
      "command": "python",
      "args": ["path/to/servers/math_server.py"],
      "env": {}
    },
    "weather": {
      "command": "python",
      "args": ["path/to/servers/weather_server.py"],
      "env": {}
    }
  }
}
```

**Note**: Claude Desktop works best with STDIO servers for direct integration.

## Key MCP Concepts

### 1. Tools
Tools are functions that the AI model can call. They are defined using the `@mcp.tool()` decorator.

### 2. Transports
- **stdio**: Communication through standard input/output
- **SSE**: Server-Sent Events for web communication

### 3. FastMCP
`FastMCP` is a library that simplifies MCP server creation, similar to how FastAPI simplifies API creation.

## Project Structure

```
Project2/
├── .env                    # Environment variables
├── .gitignore             # Git ignored files
├── .python-version        # Python version
├── README.md              # This file
├── main.py                # Main entry point
├── pyproject.toml         # Project configuration
├── uv.lock                # Dependency lock file
├── servers/               # MCP servers
│   ├── __init__.py
│   ├── math_server.py     # STDIO server - math operations
│   └── weather_server.py  # SSE server - weather service
└── .venv/                 # Virtual environment
```

## Dependencies

- `langchain-mcp-adapters`: Adapters for integrating MCP with LangChain
- `langchain[openai]`: LangChain with OpenAI support
- `langgraph`: Framework for building graph-based applications
- `python-dotenv`: Environment variable management

## Next Steps

1. **Experiment** with both transport types
2. **Compare** performance between STDIO and SSE
3. **Create** more complex tools
4. **Implement** transport-specific error handling
5. **Explore** web application integration using SSE

## Additional Resources

- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP on GitHub](https://github.com/jlowin/fastmcp)
- [Claude Desktop Setup](https://claude.ai/docs)
- [Server-Sent Events MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## Contributions

Contributions are welcome! If you have ideas for new MCP servers or improvements, feel free to create an issue or pull request.

---

**Note**: This is an educational project designed to learn about MCP. The examples demonstrate practical differences between STDIO and SSE for different use cases.
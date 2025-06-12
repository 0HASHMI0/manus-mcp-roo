# Unified MCP Server with Tools

## Project Description

This project implements a unified MCP (Meta-Controller Protocol) server designed to expose a collection of diverse tools to frontend AI programs. The server acts as a central gateway, allowing AI agents to access and utilize various functionalities (such as file operations, code execution, web search, document editing, etc.) through a standardized interface. This architecture promotes modularity and allows for easy integration of new tools.

## Project Structure
```
.
├── app
│   └── mcp
│       ├── __init__.py  # Initializes the mcp module
│       └── server.py  # Contains the MCPServer class for unifying and exposing tools. It handles request routing, tool execution, and response generation.
│   └── tool
│       ├── __init__.py  # Initializes the tool module
│       ├── ask_human.py  # Tool for asking a human for input.
│       ├── base.py  # Base class from which all tools inherit, defining a common interface.
│       ├── bash.py  # Tool for executing bash commands in the terminal.
│       ├── browser_use_tool.py  # Tool for automating web browser interactions.
│       ├── chart_visualization  # Directory containing tools related to chart visualization.
│       │   ├── README.md  # Documentation for chart visualization tools.
│       │   ├── README_zh.md # Chinese documentation for chart visualization tools.
│       │   ├── __init__.py # Initializes the chart_visualization submodule.
│       │   ├── chart_prepare.py # Tool for preparing data for chart visualization.
│       │   ├── data_visualization.py # Tool for generating data visualizations.
│       │   ├── package-lock.json # npm package lock file for chart visualization frontend.
│       │   ├── package.json # npm package file for chart visualization frontend.
│       │   ├── python_execute.py # (Likely a tool for executing Python code related to charts)
│       │   ├── src # Source files for chart visualization frontend.
│       │   │   └── chartVisualize.ts # TypeScript file for chart visualization.
│       │   ├── test # Test files for chart visualization tools.
│       │   │   ├── chart_demo.py
│       │   │   └── report_demo.py
│       │   └── tsconfig.json # TypeScript configuration file.
│       ├── create_chat_completion.py  # Tool for interacting with chat completion models.
│       ├── excel_editor_tool.py  # Tool for editing Excel files (reading sheets, writing cells, creating sheets).
│       ├── file_operators.py  # Tool for performing file system operations like reading, writing, and deleting files.
│       ├── mcp.py  # (Likely a tool or component related to MCP internal operations)
│       ├── pdf_editor_tool.py  # Tool for editing PDF files (reading text, merging PDFs).
│       ├── planning.py  # Tool for creating and managing task plans.
│       ├── python_execute.py  # Tool for executing arbitrary Python code snippets.
│       ├── search  # Directory containing various search tools.
│       │   ├── __init__.py # Initializes the search submodule.
│       │   ├── baidu_search.py # Tool for searching using Baidu.
│       │   ├── base.py # Base class for search tools.
│       │   ├── bing_search.py # Tool for searching using Bing.
│       │   ├── duckduckgo_search.py # Tool for searching using DuckDuckGo.
│       │   └── google_search.py # Tool for searching using Google.
│       ├── str_replace_editor.py  # Tool for performing string replacements within files.
│       ├── terminate.py  # Tool for terminating processes or the current operation.
│       ├── tool_collection.py  # Manages the collection of all available tools, providing a central registry and access point.
│       └── web_search.py  # Tool for performing general web searches.
├── requirements.txt  # Lists all the necessary Python dependencies for the project, including libraries used by the tools.
└── run_mcp_server.py  # The main entry point script to initialize and run the MCP server.
```
## Setup and Running

To set up and run the unified MCP server, follow these steps:

1.  **Clone the repository (if applicable):** If this project is hosted in a repository, clone it to your local machine.
2.  **Install dependencies:** Navigate to the project's root directory in your terminal and install the required Python packages using pip:
```
bash
    pip install -r requirements.txt
    
```
3.  **Run the server:** Execute the `run_mcp_server.py` script to start the server:
```
bash
    python run_mcp_server.py
    
```
The server will start listening for incoming MCP requests. The default transport method might be standard input/output (stdio), but you can check the `run_mcp_server.py` file for available command-line arguments to configure the transport (e.g., for HTTP).

Once the server is running, frontend AI programs configured to communicate via MCP can send requests to utilize the exposed tools.
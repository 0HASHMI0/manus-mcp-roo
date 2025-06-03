# MANUS MCP for Roo - Installation Guide

## Prerequisites
- Python 3.11+
- Node.js 18+ (for visualization tools)
- Git

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/0HASHMI0/manus-mcp-roo.git
cd manus-mcp-roo
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Copy the example config file:
```bash
cp config/config.example.toml config/config.toml
```

Edit `config/config.toml` to set:
- API keys for search engines
- Default language/country for searches
- Tool-specific configurations

### 4. Install Visualization Dependencies (Optional)
```bash
cd app/tool/chart_visualization
npm install
```

### 5. Start the MCP Server
```bash
python run_mcp_server.py
```

### 6. Integrate with Roo CLI
Add this to your Roo CLI configuration:
```yaml
mcp_servers:
  - name: manus-mcp
    type: stdio
    command: python run_mcp_server.py
    working_dir: /path/to/manus-mcp-roo
```

## Docker Installation
```bash
docker build -t manus-mcp-roo .
docker run -p 8000:8000 manus-mcp-roo
```

## Verification
Test the installation:
```bash
python -m app.tool.web_search --query "test search"
```

## Troubleshooting
- **Missing dependencies**: Run `pip freeze` to verify all packages installed
- **Permission issues**: Use virtual environments (`python -m venv venv`)
- **Search engine failures**: Verify API keys in config.toml

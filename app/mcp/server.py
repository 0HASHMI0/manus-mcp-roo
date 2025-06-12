import logging
import sys


logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stderr)])

import argparse
import asyncio
import atexit
import jsonpickle
from inspect import Parameter, Signature
from typing import Any, Dict, Optional
from app.tool.base import ToolResult, ToolFailure
from mcp.server.fastmcp import FastMCP

from app.logger import logger
from app.tool.tool_collection import get_all_tools
from app.tool.base import BaseTool
class MCPServer:
    """MCP Server implementation with tool registration and management."""

    # Define the path prefix for tool exposure
    TOOL_PATH_PREFIX = "tool"

    def __init__(self, name: str = "openmanus"):
        self.server = FastMCP(name)
        self.tools: Dict[str, BaseTool] = {}
        self._load_tools() # Load tools upon initialization
    def register_tool(self, tool, method_name: Optional[str] = None) -> None:
        """Register a tool with parameter validation and documentation."""
        tool_name = method_name or tool.name
        tool_param = tool.to_param()
        tool_function = tool_param["function"]

        # Define the async function to be registered
        async def tool_method(**kwargs):
            logger.info(f"Executing {tool_name}: {kwargs}")
            try:
                # Validate parameters against schema before execution
                self._validate_parameters(tool_name, kwargs, tool_method._parameter_schema)
                result = await tool.execute(**kwargs)
                logger.info(f"Result of {tool_name}: {result}")
                # Return the result directly. FastMCP handles JSON serialization if needed.
                return result
            except ValueError as ve:
                logger.error(f"Parameter validation error for tool {tool_name}: {ve}")
                return {"error": f"Parameter validation error: {ve}"}
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {e}")
                return {"error": str(e)}


        # Set method metadata for FastMCP registration
        # Set method metadata
        tool_method.__name__ = tool_name
        tool_method.__doc__ = self._build_docstring(tool_function)
        tool_method.__signature__ = self._build_signature(tool_function)

        # Store parameter schema (important for tools that access it programmatically)
        param_props = tool_function.get("parameters", {}).get("properties", {})
        required_params = tool_function.get("parameters", {}).get("required", [])
        tool_method._parameter_schema = {
            param_name: {
                "description": param_details.get("description", ""),
                "type": param_details.get("type", "any"),
                "required": param_name in required_params,
            }
            for param_name, param_details in param_props.items()
        }

        # Register with server
        self.server.tool(f"{self.TOOL_PATH_PREFIX}/{tool_name}")(tool_method)
        logger.info(f"Registered tool: {tool_name}")

    def _build_docstring(self, tool_function: dict) -> str:
        """Build a formatted docstring from tool function metadata."""
        description = tool_function.get("description", "")
        param_props = tool_function.get("parameters", {}).get("properties", {})
        required_params = tool_function.get("parameters", {}).get("required", [])

        # Build docstring (match original format)
        docstring = description
        if param_props:
            docstring += "\n\nParameters:\n"
            for param_name, param_details in param_props.items():
                required_str = (
                    "(required)" if param_name in required_params else "(optional)"
                )
                param_type = param_details.get("type", "any")
                param_desc = param_details.get("description", "")
                docstring += (
                    f"    {param_name} ({param_type}) {required_str}: {param_desc}\n"
                )

        return docstring

    def _build_signature(self, tool_function: dict) -> Signature:
        """Build a function signature from tool function metadata."""
        param_props = tool_function.get("parameters", {}).get("properties", {})
        required_params = tool_function.get("parameters", {}).get("required", [])

        parameters = []

        # Follow original type mapping
        for param_name, param_details in param_props.items():
            param_type = param_details.get("type", "")
            default = Parameter.empty if param_name in required_params else None

            # Map JSON Schema types to Python types (same as original)
            annotation = Any
            if param_type == "string":
                annotation = str
            elif param_type == "integer":
                annotation = int
            elif param_type == "number":
                annotation = float
            elif param_type == "boolean":
                annotation = bool
            elif param_type == "object":
                annotation = dict
            elif param_type == "array":
                annotation = list

            # Create parameter with same structure as original
            param = Parameter(
                name=param_name,
                kind=Parameter.KEYWORD_ONLY,
                default=default,
                annotation=annotation,
            )
            parameters.append(param)

        return Signature(parameters=parameters)

    def _validate_parameters(self, tool_name: str, params: Dict[str, Any], schema: Dict[str, Any]):
        """Validate parameters against the tool's parameter schema."""
        required_params = [name for name, details in schema.items() if details.get("required")]
        missing_required = [param for param in required_params if param not in params]
        if missing_required:
            raise ValueError(f"Missing required parameters: {', '.join(missing_required)}")

        # Basic type checking (can be expanded for more complex schemas)
        for param_name, param_value in params.items():
            if param_name in schema:
                expected_type = schema[param_name].get("type")
                # Add type checking logic here based on expected_type if needed

    async def cleanup(self) -> None:
        """Clean up server resources."""
        logger.info("Cleaning up resources")
        # Follow original cleanup logic - only clean browser tool
        if "browser" in self.tools and hasattr(self.tools["browser"], "cleanup"):
            await self.tools["browser"].cleanup()

    def _load_tools(self) -> None:
        """Load all tools using the tool collection."""
        self.tools = get_all_tools()

    def register_all_tools(self) -> None:
        """Register all tools with the server."""
        for tool_name, tool in self.tools.items():
            self.register_tool(tool)

    def run(self, transport: str = "stdio") -> None:
        """Run the MCP server."""
        # Register all tools
        self.register_all_tools()

        # Register cleanup function (match original behavior)
        atexit.register(lambda: asyncio.run(self.cleanup()))

        # Start server (with same logging as original)
        logger.info(f"Starting OpenManus server ({transport} mode)")
        self.server.run(transport=transport)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="OpenManus MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio"],
        default="stdio",
        help="Communication method: stdio or http (default: stdio)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Create and run server (maintaining original flow)
    server = MCPServer()
    server.run(transport=args.transport)

"""Collection classes for managing multiple tools."""
from typing import Any, Dict, List

# Import all your tool classes here
from app.tool.ask_human import AskHumanTool
from app.tool.bash import BashTool
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.file_operators import FileOperatorsTool
from app.tool.chart_visualization.chart_prepare import ChartPrepareTool
from app.tool.chart_visualization.data_visualization import DataVisualizationTool
from app.tool.search.baidu_search import BaiduSearchTool
from app.tool.search.bing_search import BingSearchTool
from app.tool.planning import PlanningTool
from app.tool.python_execute import PythonExecuteTool
from app.tool.str_replace_editor import StrReplaceEditorTool
from app.tool.pdf_editor_tool import PDFEditorTool
from app.tool.excel_editor_tool import ExcelEditorTool
from app.tool.terminate import TerminateTool
from app.tool.web_search import WebSearchTool
from app.exceptions import ToolError
from app.logger import logger
from app.tool.base import BaseTool, ToolFailure, ToolResult


class ToolCollection:
    """A collection of defined tools."""

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, *tools: BaseTool):
        # Automatically register all available tools
        available_tools = [
            AskHumanTool(),
            BashTool(),
            BrowserUseTool(),
            ChartPrepareTool(),
            DataVisualizationTool(),
            FileOperatorsTool(),
            BaiduSearchTool(),
            BingSearchTool(),
            PlanningTool(),
            PythonExecuteTool(),
            PDFEditorTool(),
            ExcelEditorTool(),
            StrReplaceEditorTool(),
            # TerminateTool(), # TerminateTool might be handled differently, not exposed via MCP
            WebSearchTool(),
            # Add other tool classes here as you implement them
        ]

        self.tools = tools if tools else tuple(available_tools)
        self.tool_map = {tool.name: tool for tool in tools}

    def __iter__(self):
        return iter(self.tools)

    def to_params(self) -> List[Dict[str, Any]]:
        return [tool.to_param() for tool in self.tools]

    async def execute(
        self, *, name: str, tool_input: Dict[str, Any] = None
    ) -> ToolResult:
        tool = self.tool_map.get(name)
        if not tool:
            return ToolFailure(error=f"Tool {name} is invalid")
        try:
            result = await tool.execute(**tool_input if tool_input is not None else {})
            return result
        except ToolError as e:
            return ToolFailure(error=e.message)

    async def execute_all(self) -> List[ToolResult]:
        """Execute all tools in the collection sequentially."""
        results = []
        for tool in self.tools:
            try:
                result = await tool()
                results.append(result)
            except ToolError as e:
                results.append(ToolFailure(error=e.message))
        return results

    def get_tool(self, name: str) -> BaseTool:
        return self.tool_map.get(name)

    def add_tool(self, tool: BaseTool):
        """Add a single tool to the collection.

        If a tool with the same name already exists, it will be skipped and a warning will be logged.
        """
        if tool.name in self.tool_map:
            logger.warning(f"Tool {tool.name} already exists in collection, skipping")
            return self

        self.tools += (tool,)
        self.tool_map[tool.name] = tool
        return self

    def add_tools(self, *tools: BaseTool):
        """Add multiple tools to the collection.

        If any tool has a name conflict with an existing tool, it will be skipped and a warning will be logged.
        """
        for tool in tools:
            self.add_tool(tool)
        return self

"""MCP (Model Context Protocol) gateway."""

from free_agent.mcp.client import MCPClient, MCPTool, MCP_PROTOCOL_VERSION
from free_agent.mcp.gateway import MCPGateway
from free_agent.mcp.transports import HttpTransport, SseTransport, StdioTransport

__all__ = [
    "MCPGateway",
    "MCPClient",
    "MCPTool",
    "MCP_PROTOCOL_VERSION",
    "StdioTransport",
    "HttpTransport",
    "SseTransport",
]

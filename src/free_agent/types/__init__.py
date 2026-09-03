"""Core type definitions."""

from free_agent.types.messages import (
    AssistantMessage,
    Message,
    MessageType,
    ResultMessage,
    SystemMessage,
    ToolCall,
    ToolResult,
    Usage,
    UserMessage,
    assistant_message,
    result_message,
    system_message,
    user_message,
)
from free_agent.types.options import FreeAgentOptions, MCPServerConfig, PluginRef

__all__ = [
    "Message",
    "MessageType",
    "ToolCall",
    "ToolResult",
    "Usage",
    "SystemMessage",
    "AssistantMessage",
    "UserMessage",
    "ResultMessage",
    "system_message",
    "assistant_message",
    "user_message",
    "result_message",
    "FreeAgentOptions",
    "MCPServerConfig",
    "PluginRef",
]

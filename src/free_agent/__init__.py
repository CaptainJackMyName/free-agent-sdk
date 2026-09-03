"""Free-Agent-SDK — an open-source, model-agnostic autonomous Agent SDK.

Quick start::

    import asyncio
    from free_agent import FreeAgentOptions, query
    from free_agent.llm import OpenAICompatibleProvider

    options = FreeAgentOptions(
        llm=OpenAICompatibleProvider(
            base_url="https://api.openai.com/v1",
            api_key="sk-...",
            model="gpt-4o-mini",
        ),
        allowed_tools=["Read", "Write", "Bash"],
    )

    async def main() -> None:
        async for message in query("Review src/", options=options):
            print(message.type, message.text)

    asyncio.run(main())
"""

from __future__ import annotations

from free_agent.client import FreeAgentClient, query
from free_agent.loop.engine import AgentLoop
from free_agent.subagents.definition import AgentDefinition
from free_agent.tools import Tool, tool
from free_agent.types import (
    AssistantMessage,
    FreeAgentOptions,
    Message,
    MessageType,
    ResultMessage,
    SystemMessage,
    ToolCall,
    ToolResult,
    Usage,
    UserMessage,
)

__version__ = "0.1.0"

__all__ = [
    "query",
    "FreeAgentClient",
    "FreeAgentOptions",
    "AgentLoop",
    "AgentDefinition",
    "Tool",
    "tool",
    "Message",
    "MessageType",
    "ToolCall",
    "ToolResult",
    "Usage",
    "SystemMessage",
    "AssistantMessage",
    "UserMessage",
    "ResultMessage",
    "__version__",
]

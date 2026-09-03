"""Span name constants following the ``free_agent_sdk.<layer>.<op>`` convention."""

from __future__ import annotations

LOOP_TURN = "free_agent_sdk.loop.turn"
LLM_REQUEST = "free_agent_sdk.llm.request"
TOOL_EXECUTE = "free_agent_sdk.tool.execute"
HOOK_RUN = "free_agent_sdk.hook.run"
MCP_CALL = "free_agent_sdk.mcp.call"
SUBAGENT_RUN = "free_agent_sdk.subagent.run"
SKILL_EXECUTE = "free_agent_sdk.skill.execute"

__all__ = [
    "LOOP_TURN",
    "LLM_REQUEST",
    "TOOL_EXECUTE",
    "HOOK_RUN",
    "MCP_CALL",
    "SUBAGENT_RUN",
    "SKILL_EXECUTE",
]

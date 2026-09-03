"""Agent Loop engine — the ReAct think/act/observe controller."""

from __future__ import annotations

import logging
from typing import Any, AsyncIterator, Dict, List, Optional

from free_agent.hooks.events import HookContext, HookEvent
from free_agent.hooks.registry import HookRegistry
from free_agent.loop.context import SessionContext
from free_agent.loop.turn import Turn
from free_agent.permissions.policy import PermissionManager
from free_agent.tools.base import Tool
from free_agent.tools.builtin import BUILTIN_TOOLS
from free_agent.tools.registry import ToolRegistry
from free_agent.tracing.spans import LOOP_TURN
from free_agent.tracing.tracer import get_tracer
from free_agent.types.messages import Message
from free_agent.types.options import FreeAgentOptions

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are a capable autonomous agent. Use the provided tools to accomplish "
    "the user's request, reasoning step by step and acting when needed."
)


class AgentLoop:
    """The core ReAct execution loop."""

    def __init__(self, options: FreeAgentOptions) -> None:
        if options.llm is None:
            raise ValueError("FreeAgentOptions.llm is required to run an agent.")
        self.options = options
        self.llm = options.llm
        self.context = SessionContext(options)
        self.hooks = HookRegistry.from_config(options.hooks)
        self.permissions = PermissionManager(options.permission_policy)
        self.tracer = get_tracer()

        self.registry = ToolRegistry()
        self._mcp_gateway = None
        self._skill_tool = None
        self._agent_tool = None

    # -- lifecycle -----------------------------------------------------------
    async def setup(self) -> None:
        """Assemble the tool registry (builtins + MCP + skills + subagents)."""
        self._register_builtins()

        if self.options.mcp_servers:
            await self._setup_mcp()

        if self.options.skills:
            self._setup_skill_tool()

        if self.options.agents:
            self._setup_agent_tool()

    async def aclose(self) -> None:
        if self._mcp_gateway is not None:
            await self._mcp_gateway.close_all()

    # -- tool assembly -------------------------------------------------------
    def _register_builtins(self) -> None:
        allowed = self.options.allowed_tools
        for builtin in BUILTIN_TOOLS:
            if _matches_any(builtin.name, allowed):
                self.registry.register(builtin)

    async def _setup_mcp(self) -> None:
        from free_agent.mcp.gateway import MCPGateway

        self._mcp_gateway = MCPGateway()
        for name, config in self.options.normalize_mcp_servers().items():
            await self._mcp_gateway.connect(name, config)
            for tool in await self._mcp_gateway.list_tools(name):
                full_name = f"mcp__{name}__{tool.name}"
                if not _matches_any(full_name, self.options.allowed_tools):
                    continue
                self.registry.register(
                    Tool(
                        name=full_name,
                        description=tool.description,
                        handler=tool.invoke,
                        input_schema=tool.input_schema,
                    )
                )

    def _setup_skill_tool(self) -> None:
        from free_agent.skills.executor import SkillExecutor
        from free_agent.skills.loader import SkillLoader

        loader = SkillLoader()
        executor = SkillExecutor(loader=loader, enabled=self.options.skills)
        self._skill_tool = executor.build_tool()
        self.registry.register(self._skill_tool)

    def _setup_agent_tool(self) -> None:
        from free_agent.subagents.orchestrator import SubagentOrchestrator

        orchestrator = SubagentOrchestrator(self.options, parent_llm=self.llm)
        self._agent_tool = orchestrator.build_tool()
        self.registry.register(self._agent_tool)

    # -- main loop -----------------------------------------------------------
    async def run(self, prompt: str) -> AsyncIterator[Message]:
        await self.setup()

        model = self.context.model_name or self.options.model
        yield Message.system(
            subtype="init",
            session_id=self.context.session_id,
            model=model,
            text=self.options.system_prompt or DEFAULT_SYSTEM_PROMPT,
        )
        await self.hooks.dispatch(
            HookEvent.SESSION_START,
            {"prompt": prompt},
            context=HookContext(session_id=self.context.session_id, model=model),
        )

        self.context.append(Message.system(text=self.options.system_prompt or DEFAULT_SYSTEM_PROMPT))
        self.context.append(Message.user(text=prompt))

        llm_kwargs = dict(self.options.extra_llm_kwargs)
        if self.options.temperature is not None:
            llm_kwargs["temperature"] = self.options.temperature

        turn = Turn(
            llm=self.llm,
            tools=self.registry,
            hooks=self.hooks,
            permissions=self.permissions,
            tracer=self.tracer,
            context=self.context,
            llm_kwargs=llm_kwargs,
        )

        while self.context.turn_count < self.options.max_turns:
            self.context.turn_count += 1
            async with self.tracer.span(LOOP_TURN) as span:
                span.set_attribute("loop.turn", self.context.turn_count)
                outcome = await turn.run()

            self.context.append(outcome.assistant)
            yield outcome.assistant

            if outcome.is_final:
                if outcome.result is not None:
                    self.context.append(outcome.result)
                    yield outcome.result
                await self._session_end()
                return

            if outcome.user is not None:
                self.context.append(outcome.user)
                yield outcome.user

        # Reached max turns without a final answer.
        result = Message.result(
            text=f"Stopped after reaching max_turns={self.options.max_turns}",
            usage=self.context.total_usage,
            cost=self.context.total_usage.cost,
            is_error=True,
        )
        self.context.append(result)
        yield result
        await self._session_end()

    async def _session_end(self) -> None:
        await self.hooks.dispatch(
            HookEvent.SESSION_END,
            context=HookContext(session_id=self.context.session_id, model=self.context.model_name),
        )
        await self.aclose()


def _matches_any(name: str, patterns: List[str]) -> bool:
    if not patterns or "*" in patterns:
        return True
    import fnmatch

    return any(fnmatch.fnmatch(name, p) for p in patterns)


__all__ = ["AgentLoop", "DEFAULT_SYSTEM_PROMPT"]

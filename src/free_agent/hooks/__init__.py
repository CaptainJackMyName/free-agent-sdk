"""Hook system."""

from free_agent.hooks.events import HookContext, HookEvent, HookOutput
from free_agent.hooks.matcher import HookMatcher
from free_agent.hooks.registry import Hook, HookRegistry

__all__ = [
    "HookEvent",
    "HookContext",
    "HookOutput",
    "HookMatcher",
    "Hook",
    "HookRegistry",
]

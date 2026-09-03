"""Plugin system."""

from free_agent.plugins.lifecycle import PluginManager
from free_agent.plugins.loader import LoadedPlugin, PluginLoader
from free_agent.plugins.manifest import PluginManifest

__all__ = ["PluginManifest", "PluginLoader", "LoadedPlugin", "PluginManager"]

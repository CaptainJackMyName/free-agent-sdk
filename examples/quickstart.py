"""Quick-start example for the Free-Agent-SDK.

Run with::

    python examples/quickstart.py
"""

import asyncio

from free_agent import FreeAgentOptions, query
from free_agent.llm import OpenAICompatibleProvider
from free_agent.tools import tool


@tool("Add", "Add two integers together.")
async def add(a: int, b: int) -> str:
    return str(a + b)


async def main() -> None:
    options = FreeAgentOptions(
        llm=OpenAICompatibleProvider(
            base_url="https://api.openai.com/v1",
            api_key="sk-...",  # replace with your key
            model="gpt-4o-mini",
        ),
        allowed_tools=["Read", "Write", "Bash", "Grep", "Glob"],
        max_turns=20,
    )

    async for message in query("Summarize the files in the current directory.", options=options):
        if message.type == "system":
            print(f"[system:{message.subtype}] {message.text[:60]}")
        elif message.type == "assistant":
            print(f"[assistant] {message.text[:120]}")
        elif message.type == "user":
            print(f"[user] {len(message.tool_results)} tool result(s)")
        elif message.type == "result":
            print(f"[result] {message.text}")


if __name__ == "__main__":
    asyncio.run(main())

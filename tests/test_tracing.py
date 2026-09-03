"""Tests for the tracing facade."""

from __future__ import annotations

import pytest

from free_agent.tracing import FreeAgentTracer
from free_agent.tracing.spans import LOOP_TURN, LLM_REQUEST, TOOL_EXECUTE
from free_agent.tracing.tracer import _NoopSpan


def test_noop_span_methods_do_not_raise():
    span = _NoopSpan()
    span.set_attribute("k", "v")
    span.add_event("e", {"a": 1})
    span.set_status(None)
    span.record_exception(Exception("x"))
    span.end()


class _FakeSpanContext:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def set_attribute(self, key, value):
        pass


class _FakeTracer:
    def __init__(self):
        self.started = []

    def start_as_current_span(self, name, attributes=None):
        self.started.append(name)
        return _FakeSpanContext()


@pytest.mark.asyncio
async def test_span_uses_custom_tracer():
    fake = _FakeTracer()
    tracer = FreeAgentTracer(tracer=fake)

    async with tracer.span(TOOL_EXECUTE):
        pass

    assert fake.started == [TOOL_EXECUTE]


def test_span_name_constants():
    assert LOOP_TURN == "free_agent_sdk.loop.turn"
    assert LLM_REQUEST == "free_agent_sdk.llm.request"
    assert TOOL_EXECUTE == "free_agent_sdk.tool.execute"


def test_tracer_reports_availability():
    tracer = FreeAgentTracer()
    # With or without OpenTelemetry, the object must be usable.
    assert tracer.available in (True, False)

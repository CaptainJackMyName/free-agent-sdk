# 链路追踪

SDK 采用 [OpenTelemetry](https://opentelemetry.io/) 提供 Traces、Metrics 与 Events。

## Span 命名规范

```
free_agent_sdk.<layer>.<operation>
```

| Span 名称 | 描述 |
|-----------|------|
| `free_agent_sdk.loop.turn` | 单次 Turn 执行 |
| `free_agent_sdk.llm.request` | LLM API 调用 |
| `free_agent_sdk.tool.execute` | 工具执行 |
| `free_agent_sdk.hook.run` | 钩子执行 |
| `free_agent_sdk.mcp.call` | MCP 工具调用 |
| `free_agent_sdk.subagent.run` | 子智能体执行 |
| `free_agent_sdk.skill.execute` | Skill 执行 |

## 配置导出器

```python
from free_agent.tracing import configure_tracing

# 默认使用 ConsoleSpanExporter（本地开发）
configure_tracing()

# 生产环境使用 OTLP 导出器
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
configure_tracing(exporter=OTLPSpanExporter(endpoint="http://localhost:4317"))
```

## 手动使用 Tracer

```python
from free_agent.tracing import FreeAgentTracer

tracer = FreeAgentTracer()

async with tracer.span("free_agent_sdk.custom.operation"):
    tracer.set_attribute("key", "value")
    tracer.add_event("step", {"index": 1})
```

## 无依赖降级

未安装 OpenTelemetry 时，`FreeAgentTracer` 自动退化为 no-op，不影响 SDK 其他功能。

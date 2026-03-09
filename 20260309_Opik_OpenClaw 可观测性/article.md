# OpenClaw + Opik：让 AI Agent 从"黑盒"变"白盒"的可观测性方案

> **导读**：你的 Agent 是不是也经常"神操作"？明明输入没问题，输出却让人摸不着头脑。别急，不是你的 Agent 有问题，是你缺少一套可观测性方案！今天给大家介绍 OpenClaw 官方推出的 Opik 插件，让你的 AI Agent 从"黑盒"变成透明的"白盒"。

---

## 🤔 为什么需要 Agent 可观测性？

先来看几个真实场景：

### 场景一：客服机器人突然"发疯"

```
用户：我的订单什么时候发货？
Agent：亲，您的订单将在 24 小时内发货哦~
用户：订单号是 123456
Agent：[突然开始输出 500 行代码]
```

**问题**：Agent 为什么突然输出代码？是触发了什么工具？调用了哪个 LLM？

### 场景二：成本失控

```
月末账单：$12,345.67
老板：这个月怎么花了这么多钱？
你：我...我也不知道...
```

**问题**：哪些请求最烧钱？哪个模型调用次数最多？有没有异常调用？

### 场景三：性能瓶颈

```
用户：帮我分析一下这份财报
[等待 30 秒后...]
Agent：好的，让我来分析一下...
```

**问题**：时间都花在哪里了？是 LLM 响应慢？还是工具调用卡住了？

---

## 🎯 Opik + OpenClaw：可观测性解决方案

### 什么是 Opik？

[Opik](https://github.com/comet-ml/opik) 是 Comet ML 推出的开源 LLM 和 Agent 可观测性平台，提供：

- **Trace 追踪**：完整记录 Agent 的执行链路
- **Span 分析**：细粒度查看每个步骤的耗时和输入输出
- **成本监控**：实时监控 Token 消耗和费用
- **错误诊断**：快速定位失败原因
- **性能优化**：识别瓶颈并优化

### 什么是 OpenClaw？

[OpenClaw](https://github.com/openclaw/openclaw) 是一个开源的 AI Agent 框架，支持：

- 多 Agent 协作
- 工具调用
- 子 Agent 孵化
- 事件驱动的架构

### 官方插件：@opik/opik-openclaw

Comet ML 官方推出了 OpenClaw 的 Opik 插件，实现**零代码侵入**的可观测性：

```bash
# 安装插件
openclaw plugins install @opik/opik-openclaw

# 配置插件
openclaw opik configure

# 检查状态
openclaw opik status
```

---

## 🏗️ 架构设计

### 系统架构图

![系统架构图](./images/architecture.png)

整个系统的工作流程：

1. **OpenClaw Gateway** 接收用户消息
2. **Agent 执行** 过程中触发各种事件（LLM 调用、工具调用、子 Agent 孵化等）
3. **Opik Plugin** 监听这些事件
4. **Trace & Span** 被发送到 Opik 平台
5. **开发者** 在 Opik Dashboard 查看监控数据

### 事件映射关系

| OpenClaw 事件 | Opik 实体 | 说明 |
|--------------|----------|------|
| `llm_input` | trace + llm span | 开始追踪，记录 LLM 输入 |
| `llm_output` | llm span update/end | 记录输出、Token 和耗时 |
| `before_tool_call` | tool span start | 记录工具名称和输入 |
| `after_tool_call` | tool span update/end | 记录输出/错误和耗时 |
| `subagent_spawning` | subagent span start | 子 Agent 生命周期开始 |
| `subagent_spawned` | subagent span update | 记录子 Agent 元数据 |
| `subagent_ended` | subagent span update/end | 记录子 Agent 结果 |
| `agent_end` | trace finalize | 关闭所有 Span 和 Trace |

---

## 📋 配置指南

### 基础配置

运行配置向导后，会生成如下配置：

```json
{
  "plugins": {
    "entries": {
      "opik-openclaw": {
        "enabled": true,
        "config": {
          "enabled": true,
          "apiKey": "your-api-key",
          "apiUrl": "https://www.comet.com/opik/api",
          "projectName": "openclaw",
          "workspaceName": "default"
        }
      }
    }
  }
}
```

### 环境变量（可选）

插件支持以下环境变量作为配置回退：

```bash
OPIK_API_KEY=your-api-key
OPIK_URL_OVERRIDE=https://your-opik-instance.com
OPIK_PROJECT_NAME=my-project
OPIK_WORKSPACE=my-workspace
```

### 高级配置

```json
{
  "plugins": {
    "entries": {
      "opik-openclaw": {
        "enabled": true,
        "config": {
          "enabled": true,
          "apiKey": "your-api-key",
          "apiUrl": "https://www.comet.com/opik/api",
          "projectName": "openclaw",
          "workspaceName": "default",
          "tags": ["openclaw", "production"],
          "toolResultPersistSanitizeEnabled": false,
          "staleTraceCleanupEnabled": true,
          "staleTraceTimeoutMs": 300000,
          "staleSweepIntervalMs": 60000,
          "flushRetryCount": 2,
          "flushRetryBaseDelayMs": 250
        }
      }
    }
  }
}
```

### 配置项说明

| 配置项 | 默认值 | 说明 |
|-------|-------|------|
| `tags` | `["openclaw"]` | 每个 Trace 的默认标签 |
| `toolResultPersistSanitizeEnabled` | `false` | 是否清理工具结果中的本地图片引用 |
| `staleTraceCleanupEnabled` | `true` | 是否启用过期 Trace 清理 |
| `staleTraceTimeoutMs` | `300000` | Trace 超时时间（5 分钟） |
| `staleSweepIntervalMs` | `60000` | 清理检查间隔（1 分钟） |
| `flushRetryCount` | `2` | 发送失败重试次数 |
| `flushRetryBaseDelayMs` | `250` | 重试基础延迟（指数退避） |

---

## 🔍 Trace 流程图

![Trace 流程图](./images/trace_flow.png)

一个完整的 Trace 生命周期：

```
用户消息
   ↓
[llm_input] ─────────────→ 创建 Trace + LLM Span
   ↓
[before_tool_call] ──────→ 创建 Tool Span
   ↓
[after_tool_call] ───────→ 完成 Tool Span
   ↓
[llm_output] ────────────→ 完成 LLM Span（记录 Token/成本）
   ↓
[agent_end] ─────────────→ 关闭所有 Span + Trace
   ↓
[flush] ─────────────────→ 数据发送到 Opik
```

---

## 💡 实战案例

### 案例一：诊断 Agent 异常

**问题**：Agent 偶尔输出乱码

**排查步骤**：

1. 在 Opik Dashboard 搜索包含错误的 Trace
2. 查看对应 Span 的输入输出
3. 发现是某个工具返回了异常格式
4. 修复工具代码

**代码示例**：

```typescript
// 插件内部自动处理
api.on("after_tool_call", (event) => {
  // 记录工具调用结果
  const toolSpan = active.toolSpans.get(event.toolCallId);
  toolSpan.update({
    output: event.output,
    endTime: Date.now()
  });
  toolSpan.end();
});
```

### 案例二：成本优化

**问题**：月度 LLM 费用超标

**分析步骤**：

1. 在 Opik 中按 `costUsd` 排序所有 Trace
2. 发现 Top 10 的请求都使用了同一模型
3. 检查发现该模型配置过于"豪华"
4. 调整为性价比更高的模型

**监控面板示例**：

```sql
-- Opik 支持 SQL 查询
SELECT
  model,
  SUM(usage_total) as total_tokens,
  SUM(cost_usd) as total_cost
FROM traces
WHERE project = 'openclaw'
GROUP BY model
ORDER BY total_cost DESC
LIMIT 10
```

### 案例三：性能调优

**问题**：Agent 响应慢

**分析步骤**：

1. 查看 Trace 中各 Span 的 `durationMs`
2. 发现 80% 时间花在某个外部 API 调用
3. 添加缓存层优化

**Span 耗时分析**：

| Span 类型 | 平均耗时 | 占比 |
|----------|---------|------|
| LLM | 1200ms | 40% |
| Tool: Search | 1500ms | 50% |
| Tool: Calculator | 50ms | 2% |
| Subagent | 250ms | 8% |

---

## 🛠️ 开发调试

### 本地开发环境

```bash
# 克隆项目
git clone https://github.com/comet-ml/opik-openclaw.git
cd opik-openclaw

# 安装依赖
npm install

# 运行测试
npm run test

# 类型检查
npm run typecheck

# 代码检查
npm run lint

# 冒烟测试
npm run smoke
```

### 测试配置

创建 `.env` 文件：

```bash
# 测试环境配置
OPIK_API_KEY=test-key
OPIK_URL_OVERRIDE=http://localhost:8080
OPIK_PROJECT_NAME=test
```

### 常见问题排查

#### 问题 1：Trace 没有显示

**检查清单**：

```bash
# 1. 检查插件是否启用
openclaw opik status

# 2. 检查 API Key 是否正确
echo $OPIK_API_KEY

# 3. 检查网络连通性
curl -H "Authorization: Bearer $OPIK_API_KEY" \
  https://www.comet.com/opik/api/v1/traces

# 4. 查看 OpenClaw 日志
tail -f ~/.openclaw/logs/gateway.log
```

#### 问题 2：Span 数据不完整

**可能原因**：

- OpenClaw 版本过低（需要 >=2026.3.2）
- Node.js 版本过低（需要 >=22.12.0）
- 插件配置未生效

**解决方案**：

```bash
# 升级 OpenClaw
openclaw upgrade

# 重启 Gateway
openclaw gateway restart

# 重新配置插件
openclaw opik configure
```

---

## 📊 监控面板示例

![监控面板](./images/dashboard.png)

### 关键指标

| 指标 | 说明 | 告警阈值 |
|-----|------|---------|
| `trace_count` | Trace 总数 | - |
| `error_rate` | 错误率 | > 5% |
| `avg_duration` | 平均耗时 | > 5000ms |
| `total_cost` | 总成本 | > 预算 |
| `token_usage` | Token 使用量 | > 限额 |

### 告警配置

```json
{
  "alerts": [
    {
      "name": "高错误率告警",
      "condition": "error_rate > 0.05",
      "window": "5m",
      "notify": ["slack", "email"]
    },
    {
      "name": "成本超预算",
      "condition": "daily_cost > budget",
      "window": "1h",
      "notify": ["slack"]
    }
  ]
}
```

---

## 🚀 最佳实践

### 1. 生产环境配置

```json
{
  "plugins": {
    "allow": ["opik-openclaw"],  // 明确信任插件
    "entries": {
      "opik-openclaw": {
        "enabled": true,
        "config": {
          "enabled": true,
          "tags": ["production", "v1.0"],
          "staleTraceCleanupEnabled": true,
          "staleTraceTimeoutMs": 300000,
          "flushRetryCount": 3,
          "flushRetryBaseDelayMs": 500
        }
      }
    }
  }
}
```

### 2. 多环境隔离

```json
// 开发环境
{
  "projectName": "openclaw-dev",
  "workspaceName": "development"
}

// 生产环境
{
  "projectName": "openclaw-prod",
  "workspaceName": "production"
}
```

### 3. 数据保留策略

```json
{
  "retention": {
    "traces": "30d",
    "spans": "7d",
    "metrics": "90d"
  }
}
```

### 4. 敏感数据处理

```typescript
// 启用工具结果清理
toolResultPersistSanitizeEnabled: true

// 自定义敏感词过滤
sensitivePatterns: [
  /password/i,
  /token/i,
  /secret/i
]
```

---

## 🎓 总结

### 核心价值

| 能力 | 收益 |
|-----|------|
| **全链路追踪** | 看清 Agent 每一步决策 |
| **细粒度监控** | 定位问题到具体 Span |
| **成本透明** | 清楚每一分钱的去向 |
| **性能分析** | 快速识别瓶颈 |
| **错误诊断** | 秒级定位失败原因 |

### 我的建议

1. **尽早接入**：项目初期就集成可观测性，避免后期补坑
2. **合理配置**：根据业务场景调整超时和重试参数
3. **定期复盘**：每周分析 Trace 数据，持续优化
4. **告警分级**：区分 P0/P1/P2 告警，避免告警疲劳

### 未来展望

随着 Agent 技术的普及，可观测性将成为**基础设施**：

- **实时分析**：毫秒级延迟的监控数据
- **智能告警**：AI 预测异常，提前预警
- **自动优化**：基于历史数据自动调整配置
- **跨 Agent 追踪**：多 Agent 协作的全局视角

---

**互动话题**：你在开发 Agent 时遇到过哪些"黑盒"问题？欢迎在评论区分享！

**参考资料**：
- [Opik GitHub](https://github.com/comet-ml/opik)
- [Opik 官方文档](https://www.comet.com/docs/opik)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [opik-openclaw 插件](https://github.com/comet-ml/opik-openclaw)

---

*如果觉得本文有帮助，欢迎点赞、收藏、转发！*

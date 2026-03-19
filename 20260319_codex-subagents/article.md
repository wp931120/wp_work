# 两天 800+ Star，这个仓库让 Codex 变身 136 人开发团队

> 📖 **本文解读内容来源**
>
> - **原始来源**：[awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents)
> - **来源类型**：GitHub 仓库
> - **作者/团队**：VoltAgent
> - **发布时间**：2026-03-17
> - **Star 数**：861+（截至 2026-03-19）
> - **主要语言**：TOML 配置文件

---

OpenAI Codex 刚在 3 月 16 日正式发布了 subagents 功能，隔天就有人整理出了 136 个现成的子代理配置。两天 800 多 star，说明开发者等这东西很久了。

## 一个 Codex，分身 136 个专家

所谓 subagent，其实就是让 AI 编程助手具备"分身术"。你可以把它拆成多个专业角色，每个角色有独立的上下文、专属的提示词、甚至不同的模型配置。

这东西解决了什么痛点？用一个全能 AI 干所有活，看似方便，实则什么都干不精。让它写代码、做架构评审、跑安全审计、写文档——每切换一次任务，上下文就污染一次。到后面它已经忘了最初要干嘛了。

subagent 的设计思路是：既然不可能有一个全知全能的 AI，那就让多个专业 AI 协作。一个当架构师，一个当后端开发，一个当安全审计员，一个当文档工程师。每个只做自己的事，互不干扰。

## 136 个代理，分了 10 个工种

这个仓库把子代理分成 10 类：

**核心开发类**（12 个）：前端、后端、全栈、移动端、API 设计、微服务架构……基本覆盖日常开发。

**语言专家类**（25 个）：Angular、Django、Go、Rust、Kotlin、Swift、TypeScript……几乎每个主流技术栈都有专属代理。

**基础设施类**（15 个）：Docker、K8s、Terraform、Azure、DevOps、SRE……运维同学狂喜。

**质量与安全类**（16 个）：代码审查、渗透测试、安全审计、性能优化、QA 专家……

**数据与 AI 类**（12 个）：数据工程师、ML 工程师、LLM 架构师、Prompt 工程师……

**开发者体验类**（13 个）：构建系统、CLI 工具、文档工程、遗留代码现代化……

**专业领域类**（12 个）：区块链、金融科技、游戏开发、物联网、支付集成……

**商业与产品类**（11 个）：产品经理、项目经理、业务分析师、技术写作……

**元编排类**（12 个）：多代理协调、任务分发、工作流编排……

**研究分析类**（7 个）：市场调研、趋势分析、竞争情报……

## 怎么用？复制粘贴就行

使用方式出奇简单。Codex 支持两种代理存放位置：

```bash
# 全局代理，所有项目可用
~/.codex/agents/

# 项目代理，只在当前项目生效（优先级更高）
.codex/agents/
```

把你需要的 `.toml` 文件复制进去就完事：

```bash
mkdir -p ~/.codex/agents
cp categories/01-core-development/backend-developer.toml ~/.codex/agents/
```

每个配置文件长这样：

```toml
name = "backend-developer"
description = "Server-side expert for scalable APIs"
model = "gpt-5.3-codex-spark"
model_reasoning_effort = "medium"
sandbox_mode = "workspace-write"

[instructions]
text = """
You are a backend developer specializing in...
"""
```

几个字段的作用：

- **model**：指定用哪个模型。深度推理任务（架构评审、安全审计）用 `gpt-5.4`，快速扫描任务用 `gpt-5.3-codex-spark`
- **sandbox_mode**：控制文件访问权限。`read-only` 只读不写，`workspace-write` 可以修改文件
- **instructions**：专属提示词，定义这个代理的专业领域和行为规范

## 一个关键细节：显式委托

Codex 不会自动调用这些子代理。你必须在提示词里明确说"用 xxx 代理做这件事"。

比如代码审查工作流：

```
用 reviewer 代理审查这个分支的正确性、安全性和测试覆盖。
用 docs_researcher 代理验证这个补丁依赖的框架 API。
等两个都跑完，汇总发现的问题并附上文件引用。
```

或者调试工作流：

```
用 code_mapper 追踪问题代码路径，
用 browser_debugger 在浏览器里复现 bug，
最后让 frontend_developer 提出最小化修复方案。
先跑前两个只读代理，再继续。
```

这个设计决策笔者很认同。自动派发看似省事，但实际用起来容易失控——你不知道它背着干了啥。显式委托虽然多敲几个字，但每一步都在你的掌控之中。

## 笔者的判断

**这是 AI 编程工具从"单兵作战"走向"团队协作"的标志。**

早期的 GitHub Copilot 是辅助型工具，帮你补全代码。后来的 Cursor、Windsurf 开始有 agent 能力，可以自主完成任务。但本质上还是一个 AI 干所有事。

subagent 模式把 AI 编程工具推进到了"团队协作"阶段。一个项目经理 AI 协调多个专业 AI，分工明确，互不干扰。这比单纯提升模型能力更有价值——因为现实中软件工程本来就是团队活动，不是单打独斗。

**这个仓库最大的价值是"标准化"。**

136 个配置文件，其实是社区沉淀下来的"如何定义一个专业角色"的最佳实践。后端开发应该关注什么？安全审计应该检查什么？文档工程师应该怎么写？这些配置文件给出了答案。

你可以直接拿来用，也可以参考它们定义自己的团队专属代理。比如你们公司有特定的代码规范，可以在 `instructions` 里加上；你们团队用特定的技术栈，可以克隆一个语言专家代理然后定制。

**一个潜在问题是认知负担。**

136 个代理，光记住它们各自干什么就要花时间。实际使用中，大部分人可能只会用到其中 10-20 个高频代理。仓库里提供了 agent-installer 代理，可以帮你"代理的代理"——让 AI 帮你选代理。有点绕，但确实解决问题。

## 小结

OpenAI Codex 的 subagent 功能刚刚发布三天，社区就有了 136 个现成配置。这说明开发者对这个能力的渴望程度。如果你在用 Codex，花十分钟配置几个常用代理，开发体验会有质的变化。

GitHub 地址：[VoltAgent/awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents)

---

### 参考

- [awesome-codex-subagents GitHub 仓库](https://github.com/VoltAgent/awesome-codex-subagents)
- [OpenAI Codex Subagents 官方文档](https://developers.openai.com/codex/subagents)
- [OpenAI Codex Adds Subagents And Custom Agents](https://letsdatascience.com/news/openai-codex-adds-subagents-and-custom-agents-c3e4196e)
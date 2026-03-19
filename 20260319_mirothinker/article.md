# 开源 Deep Research Agent 新王者：MiroThinker 如何用「交互深度」突破性能天花板

当 OpenAI 的 Deep Research 和 Gemini 的 Deep Research 横扫各大基准测试时，开源社区一直在追问一个问题：我们能不能做出一个同等能力的研究 Agent？

MiroMind AI 给出了答案：**MiroThinker-1.7**，在 BrowseComp-ZH 上拿下开源 SOTA，在 GAIA-Val-165 上突破 82%，用 30B 参数打出了 235B 级别的表现。

## 痛点：Deep Research 的「长链诅咒」

Deep Research 任务有多难？

一个典型的研究问题——比如「分析某公司过去五年的财务状况并预测明年趋势」——需要：

1. 搜索公司财报、新闻报道、分析师观点
2. 抓取网页内容、提取关键数据
3. 用代码处理数据、绘制图表
4. 交叉验证信息来源、发现矛盾
5. 整合成结构化报告

这涉及**几十次工具调用**、**多轮信息整合**、**复杂推理链**。

传统 Agent 的问题：

- **上下文爆炸**：每一步的搜索结果、网页内容都塞进 context，很快撑爆
- **信息遗忘**：走了二十步之后，第一步搜到的关键信息被稀释了
- **轨迹崩坏**：中间某一步出错，后续全部跑偏

## 破局：Interactive Scaling（交互式扩展）

MiroThinker 提出的核心创新：**交互式扩展（Interactive Scaling）**。

过去大家优化 Agent 主要走两条路：
- **Scale Model**：用更大的模型（7B → 70B → 700B）
- **Scale Context**：用更长的上下文（4K → 32K → 128K）

MiroThinker 加了第三维度：**Scale Interaction**——系统性地训练 Agent 处理更深、更频繁的环境交互。

具体来说：

1. **训练阶段**：收集长链任务轨迹（最长 600 步），让模型学会在长时间跨度上保持目标一致性
2. **推理阶段**：利用环境反馈和外部信息来纠正错误、优化轨迹
3. **上下文管理**：Recency-Based Context Retention——只保留最近 K 个工具响应，释放空间给更多推理

这不是简单的「多走几步」，而是**把 Agent-环境交互本身当作一个可扩展的维度来优化**。

## 架构：三大核心工具 + 极简配置

MiroThinker 的工具链设计非常克制：

| 工具 | 功能 | 底层 |
|------|------|------|
| `search_and_scrape_webpage` | Google 搜索 | Serper API |
| `jina_scrape_llm_summary` | 网页抓取 + 内容提取 | Jina Reader + LLM 摘要 |
| `tool-python` | 代码执行 | E2B Sandbox |

三个工具覆盖 Deep Research 的核心需求：**搜索、阅读、计算**。

配置极简：只需要四个 API Key（Serper、Jina、E2B、一个用于摘要的 LLM），就能跑起来。

这背后的设计哲学：**最小依赖、最大可控**。不需要复杂的 Multi-Agent 架构，单 Agent + 好工具 + 好策略 = 高性能。

## 性能：开源 SOTA，逼近商业系统

MiroThinker-1.7 在多个基准测试上的表现：

| Benchmark | Score | 备注 |
|-----------|-------|------|
| BrowseComp | 74.0% | 开源领先 |
| BrowseComp-ZH | 75.3% | **开源 SOTA** |
| GAIA-Val-165 | 82.7% | 超过 Kimi-K2-Thinking |
| HLE-Text | 42.9% | 接近 Gemini Deep Research |

最亮眼的是 **MiroThinker-1.7-mini**：30B 参数，在 BrowseComp-ZH 上达到 72.3%，**用 1/8 的参数量打平了 235B 级别模型**。

这意味着什么？**中小团队也能部署高性能研究 Agent**。

## 技术细节：Recency-Based Context Retention

长链任务的隐形杀手是「上下文爆炸」。

假设每一步工具调用返回 2000 tokens 的内容，走 100 步就是 200K tokens——还没算上 Agent 自己的思考链。

MiroThinker 的解决方案：**只保留最近 K 个工具响应**。

```yaml
keep_tool_result: 5  # 只保留最近 5 个工具响应
```

核心洞察：Agent 的下一步决策主要依赖**最近的观察**，而不是几十步前的搜索结果。保留完整的「思考-行动」轨迹，但裁剪掉过时的工具返回值，既不丢失推理连贯性，又释放了大量上下文空间。

这个策略的效果：在同等上下文预算下，Agent 可以**走得更远、调更多工具、处理更复杂的任务**。

## 开源生态：模型 + 数据 + 框架全公开

MiroThinker 的开源诚意：

- **模型**：HuggingFace 上可下载（30B / 235B）
- **数据**：MiroVerse-v0.1 训练数据集
- **框架**：MiroFlow Agent 框架，支持自定义工具配置
- **基准**：完整的评测脚本和监控工具

复现成本低：一台 4×A100 服务器就能跑 235B 模型，单卡就能跑 30B mini 版本。

## 我的观点

**1. 「交互深度」是 Agent 能力的第三维度**

过去我们只关注模型大小和上下文长度，忽略了 Agent 与环境交互的深度。MiroThinker 证明了：**优化交互模式本身，可以带来巨大的性能提升**。这为 Agent 研究开辟了新方向。

**2. 单 Agent + 好策略 > 复杂 Multi-Agent**

很多项目追求 Multi-Agent 架构（Planner + Executor + Verifier...），但 MiroThinker 用单 Agent + 精心设计的工具策略就达到了顶级性能。**架构复杂度不等于能力**，好的策略比多的角色更重要。

**3. 开源 Agent 正在逼近商业系统的能力边界**

BrowseComp 上，MiroThinker-1.7（开源） vs OpenAI Deep Research（商业）的差距正在缩小。对于大多数研究场景，开源方案已经够用。**技术民主化正在发生**。

**4. Context Retention 是长链任务的通用解法**

Recency-Based Context Retention 的思路可以迁移到任何 Agent 框架。不是所有信息都值得永久保留——**学会遗忘，才能走得更远**。

---

**项目地址**：https://github.com/MiroMindAI/MiroThinker

**在线体验**：https://dr.miromind.ai/

**模型下载**：https://huggingface.co/collections/miromind-ai/mirothinker-17

MiroThinker 不是终点，而是开源 Deep Research Agent 的新起点。当交互深度成为可优化的维度，Agent 能力的天花板被重新定义了。
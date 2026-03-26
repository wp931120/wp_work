# MiroThinker 开源发布：256K 上下文、600 次工具调用，OpenAI 级别的研究 Agent 来了

> 📖 **本文解读内容来源**
>
> - **原始来源**：[MiroThinker: Pushing the Performance Boundaries of Open-Source Research Agents via Model, Context, and Interactive Scaling](https://arxiv.org/html/2511.11793v2)
> - **来源类型**：arXiv 技术报告
> - **作者/团队**：MiroMind Team（50+ 作者）
> - **发布时间**：2025 年 11 月（v2 版本）
> - **核心项目**：MiroThinker v1.0 - 开源研究 Agent
> - **资源链接**：
>   - 🌐 [在线 Demo](https://dr.miromind.ai/)
>   - 💻 [GitHub 代码库](https://github.com/MiroMindAI/MiroThinker)
>   - 🤗 [HuggingFace 模型权重](https://huggingface.co/miromind-ai/MiroThinker-v1.0-72B)

---

你有没有这种感觉：用开源模型做研究任务，总是差那么一口气？

检索能力不够、推理深度不足、工具调用次数有限……很多时候，不是模型不够聪明，而是**它没有足够的"交互空间"去探索问题**。

但商业闭源系统（比如 ChatGPT Agent、Claude Research）又不开放，你没法复现、没法定制、没法社区协作。

这个局面，可能被刚刚发布的 **MiroThinker v1.0** 打破了。

这是一个开源的研究级 Agent，在 GAIA、HLE、BrowseComp 等 4 个代表性基准测试上，**72B 版本不仅超越了所有开源竞品，还逼近了 GPT-5-high 等商业闭源系统**。

最离谱的是：**它支持 256K 上下文窗口，每任务最多可以进行 600 次工具调用**——这是之前开源模型（通常少于 100 次）的 6 倍。

今天这篇深度解读，笔者把这份 50+ 作者的技术报告完整扒了一遍。

**你不需要懂复杂的 RL 公式。** 笔者用大白话给你讲清楚：MiroThinker 到底是什么、它提出的"交互缩放"（Interactive Scaling）为什么是第三维度的突破、以及你能不能用它来搭建自己的研究 Agent。

话不多说，开始。

---

## 这是个啥？为什么要在乎？

**一句话定义：MiroThinker v1.0 是一个开源的、高性能的研究级 Agent 模型。**

它能做什么？
- 自主分解复杂研究问题
- 从互联网检索并整合实时信息
- 综合多源证据
- 生成透明、有根据的结论

**类比一下：** 以前的开源模型像一个"单次思考者"——你问问题，它想一次，给答案。MiroThinker 像一个"研究型助手"——它会先规划、再搜索、再验证、再综合，反复迭代直到得出结论。

下面这张图展示了 MiroThinker 的核心架构和工作流程：

<svg width="100%" viewBox="0 0 750 450" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#11998e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38ef7d;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#fc4a1a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f7b733;stop-opacity:1" />
    </linearGradient>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
    </marker>
  </defs>
  
  <!-- Background -->
  <rect width="750" height="450" fill="#f8f9fa" rx="12" />
  
  <!-- Title -->
  <text x="375" y="35" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">MiroThinker v1.0 核心架构与三阶段训练</text>
  
  <!-- ReAct Loop -->
  <rect x="30" y="60" width="320" height="180" rx="8" fill="#fff" stroke="url(#grad1)" stroke-width="2" />
  <text x="190" y="85" text-anchor="middle" font-size="14" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">🔄 ReAct 推理 - 行动循环</text>
  
  <!-- Thought -->
  <rect x="60" y="105" width="100" height="45" rx="6" fill="url(#grad1)" />
  <text x="110" y="132" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">思考 (T)</text>
  <text x="110" y="147" text-anchor="middle" font-size="10" font-family="system-ui, sans-serif" fill="#fff">分析当前状态</text>
  
  <!-- Arrow -->
  <line x1="160" y1="127" x2="185" y2="127" stroke="#667eea" stroke-width="2" marker-end="url(#arrow)" />
  
  <!-- Action -->
  <rect x="185" y="105" width="100" height="45" rx="6" fill="url(#grad1)" />
  <text x="235" y="132" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">行动 (A)</text>
  <text x="235" y="147" text-anchor="middle" font-size="10" font-family="system-ui, sans-serif" fill="#fff">调用工具</text>
  
  <!-- Arrow -->
  <line x1="285" y1="127" x2="310" y2="127" stroke="#667eea" stroke-width="2" marker-end="url(#arrow)" />
  
  <!-- Observation -->
  <rect x="60" y="165" width="100" height="45" rx="6" fill="url(#grad1)" />
  <text x="110" y="192" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">观察 (O)</text>
  <text x="110" y="207" text-anchor="middle" font-size="10" font-family="system-ui, sans-serif" fill="#fff">工具返回结果</text>
  
  <!-- Loop Arrow -->
  <path d="M 310 127 L 330 127 L 330 187 L 310 187" fill="none" stroke="#667eea" stroke-width="2" marker-end="url(#arrow)" />
  <text x="280" y="205" text-anchor="middle" font-size="10" font-family="system-ui, sans-serif" fill="#667eea">循环直到完成</text>
  
  <!-- Three Dimensions -->
  <rect x="380" y="60" width="340" height="180" rx="8" fill="#fff" stroke="url(#grad2)" stroke-width="2" />
  <text x="550" y="85" text-anchor="middle" font-size="14" font-weight="bold" font-family="system-ui, sans-serif" fill="#11998e">📐 三维度缩放</text>
  
  <!-- Dimension 1 -->
  <rect x="410" y="105" width="280" height="35" rx="6" fill="#fff" stroke="#11998e" stroke-width="1.5" />
  <text x="430" y="127" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#11998e">1. 模型规模</text>
  <text x="550" y="127" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">8B / 30B / 72B</text>
  
  <!-- Dimension 2 -->
  <rect x="410" y="150" width="280" height="35" rx="6" fill="#fff" stroke="#11998e" stroke-width="1.5" />
  <text x="430" y="172" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#11998e">2. 上下文长度</text>
  <text x="550" y="172" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">256K tokens</text>
  
  <!-- Dimension 3 -->
  <rect x="410" y="195" width="280" height="35" rx="6" fill="url(#grad2)" />
  <text x="430" y="217" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">3. 交互深度（新）</text>
  <text x="620" y="217" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#fff">最多 600 次工具调用</text>
  
  <!-- Benchmarks -->
  <rect x="30" y="265" width="690" height="165" rx="8" fill="#fff" stroke="url(#grad3)" stroke-width="2" />
  <text x="375" y="290" text-anchor="middle" font-size="14" font-weight="bold" font-family="system-ui, sans-serif" fill="#fc4a1a">🏆 基准测试成绩（MiroThinker-72B）</text>
  
  <!-- GAIA -->
  <rect x="60" y="310" width="150" height="50" rx="6" fill="#fff" stroke="#fc4a1a" stroke-width="1.5" />
  <text x="135" y="332" text-anchor="middle" font-size="11" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">GAIA</text>
  <text x="135" y="352" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#fc4a1a">81.9%</text>
  
  <!-- HLE -->
  <rect x="230" y="310" width="150" height="50" rx="6" fill="#fff" stroke="#fc4a1a" stroke-width="1.5" />
  <text x="305" y="332" text-anchor="middle" font-size="11" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">HLE</text>
  <text x="305" y="352" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#fc4a1a">37.7%</text>
  
  <!-- BrowseComp -->
  <rect x="400" y="310" width="150" height="50" rx="6" fill="#fff" stroke="#fc4a1a" stroke-width="1.5" />
  <text x="475" y="332" text-anchor="middle" font-size="11" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">BrowseComp</text>
  <text x="475" y="352" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#fc4a1a">47.1%</text>
  
  <!-- BrowseComp-ZH -->
  <rect x="570" y="310" width="120" height="50" rx="6" fill="#fff" stroke="#fc4a1a" stroke-width="1.5" />
  <text x="630" y="332" text-anchor="middle" font-size="11" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">BrowseComp-ZH</text>
  <text x="630" y="352" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#fc4a1a">55.6%</text>
  
  <!-- Key Insight -->
  <rect x="60" y="385" width="630" height="30" rx="6" fill="url(#grad3)" />
  <text x="375" y="405" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">💡 核心洞察：交互深度是继模型规模、上下文长度之后的第三维度</text>
</svg>

**为什么这很重要？**

因为大多数开源 Agent 只在**模型规模**和**上下文长度**两个维度上竞争。

但 MiroThinker 提出了**第三个维度：交互缩放（Interactive Scaling）**。

简单说：**让模型学会更深、更频繁地与环境交互，通过工具调用获取外部反馈来纠正错误、优化推理路径。**

这不是"测试时缩放"（test-time scaling）——那种方法让模型在隔离状态下思考更久，容易陷入错误循环。

交互缩放是**让模型主动获取外部信息、验证中间结果、调整策略**。

---

## 核心突破：三维度缩放

MiroThinker 的性能提升来自三个维度的协同优化：

### 维度 1：模型规模

提供 8B、30B、72B 三个版本，基于 Qwen2.5 和 Qwen3 初始化。

**72B 版本在多个基准上超越了 MiniMax-M2、GLM-4.6 等竞品。**

### 维度 2：上下文长度

**256K tokens 的上下文窗口**，支持长文档阅读、多轮对话历史保留。

配合"基于近因的上下文保留"策略（只保留最近 K 个工具响应），在有限上下文内最大化交互次数。

### 维度 3：交互深度（核心创新）

**每任务最多 600 次工具调用**——这是之前开源模型（通常<100 次）的 6 倍。

通过强化学习（GRPO）训练，模型学会了：
- 更深的推理链
- 更多的工具调用
- 更有效的策略探索

**关键发现：交互深度表现出与模型规模、上下文长度类似的缩放行为。**

也就是说：**交互越深，性能越好，而且是可预测的提升。**

---

## 技术架构：ReAct + 工具接口 + 上下文管理

### ReAct 范式

MiroThinker 基于经典的 **ReAct（Reasoning + Acting）** 范式。

每个步骤 t，模型维护一个轨迹：

```
H_t = {(T_1, A_1, O_1), ..., (T_{t-1}, A_{t-1}, O_{t-1})}
```

其中：
- **T（Thought）**：内部思考
- **A（Action）**：工具调用
- **O（Observation）**：工具返回结果

循环流程：
1. 模型思考：`T_t = f_θ(q, H_t)`
2. 决定行动：`A_t = π_θ(H_t, T_t)`
3. 执行工具：`O_t = Tool(A_t)`
4. 更新轨迹：`H_{t+1} = H_t ∪ {(T_t, A_t, O_t)}`
5. 重复直到无行动（`A_t = ∅`），生成最终答案

### 工具接口

MiroThinker 配备了三类工具：

| 工具类别 | 具体工具 | 用途 |
|---------|---------|------|
| **执行环境** | create_sandbox, run_command, run_python_code | Linux 沙箱，安全执行命令和代码 |
| **文件管理** | upload_file, download_file, download_from_internet | 沙箱与外部文件传输 |
| **信息检索** | google_search, scrape_and_extract_info | 网络搜索、网页信息提取 |

**关键设计：** 网页提取工具内部使用轻量级 LLM（如 Qwen3-14B）来提取任务相关信息，而不是 naive 地抓取整个页面。

这是一种高效的上下文管理形式——把长网页压缩成聚焦的文本证据。

### 上下文管理策略

为了在 256K 上下文内支持 600 次工具调用，MiroThinker 用了两个策略：

#### 1. 基于近因的上下文保留

**核心观察：模型的后续行动主要依赖最近的观察，而不是遥远的观察。**

做法：
- 保留完整的思考和行动序列
- **只保留最近 K 个工具响应**（K=5）
- 早期工具响应被遮蔽（但不删除轨迹）

数学表达：
```
Ŝ_t(K) = {i ∈ {1,...,t-1} | i ≥ t-K}
```

只保留索引在 Ŝ_t(K) 内的工具响应，其他遮蔽为 ∅。

**效果：** 释放更多上下文空间用于更深的交互轨迹，且不导致性能下降。

#### 2. 结果截断

对于可能产生超长输出的工具（如 run_command），设置长度上限，超出部分截断并添加 `[Result truncated]` 标记。

---

## 训练流程：三阶段 pipeline

MiroThinker 的训练分为三个阶段：

### 阶段 1：Agent 监督微调（SFT）

**目标：让模型学会基本的 Agent 行为。**

做法：
1. 构建大规模 SFT 数据集，每个样本是 (任务指令，专家轨迹)
2. 专家轨迹由多个 (思考，行动，观察) 三元组组成
3. 严格过滤和修复原始轨迹中的噪声（重复、无效工具调用等）

损失函数：
```
L_SFT(θ) = -E[(x,H)] [Σ log π_θ(T_t, A_t | x, H_<t)]
```

**类比：** 让实习生先看老师傅怎么做，模仿基本动作。

### 阶段 2：Agent 偏好优化（DPO）

**目标：用偏好数据 refine 决策质量。**

做法：
1. 从 SFT 模型生成偏好数据 (H⁺, H⁻)
2. **偏好标准：只看最终答案正确性，不强制固定模式**
   - 不依赖手工启发式（如规划长度、步骤数）
   - 避免引入系统性偏差
3. 使用 DPO + 辅助 SFT 损失（在优选轨迹上）

损失函数：
```
L_PO(θ) = E[L_DPO(x, H⁺, H⁻)] + λ * L_SFT⁺(θ)
```

**关键设计：** 拒绝轨迹也必须有有效最终答案，避免表面问题（重复、截断）。

### 阶段 3：Agent 强化学习（GRPO）

**目标：让模型在真实环境中探索创造性解决方案。**

做法：
1. 构建支持数千并发 rollouts 的环境
2. 使用 GRPO（Group Relative Policy Optimization）进行在线策略训练
3. 奖励函数：`R(x, H) = α_c * R_correct(H) - α_f * R_format(H)`
4. 轨迹过滤：移除病态行为（连续 API 失败、重复循环等）

**关键创新：流式 rollout 加速**

Agent RL 是多轮交互，不同轨迹完成时间差异大（长尾问题）。

实现流式机制：
- Agent worker 从任务队列流式接收 prompt
- 未完成的任务推回队列下一轮处理
- 收集足够轨迹后进行批量更新

---

## 数据构建：MiroVerse v1.0

为了训练 MiroThinker，团队构建了一个大规模合成数据集 **MiroVerse v1.0**。

### 多文档 QA 合成（MultiDocQA）

流程：
1. **文档语料构建**：Wikipedia、Common Crawl 等高度互链的来源
2. **文档采样与图构建**：类别平衡采样，通过超链接构建知识图谱
3. **文档整合**：转换为 Markdown，剪枝外部链接
4. **事实提取**：提取需要跨文档推理的关键事实
5. **约束模糊化**：将事实转换为间接约束（如"2023 年 3 月 15 日"→"2020 年代春季"）
6. **问题生成**：用 LLM 合成需要多跳推理的问题

**核心思想：** 让问题无法从单一文档回答，必须进行跨文档推理。

### Agent 轨迹合成

使用两种 Agent 范式：
1. **ReAct 单 Agent**：迭代"思考 - 行动 - 观察"循环
2. **MiroFlow 多 Agent**：协调多个专业 Agent 处理复杂工作流

使用多种 LLM（GPT-OSS、DeepSeek-V3.1 等）生成多样化轨迹，避免单模型偏差。

### 开源数据收集

补充了 10+ 个开源 QA 数据集：
- MuSiQue、HotpotQA、WebWalkerQA-Silver
- MegaScience、TaskCraft、QA-Expert-Multi-Hop-V1.0
- OneGen-TrainDataset-MultiHopQA、2WikiMultihopQA
- WikiTables、WebShaper、WebDancer、Toucan-1.5M

---

## 实验结果：全面 SOTA

### 主实验结果

| 模型 | HLE | BrowseComp | BrowseComp-ZH | GAIA |
|------|-----|------------|---------------|------|
| GLM-4.6 | 30.4 | 45.1 | 49.5 | 71.9 |
| MiniMax-M2 | 31.8 | 44.0 | 48.5 | 75.7 |
| DeepSeek-V3.1 | 29.8 | 30.0 | 49.2 | 63.1 |
| Kimi-K2 | 21.7 | 7.4 | 22.2 | 60.2 |
| Claude-4.5-Sonnet | 24.5 | 19.6 | 40.8 | 71.2 |
| OpenAI-GPT-5-high | 35.2 | 54.9 | 65.0 | 76.4 |
| **MiroThinker-8B** | 21.5 | 31.1 | 40.2 | 66.4 |
| **MiroThinker-30B** | 33.4 | 41.2 | 47.8 | 73.5 |
| **MiroThinker-72B** | **37.7** | **47.1** | **55.6** | **81.9** |

**几个关键观察：**

1. **GAIA 新 SOTA**：MiroThinker-72B 达到 81.9%，超越 MiniMax-M2（75.7%）6.2 个百分点。

2. **HLE 超越 GPT-5-high**：37.7% vs 35.2%，高出 2.5 个百分点，且使用相同的 Python 和搜索工具集。

3. **多语言能力强劲**：BrowseComp-ZH 55.6%，超越 GLM-4.6（49.5%）6.1 个百分点。

4. **小版本也 SOTA**：8B 和 30B 版本在各自规模类别内也达到 SOTA。

### 交互缩放验证

论文验证了**交互深度与性能的正相关关系**：

- RL 调优后的模型比 SFT 模型有更长的交互轨迹
- 在 BrowseComp、BrowseComp-ZH、HLE、GAIA 上平均提升 8-10 个百分点
- **交互深度表现出可预测的缩放行为**

这确立了**交互缩放作为第三维度**，与模型规模、上下文长度并列。

---

## 笔者的判断与思考

花几个小时深入研究这份报告，笔者有几个判断想分享。

### 1. "交互缩放"是真正的范式创新

大多数人做 Agent，都在优化模型大小或上下文长度。

但 MiroThinker 证明：**让模型学会更深、更频繁地与环境交互，是独立的性能提升维度。**

这给笔者的启发是：
- 如果你的应用场景需要多步推理（研究、分析、调试），**交互深度可能比模型大小更重要**
- 与其追求更大的模型，不如让现有模型学会更有效地使用工具

### 2. 三阶段训练设计非常精妙

SFT → DPO → GRPO，这个设计与 SumRank（之前解读的论文）有异曲同工之妙：

- **SFT 打基础**：学会基本 Agent 行为
- **DPO 对齐偏好**：用正确性作为唯一标准，避免手工规则偏差
- **GRPO 探索创新**：在真实环境中发现创造性解决方案

**关键洞察：** 偏好优化阶段"只看答案正确性，不强制固定模式"，这避免了引入系统性偏差，保证了可扩展性。

### 3. 上下文管理策略简单但有效

"基于近因的上下文保留"——只保留最近 K 个工具响应。

这个设计很聪明：
- 保留了完整的推理和行动轨迹（模型知道"做了什么"）
- 只遮蔽早期观察（减少上下文占用）
- **不导致性能下降**（因为模型主要依赖最近观察）

这比复杂的记忆机制更简单、更高效。

### 4. 局限性与未来方向

论文也坦诚了几个局限：
- **工具调用质量有待提升**：RL 模型调用更频繁，但部分调用贡献边际
- **思维链过长**：RL 鼓励更长响应，导致可读性下降
- **语言混合**：非英文输入时可能出现中英混杂
- **沙箱能力有限**：代码执行和文件管理工具使用不够熟练

笔者的判断是：**这些局限都是"成长中的烦恼"，不是根本性缺陷。**

随着更多社区贡献和迭代，这些问题会逐步解决。

### 5. 开源的意义

MiroThinker 最大的价值可能不是性能本身，而是**开源**。

闭源系统（ChatGPT Agent、Claude Research）虽然强大，但你没法：
- 复现结果
- 定制工作流
- 社区协作改进

MiroThinker 提供了：
- 完整代码
- 模型权重
- 在线 Demo

**这降低了研究级 Agent 的门槛，让中小团队也能搭建自己的研究助手。**

---

## 结语

MiroThinker 确实是个很强大的设计，就像一个不知疲倦的研究助手，会主动搜索、验证、综合信息。

但笔者必须坦诚：**它不是银弹。**

如果你的任务很简单（单次问答、短文本处理），直接用大模型零样本可能更简单。

但如果你的场景是：
- 复杂研究问题（文献综述、竞品分析）
- 多跳推理（需要跨多个信息源）
- 实时信息检索（需要最新数据）
- 透明可解释（需要看到推理过程）

那 MiroThinker 的思路非常值得借鉴。

跨领域想一下，这暗合了一个朴素道理：**一个人的能力不仅取决于他多聪明（模型规模）、记性多好（上下文长度），还取决于他多愿意主动获取外部信息、验证自己的想法（交互深度）。**

MiroThinker 就是把这个道理编码进了 AI 系统。

**最后给读者的建议：**

如果你在搭建 RAG 或研究 Agent 系统，不妨试试这个思路：
1. 用开源模型初始化（如 Qwen2.5/3）
2. 构建你的领域特定的 Agent 轨迹数据
3. 用三阶段训练（SFT → DPO → GRPO）
4. 优化上下文管理策略，支持更深交互

不需要完全照搬 MiroThinker 的架构，但**"交互缩放"这个核心思想**，值得每个做 AI 应用的人深思。

---

### 参考

- [MiroThinker: Pushing the Performance Boundaries of Open-Source Research Agents](https://arxiv.org/html/2511.11793v2) - arXiv:2511.11793
- [MiroThinker GitHub](https://github.com/MiroMindAI/MiroThinker)
- [MiroThinker HuggingFace](https://huggingface.co/miromind-ai/MiroThinker-v1.0-72B)
- [在线 Demo](https://dr.miromind.ai/)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) - ReAct 原论文
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning](https://arxiv.org/abs/2402.03300) - GRPO 原论文

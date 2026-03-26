# 人大开源 SumRank：24 倍小模型碾压 72B 大模型，长文档排序新 SOTA

> 📖 **本文解读内容来源**
>
> - **原始来源**：[Aligning Summarization Models for Long-Document Listwise Reranking](https://arxiv.org/html/2603.24204v1)
> - **来源类型**：arXiv 论文
> - **作者/团队**：Jincheng Feng, Wenhan Liu, Zhicheng Dou（中国人民大学高瓴人工智能学院）
> - **发布时间**：2026 年 3 月
> - **核心项目**：SumRank - 面向长文档列表式重排序的对齐摘要模型

---

你有没有遇到过这种情况：用 RAG 做搜索，检索回来的文档太长，大模型根本看不完？

或者用 listwise reranking 做排序，但文档一长，推理速度慢得离谱，效果还往下掉？

**说实话，这个问题笔者也头疼了很久。** 长文档排序一直是信息检索领域的老大难问题——截断吧，怕丢掉关键信息；全放进去吧，模型吃不消，延迟还高。

但中国人民大学的研究团队刚刚开源了一个叫 **SumRank** 的解决方案，在 5 个 TREC Deep Learning 基准测试上全部拿到 SOTA。

最离谱的是：**一个 3B 的小模型，经过他们的三阶段训练后，效果逼近 72B 大模型，推理速度还快了 42 倍。**

7B 版本更是直接超越了 72B 大模型的效果，同时保持 12 倍的速度优势。

今天这篇深度解读，笔者把这篇论文的 core idea、三阶段训练框架、实验设计和结果全部扒了一遍。

**你不需要懂复杂的 RL 公式。** 笔者用大白话给你讲清楚：为什么传统的摘要模型不适合排序任务，SumRank 是怎么做到"为排序而摘要"的，以及你能不能把这个思路用到自己的 RAG 系统里。

话不多说，开始。

---

## 这是个啥？为什么要在乎？

**一句话定义：SumRank 是一个"为排序任务量身定制"的摘要模型。**

它不是简单地把长文档压缩成短文本，而是**专门生成有利于下游排序模型判断相关性的摘要**。

**类比一下：** 传统摘要模型就像一个通用秘书，把一份 100 页的报告总结成 5 页摘要，读起来流畅，但关键细节可能丢了。SumRank 就像一个懂检索的专家秘书，知道哪些关键词、哪些证据对判断相关性最重要，总结的时候专门保留这些东西。

下面这张图展示了 SumRank 的核心架构和训练流程：

<svg width="100%" viewBox="0 0 750 420" xmlns="http://www.w3.org/2000/svg">
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
  <rect width="750" height="420" fill="#f8f9fa" rx="12" />
  
  <!-- Title -->
  <text x="375" y="35" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">SumRank 核心架构与三阶段训练流程</text>
  
  <!-- Stage 1: Cold-Start SFT -->
  <rect x="30" y="60" width="220" height="100" rx="8" fill="#fff" stroke="#667eea" stroke-width="2" />
  <text x="140" y="85" text-anchor="middle" font-size="14" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">阶段 1：Cold-Start SFT</text>
  <text x="140" y="110" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">用 72B 教师模型蒸馏</text>
  <text x="140" y="130" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">学习基础摘要生成能力</text>
  <text x="140" y="150" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">40k 实例，5 epochs</text>
  
  <!-- Arrow -->
  <line x1="250" y1="110" x2="280" y2="110" stroke="#666" stroke-width="2" marker-end="url(#arrow)" />
  
  <!-- Stage 2: RL Data Construction -->
  <rect x="280" y="60" width="220" height="100" rx="8" fill="#fff" stroke="#667eea" stroke-width="2" />
  <text x="390" y="85" text-anchor="middle" font-size="14" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">阶段 2：RL 数据构建</text>
  <text x="390" y="110" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">构建含正负样本的候选列表</text>
  <text x="390" y="130" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">生成静态背景摘要列表</text>
  <text x="390" y="150" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">2500 queries，N=10，k=1</text>
  
  <!-- Arrow -->
  <line x1="500" y1="110" x2="530" y2="110" stroke="#666" stroke-width="2" marker-end="url(#arrow)" />
  
  <!-- Stage 3: Rank-Driven GRPO -->
  <rect x="530" y="60" width="200" height="100" rx="8" fill="#fff" stroke="#667eea" stroke-width="2" />
  <text x="630" y="85" text-anchor="middle" font-size="14" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">阶段 3：Rank-Driven GRPO</text>
  <text x="630" y="110" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">用 NDCG@10 作为奖励</text>
  <text x="630" y="130" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">直接优化排序目标</text>
  <text x="630" y="150" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#555">G=8 rollouts，β=0.001</text>
  
  <!-- Inference Pipeline -->
  <rect x="30" y="190" width="690" height="110" rx="8" fill="#fff" stroke="url(#grad2)" stroke-width="2" />
  <text x="375" y="215" text-anchor="middle" font-size="14" font-weight="bold" font-family="system-ui, sans-serif" fill="#11998e">📌 推理流程：Summary-then-Rank</text>
  
  <!-- Step 1 -->
  <rect x="60" y="240" width="140" height="50" rx="6" fill="url(#grad1)" />
  <text x="130" y="262" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">1. SumRank 摘要</text>
  <text x="130" y="282" text-anchor="middle" font-size="10" font-family="system-ui, sans-serif" fill="#fff">长文档 → 紧凑摘要</text>
  
  <!-- Arrow -->
  <line x1="200" y1="265" x2="230" y2="265" stroke="#11998e" stroke-width="2" marker-end="url(#arrow)" />
  
  <!-- Step 2 -->
  <rect x="230" y="240" width="140" height="50" rx="6" fill="url(#grad1)" />
  <text x="300" y="262" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">2. Listwise Rerank</text>
  <text x="300" y="282" text-anchor="middle" font-size="10" font-family="system-ui, sans-serif" fill="#fff">摘要列表 → 排序结果</text>
  
  <!-- Arrow -->
  <line x1="370" y1="265" x2="400" y2="265" stroke="#11998e" stroke-width="2" marker-end="url(#arrow)" />
  
  <!-- Result -->
  <rect x="400" y="240" width="140" height="50" rx="6" fill="url(#grad2)" />
  <text x="470" y="262" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">3. 最终排序</text>
  <text x="470" y="282" text-anchor="middle" font-size="10" font-family="system-ui, sans-serif" fill="#fff">NDCG@10 SOTA</text>
  
  <!-- Key Metrics -->
  <rect x="30" y="325" width="340" height="80" rx="8" fill="#fff" stroke="#667eea" stroke-width="2" />
  <text x="200" y="350" text-anchor="middle" font-size="13" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">📊 核心指标（SumRank 3B vs 72B）</text>
  <text x="70" y="375" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 效果：逼近 72B 大模型</text>
  <text x="70" y="395" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 速度：42 倍加速（1.95s vs 83s）</text>
  <text x="220" y="375" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 模型大小：24 倍更小</text>
  <text x="220" y="395" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 5 个 TREC DL 基准 SOTA</text>
  
  <!-- Key Insight -->
  <rect x="390" y="325" width="330" height="80" rx="8" fill="url(#grad3)" />
  <text x="555" y="350" text-anchor="middle" font-size="13" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">💡 核心洞察</text>
  <text x="555" y="375" text-anchor="middle" font-size="12" font-family="system-ui, sans-serif" fill="#fff">为排序而摘要，而非为人类而摘要</text>
  <text x="555" y="395" text-anchor="middle" font-size="12" font-family="system-ui, sans-serif" fill="#fff">任务对齐 &gt; 通用能力</text>
</svg>

**为什么这很重要？**

因为大多数人在做 RAG 或搜索系统时，都在用**通用摘要模型**或**简单截断**来处理长文档。

但问题是：
- **传统摘要模型**（如 BART、PEGASUS）是为人类读者优化的，追求流畅、连贯，但会过滤掉排序模型需要的关键词和精确细节
- **简单截断**（如 FirstP）虽然保留了开头信息，但丢掉了文档中后部的关键证据

SumRank 的思路是：**既然摘要的最终目的是排序，那就直接用排序指标（NDCG@10）来训练摘要模型。**

这就是所谓的"任务对齐"（task-aligned）。

---

## 核心问题：长文档排序的两大痛点

在深入 SumRank 之前，笔者先给你讲清楚它要解决的问题。

### 痛点 1：效果下降

LLM 做 listwise reranking 时，输入长度剧增会导致**上下文建模负担过重**。

论文里引用了 Liu et al. (2025e) 的工作，证明输入越长，排序性能越差。这跟"Lost in the Middle"现象是一个道理——模型注意力分散，抓不住关键信号。

### 痛点 2：效率爆炸

自注意力机制的计算复杂度是**输入长度的平方**。文档从 100 词变成 1000 词，计算量不是 10 倍，是 100 倍。

这导致推理延迟高得离谱，生产环境根本没法用。

### 现有方案的局限

| 方案 | 做法 | 问题 |
|------|------|------|
| **截断（Truncation）** | 只取文档前 k 个 token | 丢掉中后部的关键证据 |
| **分块（Chunking）** | 把文档切成多段分别处理 | 破坏全局语义连贯性 |
| **通用摘要模型** | 用 BART/PEGASUS 摘要 | 为人类优化，不为排序优化 |
| **零-shot LLM** | 直接用大模型生成摘要 | 没有针对排序任务对齐 |

SumRank 的思路是：**用一个轻量级的 pointwise 摘要模型，先把每个长文档压缩成紧凑的、query-aware 的摘要，然后再做 listwise reranking。**

关键是：这个摘要模型不是随便训练的，而是**用下游排序任务的指标直接优化出来的**。

---

## 三阶段训练框架：步步为营

SumRank 的训练流程分为三个阶段，笔者用大白话给你拆解一下。

### 阶段 1：Cold-Start SFT（冷启动监督微调）

**目标：让模型学会基本的摘要生成能力。**

做法：
1. 用一个强大的教师模型（Qwen2.5-72B-Instruct）生成"黄金摘要"
2. 用这些摘要蒸馏一个轻量级学生模型（Qwen2.5-3B/7B-Instruct）
3. 训练 40k 实例，5 epochs

**类比：** 这就像让一个实习生先看老师傅怎么做，模仿基本动作。

损失函数是标准的自回归交叉熵：

$$\mathcal{L}_{\text{SFT}}(\theta)=-\frac{1}{T}\sum_{t=1}^{T}\log\pi_{\theta}(y_{t}^{*}|X,y_{<t}^{*})$$

别被公式吓到，核心思想就是：**让学生模型的输出尽量接近教师模型的输出**。

### 阶段 2：RL 数据构建

**目标：为强化学习阶段构建合适的训练环境。**

这里有个关键设计：**候选列表必须同时包含正样本和负样本**。

做法：
1. 用 BM25 检索 top-N 候选文档
2. 如果列表里缺少正样本或负样本，就人工注入
3. 用 SFT 阶段的模型为每个文档生成初始摘要，形成"静态背景摘要列表"

**为什么需要静态背景？** 这是为了减少奖励方差、保证计算效率。

想象一下：如果你每次评估一个摘要，都要重新生成整个列表的摘要，那计算量是 O(N×G)。但用静态背景，只需要生成目标文档的 G 个变体，计算量降到 O(G)。

### 阶段 3：Rank-Driven Alignment via GRPO（基于排序的 GRPO 对齐）

**目标：让摘要模型直接为排序指标优化。**

这是 SumRank 的核心创新。

**GRPO（Group Relative Policy Optimization）** 是一种强化学习算法，核心思想是：
1. 对同一个文档，采样 G 个不同的摘要变体（rollouts）
2. 把每个变体放进静态背景列表，用 LLM reranker 排序
3. 用 NDCG@10 作为奖励信号
4. 用组内相对优势更新策略

**奖励函数设计得很巧妙：**

$$
r(y)=\begin{cases}
R(y), & \text{如果是正样本文档} \\
1.0, & \text{如果是负样本且正确拒绝} \\
R(y)-\lambda, & \text{如果是负样本但没拒绝}
\end{cases}
$$

**解读：**
- 正样本：奖励排序分数
- 负样本且正确说"无相关信息"：给满分 1.0
- 负样本但瞎编内容：扣分

这个设计防止模型对不相关文档也强行生成摘要，制造虚假对齐。

**为什么用 GRPO 而不是 PPO？** GRPO 不需要单独的 value model，计算更高效，适合这种列表式评估场景。

---

## 实验结果：小模型碾压大模型

论文在 5 个 TREC Deep Learning 基准（DL 19-23）上做了全面评估。

### 主实验结果

| 方法 | TREC DL19 | DL20 | DL21 | DL22 | DL23 | 平均 |
|------|-----------|------|------|------|------|------|
| BM25（基线） | 68.5 | 63.2 | 59.8 | 61.4 | 58.9 | 62.4 |
| FirstP-256 | 71.2 | 65.8 | 62.1 | 63.5 | 60.2 | 64.6 |
| BART-summarizer | 65.3 | 60.1 | 57.2 | 59.8 | 55.6 | 59.6 |
| Qwen2.5-7B-Instruct（零样本） | 69.8 | 64.5 | 61.3 | 62.9 | 59.5 | 63.6 |
| **SumRank（3B）** | **74.5** | **68.9** | **65.2** | **66.8** | **63.1** | **67.7** |
| **SumRank（7B）** | **75.8** | **70.2** | **66.5** | **68.1** | **64.5** | **69.0** |
| Qwen2.5-72B-Instruct（理论上限） | 74.2 | 68.5 | 65.0 | 66.5 | 62.8 | 67.4 |

**几个关键观察：**

1. **SumRank（3B）逼近 72B 大模型**：3B 模型经过三阶段训练后，效果跟 72B 零样本模型几乎持平，但模型大小只有 1/24，推理速度快 42 倍。

2. **SumRank（7B）超越 72B**：7B 版本不仅效果超过 72B，速度还快 12 倍。这证明**任务对齐的小模型可以战胜通用大模型**。

3. **传统摘要模型甚至不如截断**：BART、PEGASUS 这些专门训练过的摘要模型，效果居然比简单截断还差。为什么？因为它们是为人类读者优化的，会过滤掉排序模型需要的关键词。

4. **零样本 LLM 不够用**：直接用 Qwen2.5-7B 零样本生成摘要，效果还不如 SumRank（3B）。这说明**针对任务训练比模型大小更重要**。

### 消融实验

| 变体 | 平均 NDCG@10 | 下降幅度 |
|------|--------------|----------|
| 完整 SumRank | 67.7 | - |
| w/o Rank-Driven GRPO | 64.2 | -3.5 |
| w/o Cold-Start SFT | 65.8 | -1.9 |

**结论：**
- 去掉 GRPO 阶段，效果下降最严重（-3.5）。说明**只用 SFT 不够，必须用排序指标直接优化**。
- 去掉 SFT 阶段，效果也下降（-1.9）。说明**RL 需要一个好的初始化，从零开始学太难**。

### 效率分析

| 方法 | 平均延迟（秒/查询） | 相对速度 |
|------|---------------------|----------|
| FirstP-128 | 12.3s | 6.3x |
| FirstP-256 | 18.7s | 4.4x |
| BART-summarizer | 4.2s | 2.2x |
| Qwen2.5-72B-Instruct | 83.0s | 1x |
| **SumRank（3B）** | **1.95s** | **42.6x** |
| **SumRank（7B）** | **6.8s** | **12.2x** |

**SumRank 是唯一一个既拿到 SOTA 效果，又保持最低延迟的方法。**

---

## 笔者的判断与思考

花几个小时深入研究这篇论文，笔者有几个判断想分享。

### 1. "任务对齐"是核心护城河

大多数人做 RAG 或搜索系统，都在用**通用组件**：通用嵌入模型、通用摘要模型、通用 reranker。

但 SumRank 证明：**针对具体任务对齐的专用模型，可以碾压通用大模型。**

这给笔者的启发是：如果你的应用场景足够明确（比如法律文档检索、医疗问答），与其用最大的通用模型，不如用中等规模模型 + 任务对齐训练。

### 2. 三阶段设计非常精妙

Cold-Start SFT → RL 数据构建 → Rank-Driven GRPO，这个设计有几个亮点：

- **SFT 打基础**：避免 RL 从零开始，训练更稳定
- **静态背景列表**：减少奖励方差，提高计算效率
- **NDCG 直接优化**：摘要质量由下游任务定义，不是由人类主观判断

这个框架可以迁移到其他场景。比如：
- 为 QA 任务对齐的摘要模型
- 为代码检索对齐的摘要模型
- 为多跳推理对齐的摘要模型

### 3. 小模型 + 精训练 > 大模型 + 零样本

这是一个反直觉但越来越被验证的趋势。

很多人迷信大模型，觉得 72B 一定比 3B 好。但 SumRank 证明：**3B 模型经过针对性训练，可以逼近甚至超越 72B 零样本模型。**

这对资源有限的团队是个好消息：你不需要买最贵的 GPU 集群，用中小模型 + 精训练也能拿到 SOTA。

### 4. 局限性与未来方向

论文也坦诚了几个局限：
- 没试 14B/32B 等中等规模模型
- 需要部署两个模型（摘要 + 排序），增加了运维复杂度
- 未来想做 end-to-end 统一架构

笔者的判断是：**end-to-end 是方向，但两阶段架构在短期内更实用。** 因为可以独立优化摘要和排序模块，调试也更容易。

---

## 结语

SumRank 确实是个很聪明的设计，就像一个懂检索的专家秘书，知道哪些信息对排序最重要。

但笔者必须坦诚：**它不是银弹。**

如果你的文档本来就不长（几百词），或者你的应用场景对延迟不敏感，那直接用大模型零样本可能更简单。

但如果你的场景是：
- 长文档检索（网页、论文、报告）
- 对延迟敏感（在线搜索、实时推荐）
- 有足够训练数据（可以蒸馏 + RL）

那 SumRank 的思路非常值得借鉴。

跨领域想一下，这暗合了一个朴素道理：**工具的价值不在于它有多强大，而在于它跟任务的匹配度有多高。**

一把手术刀不如一把锤子"强大"，但在做手术时，手术刀远比锤子有用。

SumRank 就是一把为排序任务定制的手术刀。

**最后给读者的建议：**

如果你在做大模型检索或 RAG 系统，不妨试试这个思路：
1. 先用大模型蒸馏一个小模型
2. 然后用你的业务指标（点击率、转化率、人工标注）作为奖励
3. 用 RL 做任务对齐

不需要完全照搬 SumRank 的三阶段框架，但**"任务对齐"这个核心思想**，值得每个做 AI 应用的人深思。

---

### 参考

- [Aligning Summarization Models for Long-Document Listwise Reranking](https://arxiv.org/html/2603.24204v1) - arXiv:2603.24204
- [SumRank GitHub Repository](https://github.com/)（待开源）
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) - Liu et al. (2024)
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning](https://arxiv.org/abs/2402.03300) - GRPO 原论文

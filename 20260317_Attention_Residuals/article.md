# Transformer 的残差连接还能再优化？月之暗面给出了一份惊艳答卷

> 📖 **本文解读内容来源**
>
> - **原始来源**：[Attention Residuals](https://github.com/MoonshotAI/Attention-Residuals)
> - **来源类型**：论文
> - **作者/团队**：Moonshot AI（月之暗面）
> - **发布时间**：2026 年 3 月

---

你可能用过 Kimi，但你知道它背后的团队刚刚发了一篇什么论文吗？

上周，月之暗面放出了最新论文 **Attention Residuals**。乍一看标题，笔者以为是某种 Attention 机制的变体。读完才发现，这篇论文做了一件更"底层"的事——

**它重新设计了 Transformer 的残差连接。**

残差连接？不是 2015 年 ResNet 就搞定的东西吗？还能优化？

好问题。这篇论文的回答是：能，而且优化后效果惊人——同等算力下，模型效果相当于用 **1.25 倍算力训练出来的 baseline**。

---

## 这是个啥：残差连接的"均匀累加"困境

先来回顾一下 Transformer 的残差连接是怎么做的。

标准的残差连接公式很简单：

```
h_l = h_{l-1} + f(h_{l-1})
```

每一层的输出 = 上一层的输出 + 这一层的变换结果。所有的层以**固定权重 1** 均匀累加。

这有什么问题？

问题在于，随着模型深度增加（现在的 LLM 动辄几十层甚至上百层），这种"均匀累加"会带来两个隐患：

**1. 稀释效应**：每一层的贡献被平均分配，越深的层，其独特贡献越容易被"稀释"。

**2. 幅度爆炸**：随着层数增加，隐藏状态的幅度会无限增长。PreNorm 虽然缓解了梯度消失，但并没有解决幅度增长问题。

下面这张图展示了 AttnRes 的核心思想：

<svg width="100%" viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4f46e5;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7c3aed;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#059669;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#10b981;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" fill="#1f2937" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">三种残差连接方式对比</text>

  <!-- (a) Standard Residuals -->
  <text x="130" y="60" text-anchor="middle" fill="#6b7280" font-size="12" font-family="system-ui, sans-serif">(a) 标准残差：固定权重累加</text>
  <rect x="50" y="80" width="60" height="35" rx="6" fill="#e5e7eb"/>
  <text x="80" y="102" text-anchor="middle" fill="#374151" font-size="11" font-family="system-ui, sans-serif">Layer 1</text>
  <rect x="50" y="125" width="60" height="35" rx="6" fill="#e5e7eb"/>
  <text x="80" y="147" text-anchor="middle" fill="#374151" font-size="11" font-family="system-ui, sans-serif">Layer 2</text>
  <rect x="50" y="170" width="60" height="35" rx="6" fill="#e5e7eb"/>
  <text x="80" y="192" text-anchor="middle" fill="#374151" font-size="11" font-family="system-ui, sans-serif">Layer 3</text>
  <text x="130" y="145" text-anchor="start" fill="#9ca3af" font-size="20" font-family="system-ui, sans-serif">+</text>
  <text x="130" y="190" text-anchor="start" fill="#9ca3af" font-size="20" font-family="system-ui, sans-serif">+</text>
  <rect x="150" y="130" width="70" height="50" rx="6" fill="url(#grad1)"/>
  <text x="185" y="160" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">固定权重</text>
  <text x="185" y="220" text-anchor="middle" fill="#ef4444" font-size="10" font-family="system-ui, sans-serif">⚠️ 贡献被稀释</text>

  <!-- (b) Full AttnRes -->
  <text x="380" y="60" text-anchor="middle" fill="#6b7280" font-size="12" font-family="system-ui, sans-serif">(b) Full AttnRes：跨层注意力</text>
  <rect x="300" y="80" width="60" height="35" rx="6" fill="#dbeafe"/>
  <text x="330" y="102" text-anchor="middle" fill="#374151" font-size="11" font-family="system-ui, sans-serif">Layer 1</text>
  <rect x="300" y="125" width="60" height="35" rx="6" fill="#dbeafe"/>
  <text x="330" y="147" text-anchor="middle" fill="#374151" font-size="11" font-family="system-ui, sans-serif">Layer 2</text>
  <rect x="300" y="170" width="60" height="35" rx="6" fill="#dbeafe"/>
  <text x="330" y="192" text-anchor="middle" fill="#374151" font-size="11" font-family="system-ui, sans-serif">Layer 3</text>
  <!-- Attention arrows -->
  <line x1="360" y1="97" x2="400" y2="145" stroke="#4f46e5" stroke-width="1.5" stroke-dasharray="3,2"/>
  <line x1="360" y1="142" x2="400" y2="150" stroke="#4f46e5" stroke-width="1.5" stroke-dasharray="3,2"/>
  <line x1="360" y1="187" x2="400" y2="155" stroke="#4f46e5" stroke-width="1.5" stroke-dasharray="3,2"/>
  <rect x="400" y="120" width="80" height="70" rx="8" fill="url(#grad2)"/>
  <text x="440" y="150" text-anchor="middle" fill="#fff" font-size="10" font-family="system-ui, sans-serif">Softmax</text>
  <text x="440" y="165" text-anchor="middle" fill="#fff" font-size="10" font-family="system-ui, sans-serif">Attention</text>
  <text x="440" y="220" text-anchor="middle" fill="#059669" font-size="10" font-family="system-ui, sans-serif">✓ 选择性聚合</text>

  <!-- (c) Block AttnRes -->
  <text x="650" y="60" text-anchor="middle" fill="#6b7280" font-size="12" font-family="system-ui, sans-serif">(c) Block AttnRes：分块注意力</text>
  <!-- Block 1 -->
  <rect x="560" y="75" width="85" height="55" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
  <text x="602" y="95" text-anchor="middle" fill="#92400e" font-size="10" font-family="system-ui, sans-serif">Block 1</text>
  <rect x="570" y="100" width="30" height="22" rx="3" fill="#fbbf24"/>
  <rect x="605" y="100" width="30" height="22" rx="3" fill="#fbbf24"/>
  <!-- Block 2 -->
  <rect x="560" y="140" width="85" height="55" rx="6" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>
  <text x="602" y="160" text-anchor="middle" fill="#1e40af" font-size="10" font-family="system-ui, sans-serif">Block 2</text>
  <rect x="570" y="165" width="30" height="22" rx="3" fill="#60a5fa"/>
  <rect x="605" y="165" width="30" height="22" rx="3" fill="#60a5fa"/>
  <!-- Block 3 -->
  <rect x="560" y="205" width="85" height="55" rx="6" fill="#dcfce7" stroke="#22c55e" stroke-width="1"/>
  <text x="602" y="225" text-anchor="middle" fill="#166534" font-size="10" font-family="system-ui, sans-serif">Block 3</text>
  <rect x="570" y="230" width="30" height="22" rx="3" fill="#4ade80"/>
  <rect x="605" y="230" width="30" height="22" rx="3" fill="#4ade80"/>
  <!-- Inter-block attention -->
  <line x1="650" y1="102" x2="700" y2="165" stroke="#7c3aed" stroke-width="2"/>
  <line x1="650" y1="167" x2="700" y2="175" stroke="#7c3aed" stroke-width="2"/>
  <line x1="650" y1="232" x2="700" y2="185" stroke="#7c3aed" stroke-width="2"/>
  <circle cx="710" cy="160" r="20" fill="#7c3aed"/>
  <text x="710" y="165" text-anchor="middle" fill="#fff" font-size="10" font-family="system-ui, sans-serif">Attn</text>
</svg>

用大白话说，标准残差就像是一个"平均主义"的公司——不管你干得好不好，每个人的奖金都一样。时间久了，干活的人就觉得"反正都一样"，积极性就下来了。

---

## 核心创新：让残差连接学会"挑食"

AttnRes 的核心思想非常直观：

**既然 Transformer 层内部用注意力机制来"选择性"关注 token，为什么残差连接不能也"选择性"地聚合不同层的输出？**

具体怎么做？公式如下：

```
h_l = Σ α_{i→l} · v_i
```

其中，权重 `α_{i→l}` 通过一个可学习的 pseudo-query（伪查询向量）计算 softmax 得到。每一层都有一个属于自己的 query 向量，用来"询问"前面所有层的输出应该贡献多少。

这带来了几个关键优势：

**1. 内容感知聚合**：权重是根据实际内容计算的，而非固定不变。模型可以根据当前输入动态调整不同层的重要性。

**2. 幅度可控**：因为 softmax 天然归一化，输出的幅度不会无限增长。这解决了 PreNorm 的一个潜在隐患。

**3. 梯度分布更均匀**：实验表明，AttnRes 让梯度在各层之间分布更加均匀，缓解了深层的"梯度饥饿"问题。

---

## 工程实现：Block AttnRes 降低内存开销

Full AttnRes 有一个实际问题：内存开销。

如果每一层都要"看"前面所有层的输出，内存复杂度会达到 O(Ld)，其中 L 是层数，d 是隐藏维度。对于 100 层的大模型，这笔开销不小。

于是论文提出了 **Block AttnRes**：

1. 把层分成 N 个块（比如 8 个块）
2. 块内部用标准残差累积
3. 只在块之间做注意力聚合

这样内存开销从 O(Ld) 降到 O(Nd)，而实验表明 8 个块就能恢复 Full AttnRes 大部分收益。

```python
def block_attn_res(blocks, partial_block, proj, norm):
    """
    块间注意力：对已完成的块表示 + 当前块的部分和做注意力
    blocks: 之前各块的表示 [N, B, T, D]
    partial_block: 当前块内的部分和 [B, T, D]
    """
    V = torch.stack(blocks + [partial_block])  # [N+1, B, T, D]
    K = norm(V)
    # 用可学习的 query 计算 logits
    logits = torch.einsum('d, n b t d -> n b t', proj.weight.squeeze(), K)
    # softmax 加权求和
    h = torch.einsum('n b t, n b t d -> b t d', logits.softmax(0), V)
    return h
```

是不是很像 Multi-Head Attention 的简化版？只不过这里的"序列"维度变成了"层"维度。

---

## 效果如何：1.25 倍算力白嫖

论文的实验结果相当硬核。

**Scaling Law 实验**表明，AttnRes 在所有计算预算下都优于 baseline。Block AttnRes 的损失曲线，相当于用 **1.25 倍算力训练的 baseline**。

<svg width="100%" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#f8fafc;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e2e8f0;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="600" height="300" fill="url(#bgGrad)" rx="8"/>

  <!-- Title -->
  <text x="300" y="30" text-anchor="middle" fill="#1f2937" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">Scaling Law：AttnRes vs Baseline</text>

  <!-- Axes -->
  <line x1="80" y1="260" x2="550" y2="260" stroke="#9ca3af" stroke-width="1.5"/>
  <line x1="80" y1="260" x2="80" y2="60" stroke="#9ca3af" stroke-width="1.5"/>
  <text x="315" y="285" text-anchor="middle" fill="#6b7280" font-size="12" font-family="system-ui, sans-serif">Compute Budget</text>
  <text x="40" y="160" text-anchor="middle" fill="#6b7280" font-size="12" font-family="system-ui, sans-serif" transform="rotate(-90, 40, 160)">Loss</text>

  <!-- Baseline curve -->
  <path d="M 100 220 Q 200 180 300 140 Q 400 110 520 85" stroke="#94a3b8" stroke-width="3" fill="none"/>
  <text x="530" y="90" fill="#64748b" font-size="11" font-family="system-ui, sans-serif">Baseline</text>

  <!-- AttnRes curve -->
  <path d="M 100 200 Q 200 155 300 115 Q 400 85 520 65" stroke="#4f46e5" stroke-width="3" fill="none"/>
  <text x="530" y="68" fill="#4f46e5" font-size="11" font-weight="bold" font-family="system-ui, sans-serif">AttnRes</text>

  <!-- 1.25x annotation -->
  <line x1="280" y1="140" x2="280" y2="115" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="295" y="130" fill="#ef4444" font-size="10" font-family="system-ui, sans-serif">= 1.25x compute</text>

  <!-- Legend -->
  <rect x="420" y="220" width="15" height="3" fill="#94a3b8"/>
  <text x="440" y="224" fill="#6b7280" font-size="10" font-family="system-ui, sans-serif">Baseline</text>
  <rect x="420" y="238" width="15" height="3" fill="#4f46e5"/>
  <text x="440" y="242" fill="#6b7280" font-size="10" font-family="system-ui, sans-serif">AttnRes</text>
</svg>

**下游任务表现**更是一骑绝尘。在 Kimi Linear 48B 模型上（1.4T tokens 训练）：

| 类别 | Benchmark | Baseline | AttnRes | 提升 |
|:---|:---|:---:|:---:|:---:|
| 通用 | MMLU | 73.5 | **74.6** | +1.1 |
| | GPQA-Diamond | 36.9 | **44.4** | **+7.5** |
| | BBH | 76.3 | **78.0** | +1.7 |
| 数学&代码 | Math | 53.5 | **57.1** | +3.6 |
| | HumanEval | 59.1 | **62.2** | +3.1 |
| 中文 | CMMLU | 82.0 | **82.9** | +0.9 |
| | C-Eval | 79.6 | **82.5** | +2.9 |

最亮眼的是 **GPQA-Diamond**（研究生级别科学问答）提升了 **7.5 分**，这是一个需要多步推理的 benchmark，说明 AttnRes 对复杂推理任务特别有效。

---

## 为什么有效：训练动力学分析

论文还做了一个很有意思的分析——训练动力学（Training Dynamics）。

<svg width="100%" viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="redGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#fecaca;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ef4444;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#bbf7d0;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#22c55e;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Title -->
  <text x="350" y="25" text-anchor="middle" fill="#1f2937" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">隐藏状态幅度对比（随层数变化）</text>

  <!-- Left: Baseline -->
  <text x="175" y="50" text-anchor="middle" fill="#6b7280" font-size="11" font-family="system-ui, sans-serif">Baseline PreNorm</text>
  <rect x="50" y="60" width="250" height="120" fill="#fef2f2" rx="4"/>
  <!-- Rising curve -->
  <path d="M 70 150 Q 120 140 170 120 Q 220 90 270 60" stroke="#ef4444" stroke-width="2.5" fill="none"/>
  <text x="280" y="55" fill="#ef4444" font-size="9" font-family="system-ui, sans-serif">幅度增长</text>
  <!-- Layer axis -->
  <line x1="70" y1="165" x2="270" y2="165" stroke="#9ca3af" stroke-width="1"/>
  <text x="170" y="185" text-anchor="middle" fill="#9ca3af" font-size="9" font-family="system-ui, sans-serif">Layer 0 → Layer L</text>

  <!-- Right: AttnRes -->
  <text x="525" y="50" text-anchor="middle" fill="#6b7280" font-size="11" font-family="system-ui, sans-serif">AttnRes</text>
  <rect x="400" y="60" width="250" height="120" fill="#f0fdf4" rx="4"/>
  <!-- Stable curve -->
  <path d="M 420 110 Q 520 105 620 110" stroke="#22c55e" stroke-width="2.5" fill="none"/>
  <text x="630" y="115" fill="#22c55e" font-size="9" font-family="system-ui, sans-serif">幅度稳定</text>
  <!-- Layer axis -->
  <line x1="420" y1="165" x2="620" y2="165" stroke="#9ca3af" stroke-width="1"/>
  <text x="520" y="185" text-anchor="middle" fill="#9ca3af" font-size="9" font-family="system-ui, sans-serif">Layer 0 → Layer L</text>
</svg>

可以看到，Baseline 的隐藏状态幅度随着层数增加而线性增长（红色曲线），而 AttnRes 则保持稳定（绿色曲线）。

这意味着什么？

1. **数值稳定性更好**：不会出现数值溢出的风险
2. **梯度传播更健康**：梯度在各层分布更均匀，不会出现"梯度集中在浅层、深层几乎不更新"的问题
3. **深层更有存在感**：每一层的贡献被合理分配，深层不会被"淹没"

---

## 我的观点

读完这篇论文，笔者有三个判断：

**1. 这是一次"被忽视的突破"**

残差连接太基础了，基础到很多人觉得"没什么好改的"。但正是这种"理所当然"，让我们错过了改进的机会。AttnRes 的核心思想其实很简单——把注意力机制从 token 维度扩展到 layer 维度。但简单的想法往往最有价值。

**2. 工程实现很克制**

论文没有一味追求"理论最优"的 Full AttnRes，而是提出了实用的 Block AttnRes。这说明团队真正考虑过大模型训练的实际约束。这种"克制"在学术圈并不多见，但对工业落地至关重要。

**3. 可能会引发一波"残差连接改造"热潮**

就像 LayerNorm 被 RMSNorm 替代、ReLU 被 SwiGLU 替代一样，残差连接可能会成为下一个"基础组件升级"的热点。如果你在做大模型训练，值得认真评估一下 AttnRes。

---

## 结语

Attention Residuals 这篇论文，让笔者想起一句话：

**"最伟大的创新，往往藏在最平凡的角落。"**

残差连接存在了近十年，几乎所有的深度学习模型都在用它。但很少有人问：为什么必须是固定权重？为什么不能让模型自己学会"挑食"？

月之暗面问了，而且给出了漂亮的答案。

不得不感叹一句：有时候，最好的优化不是加东西，而是改变"理所当然"的假设。

---

### 参考

- [Attention Residuals - GitHub](https://github.com/MoonshotAI/Attention-Residuals)
- [Attention Residuals - PDF](https://github.com/MoonshotAI/Attention-Residuals/blob/master/Attention_Residuals.pdf)
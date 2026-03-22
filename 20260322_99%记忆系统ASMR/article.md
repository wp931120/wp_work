# AI 记忆问题被彻底解决了？Supermemory 用 99% 准确率宣告答案

> 📖 **本文解读内容来源**
>
> - **原始来源**：[We broke the frontier in agent memory: Introducing ~99% SOTA memory system](https://github.com/supermemoryai)
> - **来源类型**：技术博客
> - **作者/团队**：Dhravya Shah / Supermemory 团队
> - **发布时间**：2025 年 3 月

---

大多数 AI 从业者以为，**向量检索（Vector Search）** 是 AI 记忆系统的基石——把文本切成块、算嵌入向量、存进向量数据库，检索时按相似度匹配就完事了。

但 Supermemory 团队最近交出了一份颠覆认知的答卷：他们完全抛弃向量数据库，用一套纯**多智能体协作**的架构，在 LongMemEval 基准测试上砸出了 **~99% 的准确率**。

这不是魔术，而是一次架构范式的彻底重构。

---

## 什么是 LongMemEval？为什么它这么难啃？

在深入技术细节之前，笔者先容啰嗦一下这个基准测试的分量。

**LongMemEval** 是目前最严苛的 AI 长期记忆评测基准之一。它不像普通测试那样问几个简单问题，而是模拟了真实生产环境的"混沌"：

- **11.5 万+ token** 的对话历史
- **跨会话**的信息碎片，同一件事可能分散在十几次对话里
- **矛盾信息**，用户先说"我喜欢咖啡"，后来又改口"其实我戒咖啡了"
- **时间推理**，问题需要理解"上上周三"、"三个月前"这种时间关系

传统记忆系统在这里栽跟头的原因很简单：**检索噪音太大**。

向量相似度分不清"我喜欢咖啡"和"我戒咖啡了"哪个是最新的——在语义空间里，它们太像了。LLM 拿到一堆似是而非的上下文，自然就懵了。

---

## 核心突破：ASMR 架构解析

Supermemory 把这套新技术命名为 **ASMR（Agentic Search and Memory Retrieval）**。别误会，这跟那个让人颅内高潮的 ASMR 没关系——但同样让人舒爽。

这套架构的核心思想非常激进：**用主动推理替代向量检索**。

### 架构总览

整个系统分为三个阶段，每个阶段都有多个"专业智能体"并行工作：

下面这张图展示了 ASMR 的核心架构：

<svg width="100%" viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.2"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="800" height="500" fill="#f8fafc"/>

  <!-- 阶段一：摄入 -->
  <rect x="30" y="60" width="220" height="180" rx="12" fill="#e0e7ff" stroke="#667eea" stroke-width="2" filter="url(#shadow)"/>
  <text x="140" y="90" text-anchor="middle" fill="#4338ca" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">第一阶段：并行摄入</text>

  <rect x="50" y="110" width="80" height="40" rx="6" fill="url(#grad1)"/>
  <text x="90" y="135" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Observer 1</text>

  <rect x="50" y="160" width="80" height="40" rx="6" fill="url(#grad1)"/>
  <text x="90" y="185" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Observer 2</text>

  <rect x="150" y="110" width="80" height="40" rx="6" fill="url(#grad1)"/>
  <text x="190" y="135" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Observer 3</text>

  <text x="140" y="225" text-anchor="middle" fill="#6b7280" font-size="11" font-family="system-ui, sans-serif">提取：个人信息/偏好/事件</text>

  <!-- 箭头1 -->
  <path d="M250 150 L290 150" stroke="#667eea" stroke-width="3" fill="none" marker-end="url(#arrowhead1)"/>
  <defs>
    <marker id="arrowhead1" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#667eea"/>
    </marker>
  </defs>

  <!-- 存储层 -->
  <rect x="290" y="100" width="100" height="100" rx="12" fill="#fef3c7" stroke="#f59e0b" stroke-width="2" filter="url(#shadow)"/>
  <text x="340" y="140" text-anchor="middle" fill="#92400e" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">结构化</text>
  <text x="340" y="160" text-anchor="middle" fill="#92400e" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">存储</text>

  <!-- 箭头2 -->
  <path d="M390 150 L430 150" stroke="#f59e0b" stroke-width="3" fill="none" marker-end="url(#arrowhead2)"/>
  <defs>
    <marker id="arrowhead2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#f59e0b"/>
    </marker>
  </defs>

  <!-- 阶段二：检索 -->
  <rect x="430" y="60" width="220" height="180" rx="12" fill="#fce7f3" stroke="#f5576c" stroke-width="2" filter="url(#shadow)"/>
  <text x="540" y="90" text-anchor="middle" fill="#be185d" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">第二阶段：主动检索</text>

  <rect x="450" y="110" width="80" height="40" rx="6" fill="url(#grad2)"/>
  <text x="490" y="135" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Search 1</text>

  <rect x="450" y="160" width="80" height="40" rx="6" fill="url(#grad2)"/>
  <text x="490" y="185" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Search 2</text>

  <rect x="550" y="110" width="80" height="40" rx="6" fill="url(#grad2)"/>
  <text x="590" y="135" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Search 3</text>

  <text x="540" y="225" text-anchor="middle" fill="#6b7280" font-size="11" font-family="system-ui, sans-serif">事实/上下文/时间线</text>

  <!-- 箭头3 -->
  <path d="M650 150 L690 150" stroke="#f5576c" stroke-width="3" fill="none" marker-end="url(#arrowhead3)"/>
  <defs>
    <marker id="arrowhead3" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#f5576c"/>
    </marker>
  </defs>

  <!-- 阶段三：回答 -->
  <rect x="690" y="60" width="80" height="180" rx="12" fill="#ecfeff" stroke="#06b6d4" stroke-width="2" filter="url(#shadow)"/>
  <text x="730" y="90" text-anchor="middle" fill="#0e7490" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">第三阶段</text>

  <rect x="700" y="110" width="60" height="35" rx="6" fill="url(#grad3)"/>
  <text x="730" y="133" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">8变体</text>

  <text x="730" y="165" text-anchor="middle" fill="#0e7490" font-size="12" font-family="system-ui, sans-serif">或</text>

  <rect x="700" y="180" width="60" height="35" rx="6" fill="url(#grad3)"/>
  <text x="730" y="203" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">12森林</text>

  <!-- 结果 -->
  <rect x="280" y="280" width="320" height="80" rx="12" fill="#dcfce7" stroke="#22c55e" stroke-width="2" filter="url(#shadow)"/>
  <text x="440" y="315" text-anchor="middle" fill="#166534" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">~99% 准确率</text>
  <text x="440" y="340" text-anchor="middle" fill="#166534" font-size="14" font-family="system-ui, sans-serif">无需向量数据库，纯智能体推理</text>

  <!-- 对比标注 -->
  <rect x="100" y="400" width="250" height="70" rx="10" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
  <text x="225" y="430" text-anchor="middle" fill="#dc2626" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">❌ 传统 RAG</text>
  <text x="225" y="450" text-anchor="middle" fill="#7f1d1d" font-size="11" font-family="system-ui, sans-serif">向量相似度无法区分新旧信息</text>

  <rect x="450" y="400" width="250" height="70" rx="10" fill="#d1fae5" stroke="#10b981" stroke-width="2"/>
  <text x="575" y="430" text-anchor="middle" fill="#059669" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">✓ ASMR</text>
  <text x="575" y="450" text-anchor="middle" fill="#064e3b" font-size="11" font-family="system-ui, sans-serif">智能体主动推理时间线</text>
</svg>

**第一阶段：并行摄入（Observer Agents）**

部署 3 个并行的"观察者智能体"（使用 Gemini 2.0 Flash），各自负责读取不同的会话：

- Agent 1：处理会话 1、3、5...
- Agent 2：处理会话 2、4、6...
- Agent 3：处理会话 3、6、9...

每个智能体从原始对话中提取六类结构化信息：个人信息、偏好、事件、时间数据、更新记录、助手相关信息。

**第二阶段：主动检索（Search Agents）**

当用户提问时，不再查向量库，而是派出 3 个"搜索智能体"：

- Agent 1：搜索直接事实和明确陈述
- Agent 2：挖掘相关上下文、社交线索和隐含意义
- Agent 3：重建时间线和关系图谱

这三个智能体**主动阅读和推理**存储的结构化信息，而非做数学相似度匹配。

**第三阶段：集成回答（Answering Ensembles）**

这是最精彩的部分。研究团队实验了两种回答策略：

**Run 1：8 变体集成（98.60% 准确率）**

用 8 个高度专业化的提示变体并行回答同一问题——有的擅长计数，有的精通时间推理，有的专攻细节挖掘。只要有一个变体找到正确答案，就算成功。

**Run 2：12 变体决策森林（97.20% 准确率）**

12 个智能体（使用 GPT-4o-mini）独立给出答案，然后由一个"聚合器 LLM"进行多数投票和冲突解决，输出唯一答案。

---

## 为什么抛弃向量检索反而更强？

这是笔者读完这篇报告后最受启发的部分。

**传统 RAG 的致命缺陷**在于：语义相似度无法区分"旧事实"和"新修正"。

举个例子：用户在 3 月 1 日说"我是程序员"，在 3 月 15 日说"我转行做产品了"。这两句话在向量空间里距离很近——都关于职业。如果系统检索时把两条都捞出来，LLM 就会困惑。

ASMR 的解决方案是让智能体**主动推理时间线**。它不是问"这两句话像不像"，而是问"哪句话更晚？最新的信息是什么？"。

这就是"主动推理"和"被动匹配"的本质区别。

---

## 笔者的三点判断

读完这篇技术报告，笔者有三点核心观点想分享：

**第一，"多智能体协作"可能是 RAG 的终局形态。**

单靠一个模型"又检索又推理"是有瓶颈的。把任务拆解给专业智能体，让每个智能体只做一件事、做到极致，然后聚合结果——这种"分而治之"的思路在工程上更可控，效果上也更可解释。

**第二，向量数据库不会消失，但角色会转变。**

ASMR 并没有否定向量检索的价值，而是说它不适合处理"时序敏感、矛盾频繁"的场景。对于简单的语义搜索，向量数据库依然是性价比最高的选择。未来的记忆系统可能是"向量粗筛 + 智能体精筛"的混合架构。

**第三，这套架构的代价是"更慢、更贵"。**

文章没有回避这个问题——多智能体编排需要更多 API 调用，延迟和成本都会上升。对于实时性要求高的场景，这是需要权衡的。但对于"记忆"这种可以异步处理的任务，这笔账是划算的。

---

## 开源预告：11 天后揭晓

Supermemory 团队已经宣布，将在 4 月初开源这套 ASMR 架构的完整代码。

他们的 GitHub 仓库是 [supermemoryai](https://github.com/supermemoryai)，有兴趣的读者可以先 Star 关注。

笔者会持续跟进，等代码放出后第一时间做实战评测。

---

## 结语

不得不感叹一句：**AI 记忆问题的解法，竟然是"让 AI 自己去读、去想、去判断"**。

这听起来像是一句废话——但恰恰是这种"回归本质"的思路，打破了我们对向量检索的路径依赖。

多智能体协作不是新概念，但 Supermemory 把它用在"记忆检索"这个具体场景里，并且用 ~99% 的准确率证明了这条路走得通，这才是真正有价值的创新。

大道至简，也不过如此。

---

### 参考

- [Supermemory GitHub](https://github.com/supermemoryai)
- [LongMemEval Benchmark](https://github.com/Thomas-xzz/LongMemEval)
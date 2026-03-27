# Agentic Memory：深度解析

> 📖 **本文翻译自**
>
> - **原始来源**：[Agentic Memory: A Detailed Breakdown - @techwith_ram](https://x.com/techwith_ram/status/xxxxx)
> - **作者**：Ramakrushna — e/acc
> - **发布时间**：2026年3月

---

想象一下，有一天你雇佣了一位才华横溢的自由职业者。第一天，她表现出色，抓住每一个 bug，编写清晰的文档，甚至提出了一些你没想过的改进建议。你印象深刻。

第二天，你走进办公室说："嘿，还记得我们昨天讨论的那个问题吗？"

她停顿了一下。看着你。微微一笑。

"抱歉……什么问题？"

没有记忆。没有上下文。完全消失。你会像我写这篇文章时一样震惊。

**这正是大多数 LLM 的行为方式。** 每一次新的对话都是全新的开始。模型不知道你是谁、你们一起构建了什么，甚至几分钟前在另一个聊天窗口讨论的内容也不记得。

对于简单的聊天机器人，这没问题。但对于一个 Agent——一个执行任务、做出决策、随时间改进的系统——这种"失忆症"是致命的。

因为真正的智能不仅仅是良好地响应。它是关于**记住、学习和在前人的基础上构建**。

**记忆是将无状态系统转变为能够真正进化的东西的关键。**

---

## 一、什么是 Agentic Memory？

Agentic Memory 不仅仅是一件事。它更像是一个在后台运作的系统——不同类型的存储、检索信息的方式，以及管理这一切的智能策略，使 Agent 能够随着时间的推移真正承载上下文。

**核心思想很简单**：记忆不是在做一份工作，而是在同时做**三份截然不同的工作**。

### 1.1 记忆的三个核心功能

| 功能 | 定义 | 作用 |
|-----|------|------|
| **Continuity（连续性）** | 关于身份 | Agent 如何知道你是谁、你偏好什么、你们已经一起构建了什么。没有它，每次交互都感觉像从头开始。 |
| **Context（上下文）** | 关于当前任务 | 刚刚发生了什么、使用了哪个工具、返回了什么结果、接下来需要做什么。这是防止多步骤工作流崩溃的关键。 |
| **Learning（学习）** | 关于变得更好 | 理解什么有效、什么无效，慢慢改进决策，而不是重复同样的错误。 |

**结合起来，它使 Agent 感觉一致、可靠，每次交互都变得更智能一点。**

---

## 二、四种记忆类型

该领域已经收敛到四种不同的记忆类型。可以把它们想象成大脑的四个不同部分，每个部分都为特定的工作而进化。

### 2.1 In-Context Memory（上下文内记忆）

**上下文窗口是 Agent 的工作台**。上面的所有内容都可以立即访问。模型可以在单次前向传递中对它进行推理。不需要检索步骤。

**但工作台有大小限制**。每个 token 都要花钱和时间。当会话结束时，工作台会被清空。

**什么存在于上下文中？**

| 内容类型 | 说明 |
|---------|------|
| **System prompt** | Agent 人格、规则、能力、当前日期/用户信息 |
| **Conversation history** | 本次会话到目前为止的对话往来 |
| **Tool call results** | Agent 刚刚调用的工具的输出 |
| **Retrieved memories** | 从外部存储中提取的片段 |
| **Scratchpad** | 中间推理（逐步思考输出） |

#### 滑动窗口问题

在长对话中，历史会累积并最终溢出上下文限制。截断最旧消息的简单解决方案会丢失重要的早期上下文。更好的策略：

| 策略 | 说明 |
|-----|------|
| **Summarization（摘要）** | 定期将旧对话压缩成简短摘要并替换它们 |
| **Selective retention（选择性保留）** | 保留包含关键事实、决策或工具结果的对话；丢弃闲聊 |
| **Offload to external memory（卸载到外部记忆）** | 将重要事实提取到向量存储中，然后按需检索 |

---

### 2.2 External Memory（外部记忆）

外部记忆是在模型之外持久化的任何东西——数据库、向量存储、键值存储和文件。它会跨越会话边界存活。如果存储得当，你的 Agent 可以记住六个月前的事情。

**两种外部存储方式：**

| 类型 | 工具 | 特点 |
|-----|------|------|
| **Structured Store（结构化存储）** | PostgreSQL, Redis, SQLite | 通过 key、ID 或 SQL 查询。快速、可预测，适合用户画像、偏好和结构化数据。 |
| **Vector Stores（向量存储）** | Pinecone, Chroma, pgvector | 通过意义查询，"找到与此概念相似的记忆"。对于非结构化笔记和情景回忆至关重要。 |

**检索步骤是瓶颈**。如果你没有检索到正确的记忆，Agent 就会表现得好像它们不存在一样。好的记忆架构是 20% 的存储和 80% 的检索设计。

---

### 2.3 Episodic Memory（情景记忆）

**情景记忆是最被低估的类型。** 当外部记忆存储事实时，情景记忆存储事件——特别是过去行动的结果。

**最简单的形式是结构化日志**：每次 Agent 完成任务时，它记录发生了什么。随着时间的推移，这个日志成为 Agent 在做出决策之前可以查阅的丰富自我知识来源。

**一个 episode 长什么样：**

```json
{
  "episode_id": "ep_20240315_003",
  "timestamp": "2024-03-15T14:23:11Z",
  "task": "将 50 页 PDF 总结为 3 个要点",
  "approach": "顺序分块，每块 2000 tokens",
  "outcome": "success",
  "duration_ms": 4820,
  "token_cost": 12400,
  "quality_score": 0.91,
  "notes": "效果很好。分层分块会更快。",
  "embedding": [0.023, -0.441, 0.182, /* ... 1536 维 */]
}
```

当新任务进来时，Agent 检索语义上最相似的过去 episodes，并使用它们来选择策略。这本质上是从个人历史中进行 few-shot 学习，而不是从手工制作的数据集中学习。

#### 反思循环

```
执行任务 → 记录 Episode → 反思分析 → 提取教训 → 更新策略
```

---

### 2.4 Semantic/Parametric Memory（语义/参数记忆）

**这是模型与生俱来的记忆。** 一切都在训练期间编码到权重中——关于世界的事实、语言模式、推理策略、编码约定和文化知识。

它始终存在。Agent 永远不必检索它。但它有硬性限制：

| 限制 | 说明 |
|-----|------|
| **训练时冻结** | 模型不知道截止日期之后发生了什么 |
| **运行时无法更新** | 你不能在没有重新训练或微调的情况下注入新的永久事实 |
| **不透明** | 你无法确切检查模型"知道"或"不知道"什么 |
| **容易产生幻觉** | 模型用看似合理但错误的补全填补空白 |

**对于任何时间敏感、领域特定或私有的内容，不要依赖参数记忆。使用外部检索。** 参数记忆是当没有更好的来源时，Agent 的通用世界知识的后备。

**正确的思维模型**：参数记忆是 Agent 的通识教育。外部、情景和上下文记忆是 Agent 的在职经验。最好的 Agent 结合两者。

---

## 三、记忆如何在 Agent 循环中流动？

让我们把所有内容放在一起。以下是 Agent 处理请求时每次发生的事情——展示每个记忆系统的运作。

```
用户请求
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Step 1: 记忆检索                                        │
│  ├── 查询 Vector Store 获取相关记忆                      │
│  ├── 查询 Episodic Memory 获取相似过去任务               │
│  └── 构建注入上下文                                      │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: 构建输入                                        │
│  ├── System Prompt + 人格                               │
│  ├── 注入的记忆上下文                                    │
│  └── 当前用户消息                                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: LLM 调用（无状态）                              │
│  └── 模型生成响应                                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Step 4: 记忆写入                                        │
│  ├── 提取值得保存的事实 → External Memory               │
│  ├── 记录 episode → Episodic Memory                     │
│  └── 更新上下文历史 → In-Context Memory                  │
└─────────────────────────────────────────────────────────┘
    │
    ▼
返回响应给用户
```

**注意**：记忆操作包围 LLM 调用：之前检索，之后写入。模型本身是无状态的；记忆系统是赋予有状态、有意识的 Agent 幻觉的东西。

---

## 四、构建记忆层

让我们来构建它。我们将使用 Python 配合 OpenAI 进行嵌入，使用 ChromaDB 作为本地向量存储。相同的概念适用于任何其他技术栈——只需替换库。

### 4.1 安装依赖

```bash
pip install chromadb openai anthropic python-dotenv
```

### 4.2 MemoryStore 类

这个类处理写入记忆（带嵌入）和语义检索。这是其他一切的基础。

```python
import chromadb
from openai import OpenAI
from datetime import datetime
import json, uuid

class MemoryStore:
    """AI Agent 的持久化向量记忆"""
    
    def __init__(self, agent_id: str, persist_dir: str = "./memory_db"):
        self.agent_id = agent_id
        self.openai = OpenAI()
        
        # ChromaDB 将向量存储在磁盘上，跨重启持久化
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=f"agent_{agent_id}_memories",
            metadata={"hnsw:space": "cosine"}  # 余弦相似度
        )
    
    def _embed(self, text: str) -> list[float]:
        """使用 OpenAI 将文本转换为嵌入向量"""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def remember(
        self, 
        content: str, 
        memory_type: str = "general", 
        metadata: dict = None
    ) -> str:
        """存储一条记忆。返回记忆 ID。"""
        memory_id = str(uuid.uuid4())
        embedding = self._embed(content)
        
        meta = {
            "type": memory_type,
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": self.agent_id,
            **(metadata or {})
        }
        
        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[meta]
        )
        return memory_id
    
    def recall(
        self, 
        query: str, 
        k: int = 5, 
        memory_type: str = None,
        min_relevance: float = 0.6
    ) -> list[dict]:
        """检索与查询最相关的 k 条记忆"""
        query_embedding = self._embed(query)
        
        where = {"type": memory_type} if memory_type else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        memories = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            relevance = 1 - dist  # 余弦距离 → 相似度
            if relevance >= min_relevance:
                memories.append({
                    "content": doc,
                    "metadata": meta,
                    "relevance": round(relevance, 3)
                })
        
        return sorted(memories, key=lambda x: x["relevance"], reverse=True)
    
    def forget(self, memory_id: str):
        """删除特定记忆（GDPR 合规、过时数据等）"""
        self.collection.delete(ids=[memory_id])
```

### 4.3 EpisodicLogger 类

现在让我们在顶层添加 episode 日志记录。

```python
from dataclasses import dataclass, asdict
from typing import Optional
import time

@dataclass
class Episode:
    task: str
    approach: str
    outcome: str  # "success" | "partial" | "failure"
    duration_ms: int
    token_cost: int
    quality_score: float  # 0.0 – 1.0，由评估器或用户设置
    notes: str = ""
    error: Optional[str] = None

class EpisodicLogger:
    def __init__(self, memory_store: MemoryStore):
        self.store = memory_store
    
    def log(self, episode: Episode):
        """将 episode 作为可搜索文档保存到记忆中"""
        # 为语义搜索构建丰富的文本表示
        doc = (
            f"Task: {episode.task}\n"
            f"Approach: {episode.approach}\n"
            f"Outcome: {episode.outcome}\n"
            f"Notes: {episode.notes}"
        )
        
        self.store.remember(
            content=doc,
            memory_type="episode",
            metadata={
                "outcome": episode.outcome,
                "quality_score": episode.quality_score,
                "duration_ms": episode.duration_ms,
                "token_cost": episode.token_cost,
            }
        )
    
    def recall_similar(self, task: str, k: int = 3) -> list[dict]:
        """找到与当前任务相似的过去 episodes"""
        return self.store.recall(
            query=task,
            k=k,
            memory_type="episode",
            min_relevance=0.65
        )
```

### 4.4 整合：记忆增强 Agent

```python
import anthropic
from memory.store import MemoryStore
from memory.episodic import EpisodicLogger, Episode
import time

class MemoryAugmentedAgent:
    def __init__(self, agent_id: str):
        self.client = anthropic.Anthropic()
        self.memory = MemoryStore(agent_id)
        self.episodes = EpisodicLogger(self.memory)
    
    def _build_memory_context(self, user_message: str) -> str:
        """检索相关记忆并格式化以便注入"""
        # 语义搜索相关事实
        memories = self.memory.recall(user_message, k=4)
        
        # 相似过去任务的方法
        episodes = self.episodes.recall_similar(user_message, k=2)
        
        context_parts = []
        
        if memories:
            context_parts.append(
                "## 相关记忆\n" + 
                "\n".join([
                    f"- [{m['metadata']['type']}] {m['content']}"
                    f" (相关度: {m['relevance']})"
                    for m in memories
                ])
            )
        
        if episodes:
            context_parts.append(
                "## 过去相似任务\n" + 
                "\n".join([
                    f"- {e['content'][:200]}..."
                    for e in episodes
                ])
            )
        
        return "\n\n".join(context_parts) if context_parts else ""
    
    def run(self, user_message: str) -> str:
        start = time.time()
        
        # 1. 检索相关记忆
        memory_context = self._build_memory_context(user_message)
        
        # 2. 构建带注入记忆的系统提示
        system = """你是一个有帮助的、有记忆的 Agent。
你可以访问来自过去交互的相关上下文。
使用这些上下文给出更好、更个性化的响应。"""
        
        if memory_context:
            system += f"\n\n{memory_context}"
        
        # 3. 调用模型
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user_message}]
        )
        
        answer = response.content[0].text
        duration = int((time.time() - start) * 1000)
        
        # 4. 保存有用信息到记忆以备下次使用
        self.memory.remember(
            content=f"User asked: {user_message[:200]}",
            memory_type="interaction"
        )
        
        # 5. 记录 episode
        self.episodes.log(Episode(
            task=user_message[:200],
            approach="带记忆检索的单轮对话",
            outcome="success",
            duration_ms=duration,
            token_cost=response.usage.input_tokens + response.usage.output_tokens,
            quality_score=1.0,  # 生产环境中来自评估
        ))
        
        return answer
```

---

## 五、向量数据库

它是任何严肃记忆系统的核心。与精确匹配查询（如 SQL）不同，它查找高维空间中向量的最近邻。这就是语义搜索的原理——找到概念上相关的记忆，即使它们没有共享任何词汇。

### 5.1 相似度搜索如何工作

每条记忆都转换为一个向量（使用 OpenAI 的嵌入模型是 1,536 个浮点数的数组）。概念上相似的文本产生相似的向量。当你查询时，你嵌入查询并使用余弦相似度找到最接近的向量。

```python
import numpy as np

def cosine_similarity(a: list, b: list) -> float:
    """
    1.0 = 相同含义
    0.0 = 不相关
    -1.0 = 相反含义
    """
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 示例：这两句话会有很高的相似度
embedding_a = embed("用户偏好深色模式")
embedding_b = embed("他们喜欢界面主题是深色的")
score = cosine_similarity(embedding_a, embedding_b)  # → ~0.91（非常相似）
```

### 5.2 向量数据库选择建议

| 场景 | 推荐 |
|-----|------|
| 本地开发 | ChromaDB |
| 已在 Postgres 上 | pgvector（零额外基础设施） |
| 需要大规模 | Pinecone 或 Qdrant |

---

## 六、记忆管理

真正的记忆系统不仅仅是累积。它们策展。一个不断增长的、没有焦点的存储会随时间退化——检索变得更嘈杂、延迟增加、矛盾的记忆让 Agent 困惑。

**你需要一个遗忘策略。** 以下是三种主要方法：

### 6.1 基于时间的衰减

旧记忆不太相关。通过相关性和时间戳的组合来评分记忆。研究中使用的公式：

```python
import math
from datetime import datetime

def memory_score(
    relevance: float,       # 余弦相似度 0–1
    importance: float,      # 写入时存储 0–1
    created_at: datetime,   # 记忆形成时间
    recency_weight: float = 0.3,
    decay_factor: float = 0.995
) -> float:
    """
    灵感来自 Generative Agents 论文 (Park et al., 2023)。
    平衡：相关性、重要性、时间性。
    """
    hours_old = (datetime.utcnow() - created_at).total_seconds() / 3600
    recency = math.pow(decay_factor, hours_old)
    
    return (
        relevance * 0.4 +
        importance * 0.3 +
        recency * recency_weight
    )
```

### 6.2 写入时的重要性评分

当存储记忆时，让模型为自己的输出评分重要性。只存储高分项目。这从源头过滤噪音。

```python
import re

async def score_importance(client, content: str) -> float:
    """让 LLM 评估信息是否值得保存（0.0 到 1.0）"""
    prompt = f"""评估保存此信息对未来交互的重要性。
    
0.0 = 琐碎（问候）
0.5 = 中等有用
1.0 = 关键（偏好、错误、决策）

信息：{content}

只回复数字。"""
    
    try:
        response = await client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # 提取第一个看起来像浮点数/整数的字符串
        text = response.content[0].text.strip()
        match = re.search(r"[-+]?\d*\.\d+|\d+", text)
        if match:
            score = float(match.group())
            return max(0.0, min(1.0, score))
    except Exception:
        pass
    
    return 0.5  # 默认回退
```

### 6.3 定期合并

运行夜间作业，将重复或高度相似的记忆合并为单个规范摘要。这类似于人类睡眠如何巩固记忆。

```python
async def consolidate_memories(
    store: MemoryStore, 
    similarity_threshold: float = 0.92
):
    """使用向量搜索高效合并近似重复的记忆"""
    all_mems = store.collection.get(
        include=["documents", "embeddings", "ids"]
    )
    
    if not all_mems["ids"]:
        return
    
    visited = set()
    consolidated_docs = []
    
    for i, (mem_id, doc, emb) in enumerate(zip(
        all_mems["ids"],
        all_mems["documents"],
        all_mems["embeddings"]
    )):
        if mem_id in visited:
            continue
        
        # 使用向量存储的内置搜索找到邻居
        # 这比手动嵌套循环快得多
        results = store.collection.query(
            query_embeddings=[emb],
            n_results=10,
            include=["documents", "distances"]
        )
        
        # 识别组成员（1.0 - distance = 余弦相似度）
        group = [doc]
        visited.add(mem_id)
        
        for res_id, res_doc, dist in zip(
            results["ids"][0], 
            results["documents"][0], 
            results["distances"][0]
        ):
            sim = 1.0 - dist
            if res_id != mem_id and res_id not in visited and sim >= similarity_threshold:
                group.append(res_doc)
                visited.add(res_id)
        
        # 处理组
        if len(group) > 1:
            summary = await summarize_group(group)
            consolidated_docs.append(summary)
        else:
            consolidated_docs.append(doc)
    
    # 原子替换：清除并重新填充
    store.collection.delete(where={})
    for doc in consolidated_docs:
        await store.remember(doc)
```

---

## 七、总结

归根结底，**记忆是让 AI 感觉更像伙伴而不是工具的东西**。没有它，每次交互都从零开始。有了它，Agent 可以理解、适应并随时间改进。

**真正的力量不仅仅在于模型**；它在于你如何设计模型记住什么、忘记什么，以及如何使用这些信息。

**把记忆层设计好，其他一切都会变得更聪明。**

---

## 参考

- [Generative Agents Paper (Park et al., 2023)](https://arxiv.org/abs/2304.03442)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [Anthropic Claude API](https://docs.anthropic.com/)

---

*代码由 AI 生成。关注 [@tech_with_ram](https://x.com/tech_with_ram) 获取更多此类文章。*
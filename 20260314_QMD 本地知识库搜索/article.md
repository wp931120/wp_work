# 1.5 万 Star！QMD：完全本地的 AI 知识库搜索引擎，Claude 都爱用

> 📖 **本文解读内容来源**
>
> - **原始来源**：[tobi/qmd - GitHub](https://github.com/tobi/qmd)
> - **来源类型**：GitHub 仓库
> - **作者/团队**：Tobi Lutke (Shopify CEO)
> - **发布时间**：2025 年 12 月开源，2026 年 3 月 v2.0 稳定版
> - **Star 数量**：15,261 ⭐
> - **主要编程语言**：TypeScript (81.5%)、Python (16.7%)

---

## 你有没有经历过这种绝望？

你的电脑里躺着几百个 Markdown 笔记、几十份会议记录、上千页技术文档。

AI 助手问你："请找出所有关于 API 认证的资料。"

你打开了 Spotlight、Everything、甚至 grep... 搜出来 500 个结果。真正有用的那 3 个，藏在某个名为"2024-Q4-规划"的文件夹里。

**更绝望的是：关键词搜不到。** 因为文档里写的是"OAuth 2.0 流程"，而你搜的是"API 认证"。

语义不通，就像鸡同鸭讲。

**QMD 的出现，就是为了解决这个问题。**

用一句话定义：**QMD 是一个完全本地的 Markdown 文档搜索引擎，结合了 BM25 关键词匹配、向量语义搜索和 LLM 重排序三重能力，专为 AI Agent 的知识库检索设计。**

它有多强？看看这些数字：
- **1.5 万 Star**，896 次 Fork，2025 年 12 月开源至今不到 3 个月
- **完全本地运行**，无需 API 密钥，所有模型都是 GGUF 量化版本
- **支持 MCP 协议**，可直接作为 Claude Desktop 的插件使用
- **2.0 稳定版**，提供完整的 SDK API，可嵌入你的 Node.js/Bun 应用

本文我将带你深入 QMD 的代码世界，理解它的核心架构，并用实战示例展示它的威力。

---

## 一、QMD 是什么？为什么它不一样？

要理解 QMD 的价值，先要看懂它在解决什么问题。

### 1.1 传统搜索的局限

你常用的文档搜索工具，大概率是下面两种之一：

**关键词搜索**（如 grep、Spotlight）：
```bash
grep -r "API 认证" ~/docs/
```
问题：**语义鸿沟**。文档写的是"OAuth 2.0"，你搜"API 认证"，搜不到。

**向量搜索**（如各类 RAG 工具）：
```python
# 将文档转为向量，计算余弦相似度
```
问题：**关键词失准**。"如何重置密码"和"密码重置流程"语义相近，但你可能想要的是带"reset_password()" 代码的那篇。

### 1.2 QMD 的解法：三重融合

QMD 不做选择题，它全都要：

```
第一重：BM25 关键词搜索 → 精准匹配术语
第二重：向量语义搜索 → 理解同义表达
第三重：LLM 重排序 → 精细化排序
```

**类比理解**：
- BM25 像是"死记硬背的学霸"——关键词必须匹配
- 向量搜索像是"理解力强的学渣"——大意对得上但细节可能偏
- LLM 重排序像是"阅卷老师"——综合判断哪个答案最符合题意

三者结合，才是终极形态。

下面这张图展示了 QMD 的三重融合搜索机制：

<svg width="100%" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradBM25" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3498DB;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2980B9;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradVec" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2ECC71;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#27AE60;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradRerank" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#C0392B;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow2">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
    <marker id="arrow2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
    </marker>
  </defs>

  <!-- Query Input -->
  <rect x="10" y="70" width="90" height="50" rx="8" fill="#34495e" filter="url(#shadow2)" />
  <text x="55" y="92" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">用户查询</text>
  <text x="55" y="110" text-anchor="middle" fill="#bbb" font-size="11" font-family="system-ui, sans-serif">"API 认证"</text>

  <!-- Arrow to Three Layers -->
  <line x1="100" y1="95" x2="135" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrow2)" />
  <line x1="100" y1="95" x2="135" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrow2)" />
  <line x1="100" y1="95" x2="135" y2="140" stroke="#666" stroke-width="2" marker-end="url(#arrow2)" />

  <!-- BM25 Layer -->
  <rect x="135" y="20" width="110" height="60" rx="8" fill="url(#gradBM25)" filter="url(#shadow2)" />
  <text x="190" y="45" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">BM25</text>
  <text x="190" y="65" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">关键词精准匹配</text>

  <!-- Vector Layer -->
  <rect x="135" y="90" width="110" height="60" rx="8" fill="url(#gradVec)" filter="url(#shadow2)" />
  <text x="190" y="115" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">向量搜索</text>
  <text x="190" y="135" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">语义理解</text>

  <!-- Rerank Layer -->
  <rect x="135" y="160" width="110" height="60" rx="8" fill="url(#gradRerank)" filter="url(#shadow2)" />
  <text x="190" y="185" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">LLM 重排序</text>
  <text x="190" y="205" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">精细化排序</text>

  <!-- Arrows to Fusion -->
  <line x1="245" y1="50" x2="285" y2="80" stroke="#666" stroke-width="2" marker-end="url(#arrow2)" />
  <line x1="245" y1="120" x2="285" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrow2)" />
  <line x1="245" y1="190" x2="285" y2="110" stroke="#666" stroke-width="2" marker-end="url(#arrow2)" />

  <!-- Fusion Center -->
  <circle cx="320" cy="95" r="40" fill="#f39c12" filter="url(#shadow2)" />
  <text x="320" y="90" text-anchor="middle" fill="#fff" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">RRF</text>
  <text x="320" y="108" text-anchor="middle" fill="#fff" font-size="10" font-family="system-ui, sans-serif">融合</text>

  <!-- Arrow to Output -->
  <line x1="360" y1="95" x2="390" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrow2)" />

  <!-- Output -->
  <rect x="390" y="65" width="80" height="60" rx="8" fill="#27ae60" filter="url(#shadow2)" />
  <text x="430" y="90" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">最终</text>
  <text x="430" y="108" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">结果</text>

  <!-- Label -->
  <text x="240" y="185" text-anchor="middle" fill="#999" font-size="11" font-family="system-ui, sans-serif">QMD 三重融合搜索机制</text>
</svg>

### 1.3 为什么 QMD 值得关注？

**理由一：完全本地运行**

不需要调用 OpenAI API，不需要担心数据出境。所有模型都是 GGUF 量化版本，通过 node-llama-cpp 在本地运行。

**理由二：为 AI Agent 而生**

QMD 的 `--json` 和 `--files` 输出格式，是专门为 LLM Agent 设计的。它支持 MCP（Model Context Protocol）协议，可以直接作为 Claude Desktop 的插件使用。

**理由三：意图感知搜索**

QMD 2.0 引入了 `intent` 参数，可以解决"performance"这种歧义查询——你是想查"代码性能优化"，还是"运动表现分析"？intent 会告诉搜索系统你的真实意图。

**理由四：查询文档语法**

支持多行结构化查询：
```
lex: "rate limiting" -redis
vec: 数据库连接池为什么超时
hyde: 假设你是一个 SRE 工程师，你会如何排查连接超时问题
```

三种查询类型组合，既有精度又有召回率。

---

## 二、核心架构：QMD 是如何工作的？

通过阅读源码，我梳理出 QMD 的核心架构。

### 2.1 整体架构图

下面这张图展示了 QMD 从文档输入到最终输出的完整渲染流程：

<svg width="100%" viewBox="0 0 700 420" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#357ABD;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#5CB85C;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#449D44;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradPurple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#9B59B6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8E44AD;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradOrange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F39C12;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#E67E22;stop-opacity:1" />
    </linearGradient>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
    </marker>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Input Documents -->
  <rect x="10" y="20" width="130" height="50" rx="8" fill="url(#gradBlue)" filter="url(#shadow)" />
  <text x="75" y="42" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">Markdown 笔记</text>

  <rect x="10" y="80" width="130" height="50" rx="8" fill="url(#gradBlue)" filter="url(#shadow)" />
  <text x="75" y="102" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">会议记录</text>

  <rect x="10" y="140" width="130" height="50" rx="8" fill="url(#gradBlue)" filter="url(#shadow)" />
  <text x="75" y="162" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">技术文档</text>

  <!-- Arrows to Chunking -->
  <line x1="140" y1="45" x2="190" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />
  <line x1="140" y1="105" x2="190" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />
  <line x1="140" y1="165" x2="190" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />

  <!-- Chunking -->
  <rect x="190" y="70" width="100" height="50" rx="8" fill="url(#gradGreen)" filter="url(#shadow)" />
  <text x="240" y="92" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">文档分块</text>

  <!-- Arrow to Indexing -->
  <line x1="290" y1="95" x2="330" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />

  <!-- Dual Indexing -->
  <rect x="330" y="20" width="110" height="60" rx="8" fill="url(#gradPurple)" filter="url(#shadow)" />
  <text x="385" y="45" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">SQLite FTS5</text>
  <text x="385" y="65" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">BM25 全文索引</text>

  <rect x="330" y="110" width="110" height="60" rx="8" fill="url(#gradPurple)" filter="url(#shadow)" />
  <text x="385" y="135" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">sqlite-vec</text>
  <text x="385" y="155" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">向量存储</text>

  <!-- Arrows to Query -->
  <line x1="440" y1="50" x2="480" y2="75" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />
  <line x1="440" y1="140" x2="480" y2="115" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />

  <!-- Query Processing -->
  <rect x="480" y="70" width="100" height="50" rx="8" fill="url(#gradOrange)" filter="url(#shadow)" />
  <text x="530" y="92" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">查询处理</text>

  <!-- Arrow to Expansion -->
  <line x1="580" y1="95" x2="610" y2="95" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />

  <!-- LLM Expansion -->
  <rect x="610" y="20" width="80" height="50" rx="8" fill="#f39c12" filter="url(#shadow)" />
  <text x="650" y="42" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">LLM 扩展</text>
  <text x="650" y="58" text-anchor="middle" fill="#fff" font-size="10" font-family="system-ui, sans-serif">lex/vec/hyde</text>

  <!-- Arrow to RRF -->
  <line x1="650" y1="70" x2="650" y2="140" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />

  <!-- RRF Fusion -->
  <rect x="610" y="140" width="80" height="50" rx="8" fill="#e74c3c" filter="url(#shadow)" />
  <text x="650" y="162" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">RRF 融合</text>
  <text x="650" y="178" text-anchor="middle" fill="#fff" font-size="10" font-family="system-ui, sans-serif">排序</text>

  <!-- Arrow to Rerank -->
  <line x1="650" y1="190" x2="650" y2="240" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />

  <!-- Reranker -->
  <rect x="610" y="240" width="80" height="50" rx="8" fill="#9b59b6" filter="url(#shadow)" />
  <text x="650" y="262" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">Qwen3</text>
  <text x="650" y="278" text-anchor="middle" fill="#fff" font-size="10" font-family="system-ui, sans-serif">重排序</text>

  <!-- Arrow to Output -->
  <line x1="650" y1="290" x2="650" y2="340" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)" />

  <!-- Output -->
  <rect x="610" y="340" width="80" height="60" rx="8" fill="#27ae60" filter="url(#shadow)" />
  <text x="650" y="365" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">JSON/</text>
  <text x="650" y="380" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">CLI/MCP</text>

  <!-- Label -->
  <text x="350" y="410" text-anchor="middle" fill="#666" font-size="12" font-family="system-ui, sans-serif">QMD 搜索流程图</text>
</svg>

### 2.2 源码中的关键模块

通过阅读仓库结构，我定位到以下核心模块：

| 目录 | 职责 | 关键文件 |
|------|------|----------|
| `src/cli/` | 命令行入口 | `qmd.ts`, `store.ts` |
| `src/mcp/` | MCP Server | `server.ts`, `tools.ts` |
| `src/store/` | 存储和索引 | `schema.ts`, `indexer.ts` |
| `src/search/` | 搜索核心 | `search.ts`, `reranker.ts` |
| `src/embed/` | 嵌入生成 | `embedder.ts` |

### 2.3 核心依赖解析

从 `package.json` 可以看到 QMD 的技术选型：

```json
{
  "dependencies": {
    "better-sqlite3": "^12.4.5",
    "sqlite-vec": "^0.1.7-alpha.2",
    "node-llama-cpp": "^3.17.1",
    "@modelcontextprotocol/sdk": "^1.25.1",
    "fast-glob": "^3.3.0",
    "yaml": "^2.8.2",
    "zod": "4.2.1"
  }
}
```

**关键技术解读**：

- **better-sqlite3**：同步 SQLite 绑定，性能比异步版本更高
- **sqlite-vec**：SQLite 的向量搜索扩展，支持余弦相似度、欧氏距离
- **node-llama-cpp**：llama.cpp 的 Node.js 绑定，运行 GGUF 量化模型
- **@modelcontextprotocol/sdk**：MCP 协议 SDK，实现与 Claude 的集成

### 2.4 搜索流程详解

从源码中梳理出完整的搜索流程：

```typescript
// 简化的搜索流程伪代码
async function search(query: string, options: SearchOptions) {
  // 1. LLM 查询扩展（可选）
  const expanded = await llm.expand(query, { intent: options.intent });
  // 输出：[{ type: 'lex', query: '...' }, { type: 'vec', query: '...' }]

  // 2. 并行执行 BM25 和向量搜索
  const [lexResults, vecResults] = await Promise.all([
    store.searchLex(expanded.lex),
    store.searchVec(expanded.vec),
  ]);

  // 3. RRF 融合排序
  const fusedResults = rrfFuse(lexResults, vecResults, { weights: [2, 1] });

  // 4. LLM 重排序
  const reranked = await reranker.rerank(fusedResults, query);

  // 5. 过滤和格式化
  const filtered = reranked.filter(r => r.score >= options.minScore);

  return formatResults(filtered, options.format);
}
```

这个流程的关键在于：**每一层都有自己的优势，融合之后取长补短**。

---

## 三、实战：用 QMD 构建个人知识库

理论讲完了，来看实战。

### 3.1 安装 QMD

```bash
# 使用 npm 安装（推荐）
npm install -g @tobilu/qmd

# 或使用 Bun
bun install -g @tobilu/qmd

# 或直接运行（无需安装）
npx @tobilu/qmd --version
bunx @tobilu/qmd --version
```

验证安装：
```bash
qmd --version
# 输出：2.0.1
```

**环境要求**：
- Node.js >= 22（Node 25 需要 better-sqlite3 ^12.4.5）
- 如果使用 Bun，QMD 会自动检测并适配

### 3.2 创建你的第一个集合

集合（Collection）是 QMD 管理文档的基本单位。

```bash
# 为你的笔记创建集合
qmd collection add ~/notes --name notes

# 为会议记录创建集合
qmd collection add ~/Documents/meetings --name meetings

# 为工作文档创建集合
qmd collection add ~/work/docs --name docs
```

查看集合列表：
```bash
qmd collection list
```

输出示例：
```
notes      ~/notes                  125 docs
meetings   ~/Documents/meetings      48 docs
docs       ~/work/docs              312 docs
```

### 3.3 添加上下文描述

这是 QMD 的**核心功能**，一定要做！

上下文描述会帮助 LLM 理解每个集合的内容，从而在搜索时做出更好的判断。

```bash
# 为笔记集合添加上下文
qmd context add qmd://notes "个人学习笔记，包括算法、系统设计、编程技巧"

# 为会议记录添加上下文
qmd context add qmd://meetings "团队周会、1:1 沟通、项目评审会议记录"

# 为工作文档添加上下文
qmd context add qmd://docs "REST API 文档、架构设计文档、运维手册"
```

**为什么上下文重要？**

想象你搜索"performance"：
- 在 notes 集合中，可能是"算法性能优化"
- 在 meetings 集合中，可能是"季度绩效评审"
- 在 docs 集合中，可能是"API 响应时间指标"

上下文让 QMD 能够区分这些场景。

### 3.4 生成嵌入（Embedding）

嵌入是将文本转换为向量的过程，这是语义搜索的基础。

```bash
# 为所有集合生成嵌入
qmd embed

# 或为特定集合生成
qmd embed -c notes
```

首次运行时会：
1. 自动下载 GGUF 量化嵌入模型（约 200MB）
2. 遍历所有文档并分块
3. 使用本地 LLM 生成向量嵌入
4. 存储到 SQLite 数据库

**时间参考**：1000 篇文档约需 5-10 分钟（取决于 CPU 性能）

### 3.5 开始搜索

现在可以开始搜索了！

```bash
# 关键词搜索（最快）
qmd search "API 认证"

# 语义搜索（理解同义表达）
qmd vsearch "如何验证用户身份"

# 混合搜索 + 重排序（最佳质量）
qmd query "OAuth 2.0 授权流程"

# 限制结果数量
qmd search "rate limiting" -n 5

# 指定集合搜索
qmd search "数据库连接池" -c docs

# JSON 输出（供 LLM 使用）
qmd search "认证中间件" --json
```

### 3.6 高级查询语法

QMD 2.0 支持结构化查询文档：

创建一个查询文件 `query.txt`：
```
lex: "connection pool" timeout -redis
vec: 数据库连接为什么会在高负载时超时
hyde: 假设你是一个 SRE 工程师，写一篇关于数据库连接超时排查的文档
```

然后运行：
```bash
qmd query --file query.txt
```

**查询类型说明**：

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `lex:` | BM25 关键词搜索 | 精确匹配术语、代码、错误信息 |
| `vec:` | 向量语义搜索 | 理解同义表达、概念性查询 |
| `hyde:` | 假设性文档扩展 | 生成假设性文档，增强召回率 |

**Lex 语法支持**：
```bash
# 精确短语匹配
lex: "rate limiting"

# 排除词
lex: performance -sports -athlete

# 组合使用
lex: "connection pool" timeout -redis -mongodb
```

### 3.7 使用意图参数

意图（intent）是 QMD 2.0 的核心特性。

```bash
# 不带意图的搜索（可能返回歧义结果）
qmd search "performance"

# 带意图的搜索（精准定位）
qmd search "performance" --intent "Node.js 应用性能优化和 CPU 调优"
```

**意图如何影响搜索？**

意图参数会贯穿整个搜索流程：

1. **查询扩展**：LLM 根据意图生成更精准的子查询
2. **BM25 搜索**：意图关键词以 0.5× 权重参与评分
3. **重排序**：Qwen3-Reranker 会考虑意图与结果的相关性
4. **片段提取**：倾向于提取与意图相关的片段

**实际效果对比**：

不带意图：
```
1. 运动表现分析指南.md (score: 0.85)
2. 季度绩效评审流程.md (score: 0.78)
3. API 性能优化最佳实践.md (score: 0.72)
```

带意图（"Node.js 应用性能优化"）：
```
1. API 性能优化最佳实践.md (score: 0.92)
2. Node.js CPU 调优指南.md (score: 0.88)
3. 数据库查询性能分析.md (score: 0.75)
```

---

## 四、与 AI Agent 集成

QMD 的真正威力，在于与 AI Agent 的无缝集成。

### 4.1 作为 MCP Server 使用

MCP（Model Context Protocol）是 Anthropic 推出的协议，让 AI 助手能够访问外部工具。

**Claude Desktop 配置**：

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

**Claude Code 配置**：

```bash
# 推荐：使用插件市场
claude plugin marketplace add tobi/qmd
claude plugin install qmd@qmd

# 或手动配置
# 编辑 ~/.claude/settings.json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

配置完成后，Claude 就可以直接使用 QMD 搜索你的知识库了。

**示例对话**：

```
你：帮我找一下关于 OAuth 2.0 的文档

Claude: [使用 qmd_query 工具搜索]
        找到了 5 篇相关文档：
        1. OAuth 2.0 授权流程详解 (docs/api-auth.md)
        2. JWT 令牌验证中间件实现 (docs/middleware/jwt.ts)
        3. ...
```

### 4.2 HTTP 模式（推荐生产环境）

默认的 stdio 模式每次都会启动新进程，模型需要重新加载。

HTTP 模式可以保持模型常驻内存：

```bash
# 启动 HTTP 服务器（默认端口 8181）
qmd mcp --http

# 自定义端口
qmd mcp --http --port 8080

# 后台运行（守护进程）
qmd mcp --http --daemon

# 查看状态
qmd status

# 停止后台服务
qmd mcp stop
```

**HTTP 服务器暴露的端点**：
- `POST /mcp` — MCP Streamable HTTP 协议
- `GET /health` — 健康检查

**优势**：
- 模型保持加载状态，跨请求复用
- 嵌入/重排序上下文在 5 分钟空闲后才会释放
- 下一个请求只需约 1 秒重新加载

### 4.3 SDK 库模式

QMD 2.0 提供了完整的 SDK API，可以在你的应用中直接使用。

**安装**：
```bash
npm install @tobilu/qmd
```

**快速开始**：

```typescript
import { createStore } from '@tobilu/qmd'

const store = await createStore({
  dbPath: './my-index.sqlite',
  config: {
    collections: {
      docs: { path: '/path/to/docs', pattern: '**/*.md' },
    },
  },
})

// 搜索
const results = await store.search({
  query: "authentication flow",
  limit: 5,
  minScore: 0.3,
})

console.log(results.map(r =>
  `${r.title} (${Math.round(r.score * 100)}%)`
))

await store.close()
```

**SDK 支持的操作**：

```typescript
// 集合管理
await store.addCollection("notes", { path: "~/notes" })
await store.listCollections()
await store.removeCollection("notes")

// 上下文管理
await store.addContext("docs", "/api", "REST API 文档")
await store.setGlobalContext("内部工程文档")
await store.listContexts()

// 文档检索
const doc = await store.get("docs/readme.md")
const body = await store.getDocumentBody("docs/readme.md", {
  fromLine: 50,
  maxLines: 100,
})
const { docs, errors } = await store.multiGet("docs/**/*.md")

// 搜索
const lexResults = await store.searchLex("auth middleware")
const vecResults = await store.searchVector("how users log in")
const expanded = await store.expandQuery("auth flow")
```

---

## 五、效果展示

### 5.1 CLI 输出示例

```bash
$ qmd query "OAuth 2.0 授权流程"

Querying... (3.2s)

Results:
─────────────────────────────────────────────────────────────
1. OAuth 2.0 授权流程详解 (docs/api-auth.md)
   分数：92% | 集合：docs
   上下文：REST API 文档
   片段：
   Line 45: OAuth 2.0 定义了四种授权模式：
   Line 46: - Authorization Code: 服务端应用首选
   Line 47: - Implicit: 单页应用（已不推荐）
   Line 48: - Resource Owner Password: 遗留系统
   Line 49: - Client Credentials: 机器对机器通信

2. JWT 令牌验证中间件实现 (docs/middleware/jwt.ts)
   分数：87% | 集合：docs
   上下文：REST API 文档
   片段：
   Line 12: // 验证 OAuth 2.0 access token
   Line 13: export function authMiddleware(req, res, next) {
   Line 14:   const token = extractBearerToken(req.headers);
   Line 15:   const payload = verifyJWT(token, PUBLIC_KEY);
   ...

3. 第三方登录集成指南 (docs/integrations/social-login.md)
   分数：79% | 集合：docs
   片段：
   Line 23: 使用 Google OAuth 2.0 需要以下步骤：
   Line 24: 1. 在 Google Cloud Console 创建 OAuth 客户端
   Line 25: 2. 配置重定向 URI
   ...
```

### 5.2 JSON 输出示例（供 LLM 使用）

```bash
$ qmd search "认证中间件" --json
```

```json
[
  {
    "docid": "#abc123",
    "path": "docs/middleware/jwt.ts",
    "displayPath": "docs/middleware/jwt.ts",
    "title": "JWT 令牌验证中间件实现",
    "score": 0.87,
    "collection": "docs",
    "context": "REST API 文档",
    "snippet": "// 验证 OAuth 2.0 access token\nexport function authMiddleware...",
    "matchedLines": [12, 13, 14, 15]
  },
  {
    "docid": "#def456",
    "path": "docs/api-auth.md",
    "displayPath": "docs/api-auth.md",
    "title": "OAuth 2.0 授权流程详解",
    "score": 0.79,
    "collection": "docs",
    "context": "REST API 文档",
    "snippet": "OAuth 2.0 定义了四种授权模式...",
    "matchedLines": [45, 46, 47, 48, 49]
  }
]
```

### 5.3 性能对比

| 搜索类型 | 响应时间 | 适用场景 |
|----------|----------|----------|
| `qmd search` (BM25) | < 0.1s | 快速关键词匹配 |
| `qmd vsearch` (向量) | 1-2s | 语义理解 |
| `qmd query` (混合 + 重排序) | 3-5s | 最佳质量 |

**模型加载时间**（首次查询）：
- 嵌入模型加载：约 2-3 秒
- 重排序模型加载：约 1-2 秒
- 后续查询：模型保持加载状态

---

## 六、深度思考：QMD 的未来在哪里？

### 6.1 技术趋势判断

通过分析源码和更新日志，我看到几个趋势：

**1. 本地 AI 是确定性方向**

QMD 完全本地运行的设计理念，反映了隐私保护和数据主权意识的提升。

- 所有模型都是 GGUF 量化版本
- 通过 node-llama-cpp 在本地运行
- 无需 API 密钥，无需担心数据出境

**2. 意图感知搜索是差异化优势**

1.1.5 版本引入的 `intent` 参数，是一个重要的差异化特性。

```typescript
// 意图参数贯穿整个搜索流程
const results = await store.search({
  query: "performance",
  intent: "Node.js 应用性能优化和 CPU 调优",  // <-- 关键
})
```

这个设计解决了传统搜索的歧义问题，让搜索结果更精准。

**3. MCP 协议是 Agent 集成的标准**

QMD 对 MCP 协议的支持，让它能够无缝集成到 Claude 生态中。

- Claude Desktop：作为插件使用
- Claude Code：作为命令行工具
- 其他 MCP 客户端：通过 HTTP 模式连接

### 6.2 与同类工具对比

| 特性 | QMD | Elasticsearch | Meilisearch | LangChain RAG |
|------|-----|---------------|-------------|---------------|
| 本地运行 | ✅ 完全本地 | ⚠️ 需要服务器 | ⚠️ 需要服务器 | ⚠️ 依赖 API |
| 向量搜索 | ✅ 内置 | ⚠️ 需插件 | ⚠️ 需插件 | ✅ 内置 |
| LLM 重排序 | ✅ 内置 | ❌ | ❌ | ⚠️ 需配置 |
| MCP 支持 | ✅ | ❌ | ❌ | ❌ |
| 部署复杂度 | 低 | 高 | 中 | 中 |
| 适用场景 | 个人/小团队 | 企业级 | 中小规模 | AI 应用 |

### 6.3 笔者的判断

**我强烈看好 QMD 的发展**，理由如下：

**理由一：作者背景强大**

Tobi Lutke 是 Shopify 的 CEO，这意味着：
- 技术视野开阔，能看到别人看不到的机会
- 资源充足，可以持续投入
- 工程能力强，代码质量有保障

**理由二：赛道正确**

本地知识库检索是 AI Agent 的刚需：
- 1.5 万 Star 证明市场需求
- 2025 年 12 月开源，不到 3 个月快速迭代到 2.0
- 社区贡献积极（13+ PRs）

**理由三：技术务实**

QMD 不追求端到端大模型，而是采用组合拳：
- BM25 保证关键词精度
- 向量搜索保证语义召回
- Reranker 精细化排序

这种设计性价比高，效果可控。

**理由四：生态加持**

- MCP 协议支持，成为 Claude 官方插件
- SDK API 完整，可嵌入任意 Node.js/Bun 应用
- 社区活跃，问题响应快

**潜在挑战**：

- 本地模型质量依赖 GGUF 量化，相比云端 API 有精度损失
- 需要用户自己维护索引，对非技术用户有一定门槛
- 竞争对手多（Elasticsearch、Meilisearch 等）

---

## 七、避坑指南

根据 CHANGELOG 和源码分析，这些坑要注意：

### 7.1 Node 版本要求

```bash
# ❌ Node < 22 不支持
node --version  # v18.x 会失败

# ✅ Node >= 22
node --version  # v22.x 或 v25.x
```

**解决方案**：使用 nvm 升级 Node 版本

### 7.2 Bun 安装 ABI 不匹配

```bash
# ❌ 直接安装可能失败
bun install -g @tobilu/qmd

# ✅ QMD 2.0 的 bin 包装器会自动检测
# 但如果遇到问题，使用 npx 运行
npx @tobilu/qmd --version
```

### 7.3 sqlite-vec 平台兼容性

不同平台需要不同的预编译包：

```bash
# macOS ARM (M1/M2/M3)
npm install sqlite-vec-darwin-arm64

# macOS Intel
npm install sqlite-vec-darwin-x64

# Linux x64
npm install sqlite-vec-linux-x64

# Windows x64
npm install sqlite-vec-windows-x64
```

### 7.4 长文档截断

超过 2048 token 的 chunk 会被截断：

```bash
# ❌ PDF 导入的长文档可能影响排序
qmd collection add ~/pdf-docs --name pdfs

# ✅ 建议预处理，分段导入
# 或使用 --chunk-size 参数（如果支持）
```

### 7.5 GPU 初始化失败

```bash
# ❌ 手动配置 GPU 可能失败
# ✅ QMD 2.0 使用 autoAttempt 自动回退
# 无需手动配置，失败会自动使用 CPU
```

---

## 结语

QMD 是我近年来见过的最务实的本地搜索工具之一。

它解决了 AI 时代的一个核心痛点：**如何让 AI 助手准确找到你知识库中的资料**。

如果你经常需要：
- 在大量笔记和文档中查找资料
- 为 AI Agent 提供知识库检索能力
- 构建私人的、本地运行的搜索引擎

那么 QMD 值得你投入时间。

**最后送上一句话**：

> 好的工具不是让你做更多的事，而是让你用更少的事做出更好的结果。

QMD 就是这样的工具。

---

## 参考资源

- **官方仓库**：https://github.com/tobi/qmd
- **作者**：Tobi Lutke (@tobi) - Shopify CEO
- **Star 数量**：15,261 ⭐（截至 2026-03-14）
- **主要语言**：TypeScript (81.5%)
- **最新版本**：v2.0.1（2026-03-10）
- **文档**：仓库 README.md 和 CHANGELOG.md

---

*本文基于对 QMD 官方仓库的深度阅读撰写，所有分析基于公开源码。*
*欢迎在评论区交流讨论！*

# 让 AI Agent 学会自我进化——MetaClaw 实战

> 📖 **信息来源**
>
> - [MetaClaw GitHub 仓库](https://github.com/aiming-lab/MetaClaw)
> - 团队：aiming-lab
> - Stars：1,044+ | 语言：Python

---

## 这是个啥

如果你的 AI Agent 能像人一样，从每次对话里学习进化，那会怎样？

不用收集数据，不用训练模型，不用 GPU 集群。你只管跟它聊天，它自己就会越来越聪明。

MetaClaw 就是一个这样的框架。它让 Agent 从真实对话里学习，而不是靠离线训练。

![MetaClaw 架构图](https://raw.githubusercontent.com/aiming-lab/MetaClaw/main/assets/metaclaw.gif)

---

## 核心原理

### 它是怎么做到的

MetaClaw 就三步：

1. **技能注入**：每次对话前，从技能库里挑出相关的技能塞给 LLM
2. **奖励打分**：对话结束后，用另一个 LLM 给回答打分
3. **后台进化**：分数低的送去训练，分数高的变成新技能

听着像强化学习？确实像。但 MetaClaw 多了个**智能调度器**。

### MadMax 模式：智能调度器

默认的 MadMax 模式，只在三种情况下触发权重更新：

- **睡眠时间**：你睡觉的时候（比如 23:00-07:00）
- **系统空闲**：键盘鼠标 30 分钟没动静
- **开会时间**：Google Calendar 显示你在开会

状态机就一行：

```
IDLE_WAIT → WINDOW_OPEN → UPDATING → PAUSING → IDLE_WAIT
```

趁你不用，偷偷变强。

---

## 三种运行模式

| 模式 | 功能 | 需要 GPU 吗 |
|------|------|-----------|
| **skills_only** | 技能注入 + 自动总结 | 不需要 |
| **rl** | Skills + RL 训练 (GRPO) | 需要 |
| **madmax** (默认) | Skills + RL + 智能调度 | 需要 |

怎么选：

- 快速体验：`skills_only` 就够了
- 有 GPU 想深度玩：直接上 `madmax`
- 中间态：`rl` 模式能训练，但没有智能调度

---

## 代码实战

### 安装

```bash
# 基础安装（仅技能模式）
pip install -e .

# 完整安装（推荐）
pip install -e ".[rl,evolve,scheduler]"
```

### 配置

```bash
# 首次配置（交互式向导）
metaclaw setup
```

配置文件在 `~/.metaclaw/config.yaml`：

```yaml
mode: madmax

llm:
  provider: kimi
  model_id: moonshotai/Kimi-K2.5
  api_base: https://api.moonshot.cn/v1
  api_key: sk-...

skills:
  enabled: true
  dir: ~/.metaclaw/skills
  retrieval_mode: template
  top_k: 6
  auto_evolve: true

rl:
  enabled: false
  backend: auto
  model: moonshotai/Kimi-K2.5
  lora_rank: 32
  batch_size: 4

scheduler:
  sleep_start: "23:00"
  sleep_end: "07:00"
  idle_threshold_minutes: 30
  calendar:
    enabled: false
```

### 启动

```bash
# 默认 madmax 模式
metaclaw start

# 或者指定模式
metaclaw start --mode rl
metaclaw start --mode skills_only
```

### 连接 OpenClaw

MetaClaw 是个 Proxy，要配合 OpenClaw 用：

```bash
# 另开一个终端启动 OpenClaw
openclaw start

# 然后正常对话
# MetaClaw 会在后台拦截对话，注入技能，收集训练数据
```

---

## 技能长什么样

MetaClaw 预置了 40+ 个技能，覆盖编码、安全、Agent 任务等。

技能文件是 Markdown 格式：

```markdown
---
name: task-decomposition
description: Use this skill when a user presents a large, vague goal...
category: productivity
---

# Task Decomposition

Before starting a large goal, decompose it.

**Steps:**
1. Restate the end goal in one sentence.
2. List the concrete sub-tasks needed to reach it, in order.
3. For each sub-task, estimate effort (S/M/L).
4. Propose a timeline with milestones.
```

预置技能包括：

- `task-decomposition`：任务分解
- `codebase-navigation`：代码库导航
- `git-workflow`：Git 工作流
- `secrets-management`：密钥管理
- `structured-logging-and-observability`：结构化日志
- `test-before-ship`：发布前测试
- `verify-before-irreversible-action`：不可逆操作前验证

---

## 效果展示

GitHub Demo 视频里的几个镜头：

1. **技能自动注入**：用户问"帮我部署这个服务"，Agent 自动调用 `test-before-ship` 技能，先测试再部署
2. **失败案例总结**：某次回答得分低，系统自动提取新技能"部署前先检查环境变量"
3. **权重热更新**：训练完成后，不用重启，新权重直接生效

![MetaClaw Demo](https://github.com/user-attachments/assets/d86a41a8-4181-4e3a-af0e-dc453a6b8594)

Agent 的行为确实会越来越符合用户习惯。

---

## 核心架构

组件关系图：

```mermaid
graph TB
    A[用户] --> B[OpenClaw]
    B --> C[MetaClaw Proxy]
    C --> D[LLM API]

    C --> E[Skill Manager<br/>技能检索注入]
    C --> F[PRM Scorer<br/>奖励打分]
    C --> G[Rollout<br/>数据收集]

    G --> H[Trainer<br/>RL 训练]
    H --> I[Scheduler<br/>智能调度]

    I --> J[空闲检测]
    I --> K[Google Calendar]

    style C fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style E fill:#764ba2,stroke:#333,stroke-width:1px,color:#fff
    style F fill:#764ba2,stroke:#333,stroke-width:1px,color:#fff
    style H fill:#f093fb,stroke:#333,stroke-width:1px,color:#fff
    style I fill:#f5576c,stroke:#333,stroke-width:1px,color:#fff
```

---

## 一些思考

### 独特价值在哪

MetaClaw 的核心价值不在"能学习"，而在**学习时机智能**。

其他 Agent 框架也能强化学习，但有几个问题：

- 训练会打断服务
- 用户不知道 Agent 在变强
- 推理和训练抢 GPU

MetaClaw 的调度器解决了：**趁你不用，偷偷进化**。

### 和同类方案对比

| 方案 | 学习方式 | 需要训练吗 | 打断服务吗 |
|------|---------|-----------|-----------|
| **MetaClaw** | 元学习 + RL | 可选 | 不打断 |
| 传统微调 | 离线训练 | 必须 | 是 |
| Prompt 工程 | 人工优化 | 不需要 | - |
| RAG | 检索增强 | 不需要 | - |

个人 Assistant 场景，MetaClaw 很合适。

企业级服务、对稳定性要求极高的，`skills_only` 模式更稳妥。

### 局限性

MetaClaw 目前的几个限制：

1. **依赖 OpenClaw**：必须配合 OpenClaw 使用，不是独立 Agent
2. **调度器需要配置**：Google Calendar 集成要额外授权
3. **RL 训练成本高**：madmax 模式需要 GPU，云端 Tinker 也要钱
4. **技能质量不稳定**：自动总结的技能有时不够精准

### 我的判断

MetaClaw 代表了一个正确方向：**Agent 不应该是一次性部署的死物，而应该是持续进化的活物**。

虽然现在还需要 GPU、需要配置、需要依赖 OpenClaw，但思路是对的。

就像人一样，不是出生时就定型了，而是在每一天的经历里，慢慢变成更好的自己。

---

## 结语

MetaClaw 把"元学习"这个学术概念，变成了普通人能用的工具。

打个比方：

> GAN 像梅西和 C 罗，正因对手存在才互相促进。
> MetaClaw 像你的私人教练，你训练它，它也训练你。

真正的智能，不是静态的知识，而是动态的进化能力。

如果你的 Agent 也能越用越聪明，那会是种什么体验？

---

### 参考

- [MetaClaw GitHub 仓库](https://github.com/aiming-lab/MetaClaw)
- [OpenClaw 核心框架](https://github.com/openclaw-lab/openclaw)
- [SkillRL 技能增强框架](https://github.com/SkillRL/SkillRL)
- [Tinker 云端 RL 训练](https://github.com/aiming-lab/tinker)

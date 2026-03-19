# 用文件夹养一群 AI 员工：MCP + Markdown 的 Agent 构建心法

> 📖 **本文解读内容来源**
>
> - **原始来源**：[The Startup Ideas Podcast - Turn Folders Into a Full AI Team](https://open.spotify.com/episode/361XxtzIMv7DAbMQP7Pjza)
> - **来源类型**：播客内容整理
> - **发布时间**：2026年3月

你有没有想过，把 AI 变成你的「数字员工」，而不是一个只会回答问题的聊天机器人？

Remy Gaskill 在 The Startup Ideas Podcast 里分享了一套方法论：**用文件夹 + Markdown 文件，构建一整支 AI 团队**。不需要写代码，只要会写文档。

这套方法的核心洞察：**Chat 是"你问我答"，Agent 是"你给目标，它出结果"**。

## 从 Chat 到 Agent：思维模式的根本转变

大多数人用 AI 的方式还停留在第一阶段：问一个问题，得到一个答案，然后自己去做事。

这叫 **Chat**。Chat 是乒乓球——你打过去，它打回来。

**Agent** 不一样。你给 Agent 一个目标，它自己规划步骤，自己执行，自己交付结果。

Remy 把它总结为：**"question to answer" vs "goal to result"**。

用 Agent 的人和不用的人，效率差距是 10-20 倍。这不是夸张——一个能自动完成"调研-写稿-发邮件-更新 Notion"的 Agent，和一个只会回答问题的聊天机器人，完全是两个物种。

## Agent 的底层循环：Observe → Think → Act

所有 Agent 都运行在同一个三步循环上：**观察（Observe）→ 思考（Think）→ 行动（Act）**。

举个例子：你让 Agent 帮你"建一个 Greg Eisenberg 的作品集网站"。

1. **观察**：检查工作区有没有现成文件
2. **思考**：发现没有，决定先调研 Greg Eisenberg
3. **行动**：去搜索、读资料

然后循环继续：有了调研结果 → 思考"需要一个计划" → 写计划 → 循环 → 写代码 → 循环 → 部署网站 → 循环 → 截图验证完成。

Agent 会一直循环，直到确认任务完成。

Claude Code、Codex、Cowork、Manus……这些"Agent Harnesses"（Agent 框架）本质上都在跑这个循环。学会一个，其他的就像学会开车后换辆车——油门刹车方向盘都一样，只是配置不同。

## Step 01：给 Agent 一个大脑——agents.md

先在电脑上创建一个文件夹，比如叫"executive_assistant"。

这时候文件夹是空的。你让 Agent 写一封冷邮件，它完全不知道你是谁、卖什么、目标客户是谁。

解决方案：创建一个 **agents.md** 文件。

这个文件就是 Agent 的**系统提示词（System Prompt）**。每次任务开始前，Agent 会先读这个文件。

里面放什么？你的角色、业务背景、偏好设置、常用工具、工作习惯。

不同框架叫法不一样：
- Claude Code → `claude.md`
- Codex / OpenClaw → `agents.md`
- Gemini → `gemini.md`

核心逻辑一样：**一个 Markdown 文件，给 Agent 提供上下文**。

**Pro tip**：你可以用任何聊天模型帮你构建这个文件。直接说："用面试的方式问我问题，提取所有必要的上下文，然后帮我生成一个 agents.md 文件"。它会帮你把脑子里的东西都挖出来，结构化整理。

这就是从**提示词工程（Prompt Engineering）**到**上下文工程（Context Engineering）**的转变。把 Agent 喂饱足够的业务背景，你的提示词可以简单到只要一句"帮我写一封冷邮件"。

## Step 02：给 Agent 一个记忆——memory.md

ChatGPT 有自动记忆功能，会在云端保存你的偏好。但 Agent 不一样——**你自己控制记忆**。

实现方法：在 agents.md 里加两行指令：

```
- 每次任务开始前，读取 memory.md
- 当我纠正你或学到新东西时，更新 memory.md
```

然后在同一文件夹下创建一个空的 memory.md 文件。

现在，当你说"别写这么正式"，Agent 会自动在 memory.md 里记录"保持口语化风格，不要正式"。之后的每次对话都会继承这个偏好。

**好员工会记住你的偏好并持续改进，你的 Agent 也应该这样。**

最佳实践：agents.md 控制在 200 行以内。如果 memory.md 开始保存琐碎的细节，就更新指令让它只保存"有实质意义的纠正"。

## Step 03：连接工具——MCP

默认情况下，大多数 Agent 框架只带一个网页搜索功能。就这。

要连接 Gmail、Google Calendar、Notion、Stripe、Granola……你需要 **MCP（Model Context Protocol）**。

最简单的理解方式：没有 MCP 之前，Agent 要学每个工具的"语言"——Claude 说英语，Notion 说西班牙语，Gmail 说法语，Slack 说中文。连接它们需要定制开发。

Anthropic 开发了 MCP 作为**通用翻译器**。Agent 还是说英语，工具还是说各自的方言，MCP 在中间双向翻译。

现在大多数框架都做得很简单：Cowork、Codex、Manus、Perplexity 都有"连接器"或"技能"菜单，点击登录即可。

Remy 现场演示：他让一个 Agent 总结收件箱、从 Granola 拉会议笔记、创建 Stripe 支付链接、在 Notion 建项目、草拟跟进邮件——一个提示词，Agent 自动调用所有工具，Remy 完全不用切换标签页。

"哪怕只是把一件事提速 7 倍，不需要在各种工具之间跳来跳去，效果就开始复利了。"

## Step 04：构建 Skills——AI 的 SOP

**Skills 是复利引擎。**

把 Skill 想象成 Agent 的**标准作业流程（SOP）**。你把一个流程讲清楚一次，Agent 就能每次完美复现。

没有 Skill：你让 Agent 写客户提案。来回调整 30 分钟——改格式、把价格放到最下面、用这个蓝色……终于满意了。下周，从头再来。

有 Skill：Agent 加载你的提案 Skill。它已经知道格式、颜色、价格位置。几分钟搞定。

**两种创建 Skill 的方法：**

1. **喂素材**：Remy 把一个病毒式 Hook 课程的全文本上传，让 Agent"基于这个课程帮我建一个病毒式 Hook 的 Skill"。Agent 自动打包成 .skill 文件。
2. **从实战中提取**：跟 Agent 走一遍流程，满意后说"把我们刚才做的事建成一个 Skill"。它自动打包整个工作流。

Remy 的真实案例：他建了一个广告库分析 Skill——抓竞品广告、截图落地页、分析文案和创意、生成主报告。以前要 3-4 小时，现在打两个字就跑。

**如果你每周自动化 3-5 个小流程，最终会自动化整个工作流。**

## Step 05：链式技能 + 定时任务

Skills 真正强大是在**组合**的时候。

- 会议准备 Skill：调研嘉宾、整理谈话要点
- 播客调研 Skill：深挖嘉宾背景
- 早报 Skill：检查日历，发现播客录制，自动触发调研 Skill

大多数框架现在支持**定时任务**。设置早报 Skill 每天早上 9 点运行：查日历、总结收件箱、拉 Notion 项目更新、给出当日作战计划。

Remy 的真实案例：他在买一辆特定颜色和配置的车。每 3 小时，一个 Agent 自动抓取 CarMax、Cars.com、Autotrader 等平台，有匹配的就推送通知。省下了每天疯狂刷新标签页的一小时。

## 文件夹结构：一整套 AI 员工

Remy 的完整配置：

一个公司或客户一个大文件夹。里面按部门建子文件夹：executive_assistant、content_team、head_of_marketing、sales。

每个子文件夹有自己的 agents.md、memory.md、skills 文件夹、MCP 连接。营销 Agent 知道广告创意规则，内容 Agent 知道品牌调性，行政助理知道你怎么签邮件。

最顶层，一个总管 Agent 管理它们全部。

**全局 vs 项目级**：有些 Skill 到处适用（比如"写短一点"），放全局。有些只属于特定角色（比如"把人转给 Sebastian"），放项目文件夹。

## 从哪里开始？

1. 选一个 Agent 框架（新手推荐 Cowork）
2. 创建一个叫"executive_assistant"的文件夹
3. 用面试式提示词构建 agents.md
4. 加一个带自更新指令的 memory.md
5. 通过 MCP 连接你最常用的工具
6. 用 Agent 做真实任务。重复的流程，就建成 Skill
7. 每周自动化 3-5 个小流程

**真正抗迭代的资产是电脑里的 Markdown 文件。** 框架会换，你的上下文、记忆、Skill 可以无缝迁移到任何一个。

## 笔者的观点

**1. 从提示词工程到上下文工程，是 AI 应用的必经之路**

大多数人还在纠结"怎么写一个完美的 Prompt"，但真正的高手已经开始"喂 Agent 业务上下文"。当你把业务背景、偏好、工作习惯都沉淀成 Markdown 文件，Prompt 就可以简单到一句话。**重剑无锋，大巧不工。**

**2. Markdown 是 AI 资产的最可移植形式**

今天的 Agent 框架（Claude Code、Codex、Cowork）可能不是明天的主流。但你的 agents.md、memory.md、skills 文件是纯文本，可以迁移到任何框架。**技术会迭代，资产要可移植。**

**3. Skills 是 AI 时代的"代码复用"**

程序员用函数和模块实现复用，普通人用 Skills。每一个 Skill 都是你工作流的一次"打包"，用一次赚一次。**复利是普通人最强的杠杆。**

**4. 学会遗忘，才能走得更远**

memory.md 不是什么都记，而是记"有实质意义的纠正"。Agent 的上下文空间有限，和人脑一样——记住最重要的，忘掉噪音。**记住核心，轻装前行。**

---

### 参考

- [The Startup Ideas Podcast - Spotify](https://open.spotify.comepisode/361XxtzIMv7DAbMQP7Pjza)
- [The Startup Ideas Podcast - YouTube](https://www.youtube.com/watch?v=eA9Zf2-qYYM)

这套方法论的核心：**连接工具 → 构建上下文 → 创建 Skills → 自动化流程 → 循环迭代**。

你不是在取代自己，而是在压缩杂事，把时间留给真正重要的决策。

从行政助理开始，这周建一个 Skill，下周再建一个。几个月后，你会把一周的工作压缩到一天。
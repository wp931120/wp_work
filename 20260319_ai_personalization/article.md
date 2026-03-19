# 让 AI 真正认识你：用三个文件构建超个性化系统

> 📖 **本文解读内容来源**
>
> - **原始来源**：[How I built a hyper-personalization system with AI - Josh Pigford](https://everydayisayear.ai/p/how-i-built-a-hyper-personalization)
> - **来源类型**：技术博客 / Newsletter
> - **作者**：Josh Pigford（@Shpigford）
> - **发布时间**：2026年3月18日

你的 AI 知道你老婆的生日吗？知道你每天早上几点起床、周末爱干什么、最讨厌听什么词吗？

如果你用的是 ChatGPT 或 Claude 的默认记忆功能，答案大概率是：不知道。每次对话，都像第一次见面。

Josh Pigford 是个连续创业者，他做了一件看似"返璞归真"的事——用纯文本文件，让 AI 真正认识他。不是什么黑科技，就是 Markdown 文件。但效果惊人。

## 行业在追错的东西

AI 行业每周都在发新模型。更强的推理能力、更大的上下文窗口、更快的响应速度。

但有一个问题几乎没人解决：**让 AI 认识使用它的人**。

ChatGPT 的记忆功能是个玩具。Claude 的记忆聊胜于无。每次对话，你都得重新介绍自己："我是一个程序员，我喜欢简洁的代码风格，不要写太多注释……"

这不是智能助手，这是失忆症患者。

Josh 的洞察很犀利：**模型已经足够聪明了，它们只是不知道关于你的任何事**。

## 三个文件，解决核心问题

Josh 的系统架构出奇简单：

- **USER.md**：你是谁。姓名、位置、时区、日程、工作背景、家庭概况、兴趣爱好、食物偏好、沟通风格。一切让助手不再像个陌生人的信息。Josh 的文件大约 80 行。
- **MEMORY.md**：AI 学到了什么。不是原始日志，而是提炼过的洞察——你的工作方式、你做的决策、你学到的教训、你表达过的观点。AI 每次会话前读取，学到新东西时更新。
- **brain/family/**：每个家人一个文件。生日、关系、偏好、礼物点子、备注。老婆有、孩子有、连孙女都有。节日、生日、送礼话题来的时候，AI 能直接引用。

三个概念。纯文本。能配合任何支持系统提示词或文件上下文的 AI 工具。

下面这张图展示了整个系统的架构：

<svg width="100%" viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="fileGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1d4ed8;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="fileGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#10b981;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#059669;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="fileGrad3" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#f59e0b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#d97706;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.15"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="700" height="400" fill="#0f172a"/>

  <!-- AI 大脑 -->
  <rect x="275" y="30" width="150" height="60" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="350" y="58" text-anchor="middle" fill="#fff" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">AI 助手</text>
  <text x="350" y="78" text-anchor="middle" fill="#e0e7ff" font-size="12" font-family="system-ui, sans-serif">每次会话前读取</text>

  <!-- 箭头 -->
  <path d="M350 90 L350 130" stroke="#6366f1" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#6366f1"/>
    </marker>
  </defs>

  <!-- 文件夹容器 -->
  <rect x="50" y="140" width="600" height="220" rx="16" fill="#1e293b" stroke="#334155" stroke-width="2"/>

  <!-- 文件夹标签 -->
  <text x="350" y="170" text-anchor="middle" fill="#94a3b8" font-size="14" font-family="system-ui, sans-serif">📁 你的个人知识库</text>

  <!-- USER.md -->
  <rect x="80" y="200" width="160" height="130" rx="10" fill="url(#fileGrad1)" filter="url(#shadow)"/>
  <text x="160" y="230" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">USER.md</text>
  <text x="160" y="255" text-anchor="middle" fill="#bfdbfe" font-size="11" font-family="system-ui, sans-serif">你是谁</text>
  <line x1="100" y1="270" x2="220" y2="270" stroke="#60a5fa" stroke-width="1" opacity="0.5"/>
  <text x="160" y="290" text-anchor="middle" fill="#e0f2fe" font-size="10" font-family="system-ui, sans-serif">• 基本信息与偏好</text>
  <text x="160" y="308" text-anchor="middle" fill="#e0f2fe" font-size="10" font-family="system-ui, sans-serif">• 日程与工作</text>
  <text x="160" y="326" text-anchor="middle" fill="#e0f2fe" font-size="10" font-family="system-ui, sans-serif">• 兴趣与风格</text>

  <!-- MEMORY.md -->
  <rect x="270" y="200" width="160" height="130" rx="10" fill="url(#fileGrad2)" filter="url(#shadow)"/>
  <text x="350" y="230" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">MEMORY.md</text>
  <text x="350" y="255" text-anchor="middle" fill="#a7f3d0" font-size="11" font-family="system-ui, sans-serif">AI 学到了什么</text>
  <line x1="290" y1="270" x2="410" y2="270" stroke="#34d399" stroke-width="1" opacity="0.5"/>
  <text x="350" y="290" text-anchor="middle" fill="#d1fae5" font-size="10" font-family="system-ui, sans-serif">• 决策与教训</text>
  <text x="350" y="308" text-anchor="middle" fill="#d1fae5" font-size="10" font-family="system-ui, sans-serif">• 偏好与习惯</text>
  <text x="350" y="326" text-anchor="middle" fill="#d1fae5" font-size="10" font-family="system-ui, sans-serif">• 持续更新</text>

  <!-- brain/family/ -->
  <rect x="460" y="200" width="160" height="130" rx="10" fill="url(#fileGrad3)" filter="url(#shadow)"/>
  <text x="540" y="230" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">family/</text>
  <text x="540" y="255" text-anchor="middle" fill="#fde68a" font-size="11" font-family="system-ui, sans-serif">家人档案</text>
  <line x1="480" y1="270" x2="600" y2="270" stroke="#fbbf24" stroke-width="1" opacity="0.5"/>
  <text x="540" y="290" text-anchor="middle" fill="#fef3c7" font-size="10" font-family="system-ui, sans-serif">• 每人一个文件</text>
  <text x="540" y="308" text-anchor="middle" fill="#fef3c7" font-size="10" font-family="system-ui, sans-serif">• 生日与偏好</text>
  <text x="540" y="326" text-anchor="middle" fill="#fef3c7" font-size="10" font-family="system-ui, sans-serif">• 礼物点子</text>
</svg>

## 入职面试：让 AI 了解你

这些文件不会自己写出来。Josh 设计了一个"Onboarding Interview"（入职面试）的提示词。

核心思路：**不是问卷，是对话**。AI 一次问 2-3 个问题，根据你的回答追问有意思的点，你回答简短就不追问。整个过程 10-15 分钟，最后 AI 一次性生成所有文件。

覆盖的领域：
- 身份与基本信息：姓名、称呼、时区、电话
- 日常生活：作息、晨间习惯、最近在看什么
- 工作与项目：做什么、做了多久、工作风格
- 家庭与家人：谁住一起、名字、生日、爱好
- 兴趣爱好：音乐、运动、收藏、旅行偏好
- 沟通偏好：简洁还是详细、语气正式还是随性
- 目标与愿望：当前在追求什么、长期梦想
- 禁忌与边界：讨厌什么、什么话题不该碰

对话结束后，AI 生成 USER.md、MEMORY.md、family/README.md 以及每个家庭成员的独立文件。

## 每日一滴：六周后的质变

入职面试能覆盖 60% 左右。深度来自之后的事。

Josh 设置了一个 cron job：每天早上 9 点，AI 读取现有文件，找一个信息空白，问一个有深度的问题。不是"你最喜欢什么颜色"这种，而是"你提到你女儿在做彩绘玻璃，她是怎么入坑的？"

工作流程：
1. AI 发送一个问题到你的聊天频道
2. 你有空时回答（通常 30 秒）
3. 第二天早上，AI 处理昨天的答案，更新到对应文件，然后问新问题

六周后，这套"每日一滴"积累的上下文比最初的面试还多。它会捕捉到你从没想到要主动说的东西：早晨习惯、咖啡怎么喝、配偶要回学校了、年轻时玩过乐队、在丹佛住过五年所以是雪崩队球迷……

下面这张图展示了六周积累的效果对比：

<svg width="100%" viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="beforeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ef4444;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#dc2626;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="afterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#10b981;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#059669;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="700" height="350" fill="#0f172a"/>

  <!-- 标题 -->
  <text x="350" y="35" text-anchor="middle" fill="#fff" font-size="20" font-weight="bold" font-family="system-ui, sans-serif">六周后的对比</text>

  <!-- 左侧：通用 AI -->
  <rect x="40" y="70" width="280" height="250" rx="12" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
  <rect x="40" y="70" width="280" height="45" rx="12" fill="url(#beforeGrad)"/>
  <rect x="40" y="103" width="280" height="12" fill="url(#beforeGrad)"/>
  <text x="180" y="100" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">通用 AI</text>

  <text x="60" y="145" fill="#94a3b8" font-size="12" font-family="system-ui, sans-serif">"我需要给你老婆送礼物，有什么建议？"</text>
  <rect x="60" y="160" width="240" height="50" rx="8" fill="#374151"/>
  <text x="75" y="182" fill="#9ca3af" font-size="11" font-family="system-ui, sans-serif">"我很乐意帮你想礼物！这里有</text>
  <text x="75" y="198" fill="#9ca3af" font-size="11" font-family="system-ui, sans-serif">一些热门选择……"</text>

  <text x="60" y="235" fill="#94a3b8" font-size="12" font-family="system-ui, sans-serif">"今天想做什么？"</text>
  <rect x="60" y="250" width="240" height="50" rx="8" fill="#374151"/>
  <text x="75" y="272" fill="#9ca3af" font-size="11" font-family="system-ui, sans-serif">"你想做什么？我可以帮你……"</text>
  <text x="75" y="288" fill="#9ca3af" font-size="11" font-family="system-ui, sans-serif">（什么都不知道，重新开始）</text>

  <!-- 右侧：个性化 AI -->
  <rect x="380" y="70" width="280" height="250" rx="12" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <rect x="380" y="70" width="280" height="45" rx="12" fill="url(#afterGrad)"/>
  <rect x="380" y="103" width="280" height="12" fill="url(#afterGrad)"/>
  <text x="520" y="100" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">个性化 AI（6周后）</text>

  <text x="400" y="145" fill="#94a3b8" font-size="12" font-family="system-ui, sans-serif">"我需要给老婆送礼物"</text>
  <rect x="400" y="160" width="240" height="50" rx="8" fill="#064e3b"/>
  <text x="415" y="182" fill="#6ee7b7" font-size="11" font-family="system-ui, sans-serif">"她生日是3月15日，喜欢缝纫和编</text>
  <text x="415" y="198" fill="#6ee7b7" font-size="11" font-family="system-ui, sans-serif">织，最近要回学校……"</text>

  <text x="400" y="235" fill="#94a3b8" font-size="12" font-family="system-ui, sans-serif">（自动）</text>
  <rect x="400" y="250" width="240" height="50" rx="8" fill="#064e3b"/>
  <text x="415" y="272" fill="#6ee7b7" font-size="11" font-family="system-ui, sans-serif">"你4:45就起来了，趁家人还在睡，</text>
  <text x="415" y="288" fill="#6ee7b7" font-size="11" font-family="system-ui, sans-serif">要不要先处理那个刚毙掉的项目？"</text>

  <!-- 中间箭头 -->
  <text x="350" y="200" text-anchor="middle" fill="#6366f1" font-size="24" font-family="system-ui, sans-serif">VS</text>
</svg>

## 你可以直接用的模板

Josh 公开了他的"入职面试"提示词。复制、修改、用你喜欢的 AI 工具跑：

```markdown
You're getting to know your human for the first time. Your goal is to build
a rich personal profile that will make every future interaction feel personal
and useful.

Run this as a CONVERSATION — not a survey. Ask 2-3 questions at a time,
wait for answers, then ask follow-ups based on what they share. Be genuinely
curious, not clinical. If they give short answers, don't push — you'll learn
more over time.

What to cover (let it flow naturally, don't force the order):

Identity & Basics
- Name, what they prefer to be called, pronouns
- Location, timezone
- Phone number (if they want you to have it)

Daily Life
- Typical day — wake time, work hours, evening routine
- Morning ritual
- Currently watching/reading/playing?
- Food relationship — foodie or fuel?

Work & Projects
- What they do, how long they've been doing it
- Current active projects or businesses
- Work style — planner or builder? Deep focus or context-switching?
- Strengths and energy drains

Family & Household
- Who lives in the house? Partner, kids, pets?
- Names, birthdays, relationships
- Notable details — hobbies, schools, schedules
- Extended family worth knowing about

Interests & Hobbies
- What they do for fun
- Music, sports, collections, creative outlets
- Travel preferences
- Hidden passions or guilty pleasures

Communication Preferences
- Brief or detailed info delivery?
- Tone — formal, casual, snarky, warm?
- When to proactively reach out vs. stay quiet
- What annoys them in an AI assistant
- Quiet hours — when to never message

Goals & Aspirations
- What they're working toward now
- Long-term dreams or "someday" projects
- What success looks like to them

Pet Peeves & Boundaries
- Things they hate (AI responses, general)
- Off-limits or sensitive topics
- Privacy boundaries for group chats

After the conversation, create these files:

USER.md
Compile everything into a clean, scannable format with sections and bullet
points. Include subsections for Daily Life, Interests, Family, Work, etc.
This is the primary reference file the agent reads every session.

brain/family/README.md
Household overview table with names, relationships, birthdays, ages. Include
an "Upcoming Dates" section for the current year listing birthdays and
anniversaries chronologically.

brain/family/{firstname}.md (one per family member)
Use this template for each person mentioned:

  # {Name}
  **Relationship:** {relationship to user}
  **Birthday:** {date}
  ---
  ## Preferences
  (none yet)
  ## Important Dates
  - **Birthday:** {date}
  ## Gift Ideas
  (none yet)
  ## Notes
  (none yet)

Include pets too (simpler format — name, breed/species, any quirks).

MEMORY.md
Start a long-term memory file. Add a "Self-Knowledge" section capturing work
style, core drives, decision-making patterns — the deeper personality
insights that emerged from the conversation. This file grows over time.
```

## 笔者的几个判断

**第一，这不是技术问题，是产品问题。**

模型能力已经足够，真正缺的是让用户"喂"信息的方式。ChatGPT 的记忆是被动记录，Josh 的系统是主动面试。主动和被动，效果差了十倍。

**第二，纯文本是最被低估的技术选型。**

没有数据库、没有向量存储、没有专有格式。Markdown 文件，放哪都能用。换 AI 工具？复制粘贴就行。这就是**可移植性**的力量。越复杂的系统，迁移成本越高。越简单的格式，生命力越强。

**第三，"每日一滴"是个天才设计。**

大多数人没耐心一次性填完一份详细的个人档案。但每天 30 秒回答一个问题？谁都能做到。六周 42 个问题，信息量惊人。这暗合了一个朴素道理：**持续的小投入，比一次性的大投入更可持续**。

**第四，这个方案的局限在于"启动成本"。**

你需要有个能跑 cron job 的环境，需要一个能自动更新文件的 Agent。对普通用户来说，门槛不低。但如果你已经在用 OpenClaw、Claude Code 或类似工具，这就是现成的方案。

## 今天的行动建议

如果你已经在用个人 AI 助手（OpenClaw、Claude Code 等）：

1. 复制上面的提示词
2. 让 AI 面试你 10-15 分钟
3. 让它生成 USER.md、MEMORY.md、family/ 文件
4. 设置一个每日问问题的定时任务

如果你还没开始用个人 AI 助手：这是开始的好理由。OpenClaw 支持在 Mac、PC、Linux 甚至树莓派上运行，接 Discord 或 Telegram，一天之内就能让 AI 认识你。

六周后，你会有一个真正了解你的 AI。它知道你几点起床、收集什么、老婆喜欢什么、上周毙掉了哪个项目想法。

不需要更强的模型。只需要文件和持续。

---

### 参考

- [How I built a hyper-personalization system with AI - Josh Pigford](https://everydayisayear.ai/p/how-i-built-a-hyper-personalization)
- [OpenClaw](https://openclaw.ai) - 开源个人 AI 助手框架
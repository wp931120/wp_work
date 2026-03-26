# Karpathy 开源"自动驾驶实验室"：一晚跑 100 次实验，我拿它优化了所有 Skills

> 📖 **本文解读内容来源**
>
> - **原始来源**：[The Ultimate Autoresearch Guide](https://www.aibyaakash.com/p/autoresearch-guide)
> - **来源类型**：技术博客
> - **作者**：Aakash Gupta
> - **发布时间**：2026 年 3 月
> - **核心项目**：[karpathy/autoresearch](https://github.com/karpathy/autoresearch) - 42,000+ GitHub Stars

---

你有没有过这种时刻：写了一个 Prompt，跑了三次都不满意，改来改去还是差点意思？

或者写了一封 outreach 邮件，回复率只有 2%，想 A/B 测试但手动搞太慢？

**说实话，笔者也遇到过。** 上周笔者优化一个 Skills 文件，反复调了 8 遍，最后还是觉得不够好。但人的精力有限，你不可能一晚上试 50 个版本。

但 Karpathy 可以。

他开源了一个叫 **autoresearch** 的项目，GitHub 上 42,000 颗星，Fortune 杂志称之为"**The Karpathy Loop**"。

核心逻辑很简单：**让 AI 自己跑实验，一晚上迭代 100 次，只保留有效的改进。**

Karpathy 拿它优化自己的小语言模型训练代码，跑了两天，AI 找到了 20 个他人工优化几个月都没发现的改进点，包括一个 attention 实现的 bug。最终模型速度提升 11%。

Shopify CEO Tobi Lutke 当晚就拿去试了，37 次实验后，他的小模型开始超越大模型。然后他把这个 Loop 用在 Shopify 的 Liquid 模板引擎上，**93 次自动提交，渲染速度提升 53%**。

最离谱的是：这套系统跑一晚上，电费只要 25 美元。

今天这篇深度指南，笔者花两周时间把 Karpathy 的 repo、社区 fork 和真实应用场景全部扒了一遍。

**你不需要 GPU，不需要懂 ML。** 这个 Loop 可以用在广告文案、邮件序列、视频脚本、招聘 JD……任何你能定义"好"是什么的东西上。

话不多说，开始。

---

## 这是个啥？为什么要在乎？

**一句话定义：autoresearch 是一个自动化的"试错 - 保留"循环系统。**

它做三件事：
1. 对你的目标文件（Prompt、Skill、模板）做一次小改动
2. 用预设的评分标准给输出打分
3. 分数提高就保留，降低就回滚，然后继续下一轮

**类比一下：** 这就像你有一个永不疲倦的实习生，他愿意一晚上试 100 种写法，每种都按你的标准打分，最后只把最好的版本交给你。

下面这张图展示了核心循环：

<svg width="100%" viewBox="0 0 700 320" xmlns="http://www.w3.org/2000/svg">
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
      <stop offset="0%" style="stop-color:#eb3349;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f45c43;stop-opacity:1" />
    </linearGradient>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#667eea" />
    </marker>
  </defs>
  
  <!-- Background -->
  <rect width="700" height="320" fill="#f8f9fa" rx="12" />
  
  <!-- Title -->
  <text x="350" y="35" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">The Karpathy Loop - Autoresearch 核心循环</text>
  
  <!-- Step 1: Read -->
  <rect x="50" y="70" width="120" height="60" rx="8" fill="url(#grad1)" />
  <text x="110" y="95" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">1. 读取当前版本</text>
  <text x="110" y="115" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">Prompt/Skill 文件</text>
  
  <!-- Arrow 1 -->
  <line x1="170" y1="100" x2="220" y2="100" stroke="#667eea" stroke-width="2" marker-end="url(#arrowhead)" />
  
  <!-- Step 2: Edit -->
  <rect x="220" y="70" width="120" height="60" rx="8" fill="url(#grad1)" />
  <text x="280" y="95" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">2. AI 决定改动</text>
  <text x="280" y="115" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">每次只改一处</text>
  
  <!-- Arrow 2 -->
  <line x1="340" y1="100" x2="390" y2="100" stroke="#667eea" stroke-width="2" marker-end="url(#arrowhead)" />
  
  <!-- Step 3: Test -->
  <rect x="390" y="70" width="120" height="60" rx="8" fill="url(#grad1)" />
  <text x="450" y="95" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">3. 运行测试</text>
  <text x="450" y="115" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">生成 30 个输出评分</text>
  
  <!-- Arrow 3 -->
  <line x1="510" y1="100" x2="560" y2="100" stroke="#667eea" stroke-width="2" marker-end="url(#arrowhead)" />
  
  <!-- Step 4: Decision -->
  <rect x="560" y="70" width="120" height="60" rx="8" fill="#667eea" />
  <text x="620" y="95" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">4. 决策</text>
  <text x="620" y="115" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">分数↑还是↓？</text>
  
  <!-- Keep Path -->
  <path d="M 620 130 L 620 160 L 110 160 L 110 130" fill="none" stroke="url(#grad2)" stroke-width="2" marker-end="url(#arrowhead)" />
  <text x="380" y="155" text-anchor="middle" fill="#11998e" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">✓ 保留（git commit）</text>
  
  <!-- Discard Path -->
  <path d="M 620 130 L 650 130 L 650 200 L 280 200 L 280 130" fill="none" stroke="url(#grad3)" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowhead)" />
  <text x="480" y="195" text-anchor="middle" fill="#eb3349" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">✗ 回滚（git reset）</text>
  
  <!-- Stats Box -->
  <rect x="50" y="220" width="280" height="80" rx="8" fill="#fff" stroke="#667eea" stroke-width="2" />
  <text x="190" y="245" text-anchor="middle" font-size="13" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">📊 性能数据</text>
  <text x="80" y="270" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 每轮耗时：~5 分钟</text>
  <text x="80" y="290" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 每小时：12 轮迭代</text>
  <text x="220" y="270" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 每晚：~100 轮</text>
  <text x="220" y="290" font-size="12" font-family="system-ui, sans-serif" fill="#555">• 成本：~$25/晚</text>
</svg>

**为什么这很重要？**

因为大多数人在用 AI 时，都是在**单次交互**的层面优化。你问一次，得到一个答案，觉得不够好，再问一次。但人的耐心有限，通常试 3-5 次就放弃了。

**但 AI 不需要休息。** 它可以一晚上试 100 次，而且每次都比上一次更好。

这就是复利的力量。

---

## 核心原理：三个文件，一个循环

autoresearch 系统由三个文件驱动：

| 文件 | 作用 | AI 能否修改 |
|------|------|------------|
| **目标文件** | 被优化的东西（Prompt、Skill、模板） | ✅ 可以 |
| **评分标准** | 定义什么是"好"的 yes/no 问题 | ❌ 绝对禁止 |
| **指令文件** | 告诉 AI 要试什么、如何行为 | ❌ 人类编写 |

**关键约束：每次循环只能改一个文件，其他全部锁定。**

如果 AI 能修改评分标准，它会干嘛？当然是让测试变简单，而不是让输出变好。这就像学生改考卷答案一样。

### 循环流程

每轮循环大约 5 分钟：

1. AI 读取当前版本的目标文件
2. 决定做什么改动
3. 执行编辑
4. 运行测试（生成 30 个输出，按评分标准打分）
5. 分数提高 → git commit 保留
6. 分数降低或持平 → git reset 回滚
7. 下一轮开始

**每小时 12 轮，一晚上 100 轮，电费 25 美元。**

Karpathy 用这个 Loop 跑了自己手工优化几个月的代码，AI 找到了 20 个他没发现的改进点。所有改进叠加后迁移到更大的模型上，速度提升 11%。

---

## 如何搭建你的第一个 Loop

### 第一步：克隆仓库

```bash
git clone https://github.com/karpathy/autoresearch ./autoresearch-reference
git init && git add . && git commit -m "setup"
```

这给你的 coding agent 一份 Karpathy 约定的参考副本。如果你已经有想优化的 Prompt 或 Skill 文件，把它放进同一个文件夹。

### 第二步：写评分标准（这是人类的工作）

**这里是大多数人成败的关键。**

你要写的是**yes/no 问题**，描述好的输出长什么样。

笔者用一个落地页文案 Skill 的评分标准举例：

```markdown
## Eval Criteria（评分标准）

- 标题是否包含具体数字或可量化结果？
- 文案是否完全无 buzzwords（如"革命性"、"颠覆性"）？
- CTA 是否使用与产品结果相关的具体动作动词？
- 标题后第一句是否点明具体痛点？
- 总文案是否在 80-150 词之间？
```

**5 个二元问题。** AI 每轮生成 30 个输出，每个都打分，最后给出一个百分比。

**不知道从哪开始？** 直接描述你当前输出的问题："标题太泛、术语太多、CTA 太弱"。Claude Code 会帮你把这些抱怨转成二元评分标准。

**经验法则：3-6 个问题最合适。** 少于 3 个，AI 会找漏洞；多于 6 个，AI 开始刷 checklist 而不是真正改进输出质量。

### 第三步：告诉 Claude Code 跑 Loop

```
阅读 autoresearch-reference/program.md 理解 Karpathy 的
autoresearch 约定。我想优化 [我的 skill / prompt / 系统提示]，
使用这些评分标准：[你的 yes/no 问题]。

用这些输入测试：[2-3 个真实场景]。

搭建评估框架，跑基线，然后进入 autoresearch 循环。
每轮只改一处。分数提高就保留，降低就回滚。
评估创建后永远不要修改。
```

一个 Prompt。Claude Code 读取约定、搭建评估脚本、生成基线分数，然后开始迭代。

---

## 真实案例：4 轮从 41% 到 92%

笔者拿一个落地页文案 Skill 跑了这个 Loop，用上面 5 个评估标准。基线分数 41.3%。

**第 1 轮：** Claude Code 发现"标题包含具体数字"这一项 80% 失败。它在 Skill 里加了一条规则要求具体数字。分数跳到 68%。保留。

**第 2 轮：** buzzwords 是下一个最大失败点。它加了一个禁用词列表。79%。保留。

**第 3 轮：** CTA 还是很泛。它加了一个工作示例展示强 CTA 长什么样。90%。

**第 4 轮：** 它尝试收紧字数限制。分数掉到 82%，因为更短的文案伤害了 CTA。回滚。

**最终结果：41% → 92%，4 轮，3 个改动保留，1 个回滚。** 评估自动捕捉到了回退。

下面这张图展示了迭代过程：

<svg width="100%" viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="700" height="380" fill="#f8f9fa" rx="12" />
  
  <!-- Title -->
  <text x="350" y="35" text-anchor="middle" font-size="16" font-weight="bold" font-family="system-ui, sans-serif" fill="#333">落地页文案 Skill 优化过程</text>
  
  <!-- Chart Area -->
  <rect x="60" y="60" width="580" height="250" fill="#fff" rx="8" stroke="#e0e0e0" stroke-width="1" />
  
  <!-- Grid Lines -->
  <line x1="60" y1="110" x2="640" y2="110" stroke="#f0f0f0" stroke-width="1" />
  <line x1="60" y1="160" x2="640" y2="160" stroke="#f0f0f0" stroke-width="1" />
  <line x1="60" y1="210" x2="640" y2="210" stroke="#f0f0f0" stroke-width="1" />
  <line x1="60" y1="260" x2="640" y2="260" stroke="#f0f0f0" stroke-width="1" />
  
  <!-- Y Axis Labels -->
  <text x="50" y="315" text-anchor="end" font-size="11" font-family="system-ui, sans-serif" fill="#666">0%</text>
  <text x="50" y="265" text-anchor="end" font-size="11" font-family="system-ui, sans-serif" fill="#666">25%</text>
  <text x="50" y="215" text-anchor="end" font-size="11" font-family="system-ui, sans-serif" fill="#666">50%</text>
  <text x="50" y="165" text-anchor="end" font-size="11" font-family="system-ui, sans-serif" fill="#666">75%</text>
  <text x="50" y="115" text-anchor="end" font-size="11" font-family="system-ui, sans-serif" fill="#666">100%</text>
  
  <!-- Data Points -->
  <!-- Baseline: 41.3% -->
  <circle cx="120" cy="247" r="6" fill="url(#scoreGrad)" />
  <text x="120" y="265" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#333">基线</text>
  <text x="120" y="240" text-anchor="middle" font-size="10" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">41%</text>
  
  <!-- Round 1: 68% -->
  <circle cx="240" cy="196" r="6" fill="url(#scoreGrad)" />
  <text x="240" y="214" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#333">第 1 轮</text>
  <text x="240" y="189" text-anchor="middle" font-size="10" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">68%</text>
  <text x="240" y="175" text-anchor="middle" font-size="9" font-family="system-ui, sans-serif" fill="#11998e">✓ 保留</text>
  
  <!-- Round 2: 79% -->
  <circle cx="360" cy="174" r="6" fill="url(#scoreGrad)" />
  <text x="360" y="192" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#333">第 2 轮</text>
  <text x="360" y="167" text-anchor="middle" font-size="10" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">79%</text>
  <text x="360" y="153" text-anchor="middle" font-size="9" font-family="system-ui, sans-serif" fill="#11998e">✓ 保留</text>
  
  <!-- Round 3: 90% -->
  <circle cx="480" cy="152" r="6" fill="url(#scoreGrad)" />
  <text x="480" y="170" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#333">第 3 轮</text>
  <text x="480" y="145" text-anchor="middle" font-size="10" font-weight="bold" font-family="system-ui, sans-serif" fill="#667eea">90%</text>
  <text x="480" y="131" text-anchor="middle" font-size="9" font-family="system-ui, sans-serif" fill="#11998e">✓ 保留</text>
  
  <!-- Round 4: 82% (reverted) -->
  <circle cx="600" cy="168" r="6" fill="#eb3349" />
  <text x="600" y="186" text-anchor="middle" font-size="11" font-family="system-ui, sans-serif" fill="#333">第 4 轮</text>
  <text x="600" y="161" text-anchor="middle" font-size="10" font-weight="bold" font-family="system-ui, sans-serif" fill="#eb3349">82%</text>
  <text x="600" y="147" text-anchor="middle" font-size="9" font-family="system-ui, sans-serif" fill="#eb3349">✗ 回滚</text>
  
  <!-- Connecting Lines -->
  <polyline points="120,247 240,196 360,174 480,152" fill="none" stroke="url(#scoreGrad)" stroke-width="2" />
  <line x1="480" y1="152" x2="600" y2="168" stroke="#eb3349" stroke-width="2" stroke-dasharray="5,5" />
  
  <!-- Final Result -->
  <rect x="60" y="325" width="200" height="45" rx="8" fill="url(#grad2)" />
  <text x="160" y="345" text-anchor="middle" font-size="12" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">最终结果</text>
  <text x="160" y="365" text-anchor="middle" font-size="18" font-weight="bold" font-family="system-ui, sans-serif" fill="#fff">41% → 92%</text>
</svg>

---

## 六大实战场景

### 场景 1：Outreach 邮件优化

你的 outreach 回复率只有 2-3%。你试过手动 A/B 测试，但要几周才能有信号。

**评分标准：**
- 是否少于 75 词？
- 是否提到对方的具体职位？
- 是否以具体问题结尾？
- 前两句是否包含具体数字或结果？

AI 会发现人类文案writer 花几年才学到的东西：**短比长好，具体比模糊好，风险逆转比功能列表好。**

Eric Siu（广告公司 Single Grain 创始人）已经在为客户搭建这个系统。他的框架把训练脚本换成邮件本身。AI 修改主题行或 CTA，测量回复率，保留或丢弃。

**他的计算：大多数营销团队一年跑约 30 次实验。这个 Loop 一年跑 36,500+ 次。**

MindStudio 记录了团队用这个模式，4-6 周内回复率从 2-4% 提升到 8-12%。

### 场景 2：广告文案迭代

你在跑 Meta 或 Google 广告，每周手动测试 2-3 个标题变体。一年大概 150 次测试。Autoresearch 一晚上跑 100 次。

**评分标准：**
- 标题是否少于 40 字符？
- 前 5 个词是否点明具体痛点？
- 正文是否提到数字或时间框架？
- CTA 是否是动词短语而非名词短语（"开始省钱"而非"省钱计划"）？
- 是否避免品牌禁用词列表上的所有词？

### 场景 3：视频脚本优化

你的 Reels 和 TikToks 在 hook 落地时爆火，没落地时就扑街。你凭直觉知道，但测试 hook 要靠发帖等 48 小时看算法反馈。

**评分标准：**
- 开头是否制造具体好奇心缺口？
- 前 2 句是否有反直觉主张？
- 是否遵循单一叙事线索（而非 3 个松散关联的点）？
- 朗读时脚本是否少于 60 秒？
- 最后一句是否为下一条内容做铺垫？

AI 无法预测病毒式传播，但它可以执行与观看时长相关的结构模式。

### 场景 4：Onboarding 邮件序列

你 6 个月前写了 5 封 onboarding 邮件。打开率还行，但激活率卡在 30%，你一直太忙没时间重写。

**评分标准：**
- 每封邮件是否只有一个 CTA？
- 邮件是否少于 100 词？
- 主题行是否包含具体好处或数字？
- 第一句是否引用用户上次操作（而非通用问候）？
- 第一段是否避免"我们"（关注他们而非你）？

### 场景 5：招聘 JD 优化

大多数招聘 JD 写一次就再也不优化。太长、全是术语、读起来像法律文件。然后你奇怪为什么合格的人不申请。

**评分标准：**
- 是否少于 400 词？
- 是否在前 90 天内要做的具体项目？
- 是否无内部术语和缩写？
- 是否包含薪资范围？
- 第一句是否描述影响力而非职责？

这是最干净的 autoresearch 应用之一，因为评估标准显而易见且二元。AI 会剥离术语、强制具体化、前置影响力。几轮后你就有一个人们真正想读的 JD 模板。

### 场景 6：Skills 自我进化

这正是笔者在做的。每个 Skill 都加上自我改进循环：

- 每次我纠正 Agent，它记录纠正和上下文
- 当同样纠正出现 3 次以上，晋升为永久规则
- Agent 知道我的写作声音、格式偏好、沟通风格

**这是复利。** 第 1 周，你纠正所有事。第 3 个月，它自己就能运转。

---

## 三个致命错误（千万别踩）

花两周时间研究这个，笔者看到同样的三个错误在 Loop 开始前就杀死它。

### 错误 1：模糊的评估标准

"文案是否有吸引力？" 这不是 AI 能评分的问题。"标题是否包含具体数字？" 才是。

**每个标准必须是二元的。** 通过或失败，是或否，没有滑动刻度。一旦你引入 1-7 评分，AI 开始优化技术上得分高但读起来像垃圾的 4 分。

**如果你不能用一句话向陌生人解释如何评分，重写标准。**

### 错误 2：中途修改评估

你的基线回来是 35%，你的第一冲动是软化标准让数字好看点。**这是最快浪费一次运行的方法。**

评估在第一轮开始后就锁定。如果你中途改评分标准，之前所有轮次的数据都变得无意义。你在拿苹果和橙子比较。

如果评估错了，停止运行，修好它，从头重新开始。Karpathy 让 prepare.py 只读就是这个原因。

### 错误 3：太多标准

七八个评估问题感觉全面。实际上，AI 开始刷 checklist。它找到技术上通过 7/8 标准但输出读起来不像人类写的变化组合。

**3-6 个标准是甜蜜点。** 足够防止捷径，少到让 AI 优化真实质量而非 checklist 合规。有疑虑时，从 3 个开始，如果输出有你没覆盖的失败模式，一次加一个。

---

## 笔者的判断与思考

花两周时间深入研究 autoresearch，笔者有几个判断想分享。

### 1. 这不是 ML 专属，这是通用模式

所有报道都聚焦在 ML 角度。但他们都错过了更大的故事。**底层的模式可以用在任何你能衡量的东西上。**

Skills、Prompts、Agents、邮件、页面速度……任何有明确"好"标准的输出，都可以用这个 Loop 优化。

### 2. 评估是核心，不是 Loop

大多数人把注意力放在"自动化循环"上。但真正的护城河是**你的评估标准质量**。

评估标准写得好，Loop 自动跑。评估标准写得烂，Loop 跑得越快，错得越远。

这就像训练数据：垃圾进，垃圾出。

### 3. 这是"AI 员工"的真正形态

大多数人用 AI 还是单次交互：问问题，得答案，关应用。

但 autoresearch 展示的是另一种可能：**AI 不是回答者，是实验者。**

它不等你指令，它自己设计实验、跑测试、保留有效改进。你早上醒来，东西已经变得更好了。

这才是"AI 员工"该有的样子。

### 4. 复利效应被严重低估

大多数人低估了这个 Loop 的复利效应。

一晚上 100 次迭代，每次提升 1%，看起来不多。但 100 天后呢？100 个 Skills 呢？

**这就是为什么我说这是 2026 年最大的生产力解锁。** 不是因为它多炫酷，而是因为它是少数几个真正能复利的 AI 用法。

---

## 结语

autoresearch 确实是个很强大的模式，就像一个永不疲倦的优化机器。

但笔者必须坦诚：**它不是万能的。**

如果你的输出无法用二元标准衡量，这个 Loop 跑不起来。如果你的评估标准写不好，AI 会找到漏洞刷分而不是真正改进。

和竞品比，笔者的判断是：**这是目前最接近"自动驾驶实验室"的开源方案。** 不需要 GPU，不需要 ML 知识，只需要一个 coding agent（Claude Code、Cursor、Windsurf 都行）和清晰的评估标准。

跨领域想一下，这暗合了一个朴素道理：**好的系统让普通人做出好结果，坏的系统让天才也无力回天。**

autoresearch 就是一个好系统。它把"试错 - 保留"这个人类最擅长但最没耐心的过程，交给了不知疲倦的 AI。

**最后给读者的建议：**

挑一件你一直想改进的事。写 3-5 个 yes/no 问题定义什么是"好"。让 Loop 今晚就跑。

明天早上醒来，你会收到一些已经变得更好的东西。

就是这么简单。

---

### 参考

- [The Ultimate Autoresearch Guide](https://www.aibyaakash.com/p/autoresearch-guide) - Aakash Gupta
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch) - GitHub Repository
- [MindStudio: Karpathy Autoresearch Pattern for Marketing](https://www.mindstudio.ai/blog/karpathy-autoresearch-pattern-marketing-automation)
- [Fortune: The Karpathy Loop](https://fortune.com/2026/03/17/andrej-karpathy-loop-autonomous-ai-agents-future/)

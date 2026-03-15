# YC 总裁开源 AI 工作流：4 天 1.2 万星，把 Claude Code 变成一支工程团队

> 不是 prompt 合集，是一套能直接上手的"认知操作系统"

![gstack 8 种认知模式](file:///Users/wp931120/lobsterai/project/wp_work/20260315_gstack/image1.png)

**核心看点：**
- 4 天 1.2 万星，GitHub 趋势榜第一，Fork 数破 1400
- YC 总裁 Garry Tan 把他管理 YC 投后公司的工程方法论开源了
- 8 个斜杠命令，把 Claude Code 从"通用助手"变成"专家团队"
- 浏览器自动化，60 秒完成 QA 测试，不用手动点击

---

## 一、为什么需要 gstack？

AI 编程工具最大的瓶颈不是代码能力，而是"认知模式"单一。

你让同一个模型同时做产品规划、技术评审、代码审查、发布上线、QA 测试，就像让一个人既当 CEO 又当工程师又当测试，结果往往是"四不像"。

Garry Tan 在 README 里写得很直白：

> "Planning is not review. Review is not shipping. Founder taste is not engineering rigor. If you blur all of that together, you usually get a mediocre blend of all four."

规划不是评审，评审不是发布，创始人品味不是工程严谨性。把这些混在一起，通常只会得到一个平庸的混合体。

gstack 的解法很简单：显式切换认知模式。

用 8 个斜杠命令，告诉模型"我现在需要你用什么脑子"：

| 命令 | 角色 | 用途 |
|------|------|------|
| `/plan-ceo-review` | 创始人/CEO | 重新定义问题，找到藏在需求里的 10 分产品 |
| `/plan-eng-review` | 技术负责人 | 锁定架构、数据流、边界条件、测试矩阵 |
| `/review` | 偏执的资深工程师 | 找出那些能过 CI 但会在生产环境出问题的 bug |
| `/ship` | 发布工程师 | 同步主干、跑测试、推分支、开 PR |
| `/browse` | QA 工程师 | 登录、点击、截图、抓错，60 秒完成 QA 流程 |
| `/qa` | QA 负责人 | 系统级测试，自动识别受影响的页面并验证 |
| `/setup-browser-cookies` | 会话管理 | 从真实浏览器导入 cookies，测试认证页面 |
| `/retro` | 工程经理 | 团队周报：每人贡献、亮点、改进建议 |

---

## 二、一个功能的五种模式

Garry 在 README 里给了一个完整 demo，建议每个用 AI 编程的人都看看这个工作流。

假设你要给一个二手交易平台加"卖家上传图片"功能：

### 第一步：`/plan-ceo-review`（创始人模式）

你说："让卖家上传图片"

普通助手会：加个文件选择器，保存图片，结束。

gstack 会先问一个更重要的问题：这个功能到底是干嘛的？

> "上传图片"不是真正的功能。真正的工作是帮助卖家创建能卖出去的 listing。
>
> 10 分版本应该是：
> - 从照片自动识别产品
> - 从网上拉取规格和竞品价格
> - 自动生成标题和描述
> - 建议哪张图最适合做封面
> - 检测图片是否模糊、昏暗、低信任度
> - 让体验感觉像高端产品，而不是 2007 年的死表单

这就是 Brian Chesky 模式：不是实现显而易见的 ticket，而是从用户角度重新思考问题，找到那个令人愉悦的版本。

### 第二步：`/plan-eng-review`（技术负责人模式）

产品方向定了，现在需要技术骨架。

gstack 会输出：
- 架构图（上传→分类→增强→草稿生成的流水线）
- 同步/异步边界（哪些步骤实时，哪些走后台任务）
- 失败模式（上传成功但增强失败怎么办？）
- 重试逻辑、去重机制、持久化策略
- 状态机、数据流图、测试矩阵

Garry 特别强调："当你强迫模型画图时，它会变得更完整。图表会让隐藏的假设暴露出来。"

### 第三步：实现代码

退出规划模式，正常写代码。

### 第四步：`/review`（偏执工程师模式）

测试都过了？`/review` 还是会问：

- 有没有引入 N+1 查询？
- 两个标签页会不会 race condition 覆盖封面图选择？
- 失败的上传会不会留下永久孤儿文件？
- 从网上拉数据到草稿生成，有没有 prompt 注入风险？

这不是风格挑刺，而是生产事故预演。

### 第五步：`/ship`（发布机器模式）

不想再讨论了，只想落地。

`/ship` 会：同步 main 分支、跑测试、解决 Greptile 评论、推分支、开 PR。6 个工具调用，结束。

### 第六步：`/qa`（QA 负责人模式）

```
你：/qa

Claude: 分析分支 diff...
        12 个文件变更：3 个控制器、2 个视图、4 个服务、3 个测试

        受影响的路线：/listings/new, /listings/:id, /api/listings
        检测到应用运行在 localhost:3000。

        [测试每个受影响的页面]

        QA 报告：3 条路线已测试，全部正常。
        - /listings/new: 上传 + 增强流程端到端通过
        - /listings/:id: 详情页渲染正常
        - /api/listings: 返回 200，形状符合预期
        无控制台错误。相邻页面无回归。
```

---

## 三、核心技术：浏览器自动化

gstack 最让我惊艳的是浏览器自动化的技术实现。

### 传统 MCP 方案的问题

用 MCP（Model Context Protocol）做浏览器自动化，有三个问题：

1. 上下文膨胀：每次调用都带上完整的 JSON schema 和协议框架，一个简单的"获取页面文本"要多花 10 倍 token
2. 连接脆弱：持久 WebSocket/stdio 连接会掉线，重连麻烦
3. 不必要的抽象：Claude Code 已经有 Bash 工具，CLI 输出到 stdout 是最简单的接口

### gstack 的方案

编译型 CLI + 持久化 Chromium 守护进程

![gstack 浏览器自动化架构](file:///Users/wp931120/lobsterai/project/wp_work/20260315_gstack/image2.png)

关键数据：

| 工具 | 首次调用 | 后续调用 | 每次调用上下文开销 |
|------|---------|---------|------------------|
| Chrome MCP | ~5s | ~2-5s | ~2000 tokens |
| Playwright MCP | ~3s | ~1-3s | ~1500 tokens |
| gstack browse | ~3s | ~100-200ms | 0 tokens |

在一个 20 次命令的浏览器会话中，MCP 工具要在协议框架上烧掉 3-4 万 tokens，gstack 是零。

### 核心创新：基于 ref 的元素选择

gstack 的浏览器不用传统的 XPath 或 CSS 选择器，而是基于可访问性树的 ref 系统：

1. `page.locator(scope).ariaSnapshot()` 返回 YAML 风格的可访问性树
2. 快照解析器给每个元素分配 ref（`@e1`, `@e2`, ...）
3. 为每个 ref 构建 Playwright `Locator`
4. 后续命令如 `click @e3` 直接查表调用

没有 DOM 注入，没有脚本，纯 Playwright 原生 API。

### 扩展功能

- `--diff`：存储基线快照，下次调用返回统一 diff，验证操作是否生效
- `--annotate`：在每个 ref 位置注入临时覆盖层，拍带标签的截图
- `--cursor-interactive`：扫描非 ARIA 的可点击元素（有 `cursor:pointer` 的 div 等）

### 多工作空间隔离

每个工作空间都有独立的浏览器实例：

| 工作空间 | 状态文件 | 端口 |
|---------|---------|------|
| `/code/project-a` | `/code/project-a/.gstack/browse.json` | 随机 (10000-60000) |
| `/code/project-b` | `/code/project-b/.gstack/browse.json` | 随机 (10000-60000) |

无端口冲突，无状态共享，完全隔离。

这意味着你可以用 [Conductor](https://conductor.build) 同时跑 10 个 Claude Code 会话：
- 一个在跑 `/qa` 测试 staging
- 一个在做 `/review` 审查 PR
- 三个在实现不同功能
- 五个在处理其他分支

一个人，十个并行 agent，每个都有正确的认知模式。

---

## 四、Greptile 集成：自动化代码审查

[Greptile](https://greptile.com) 是 YC 投资的公司，自动审查 PR，能抓出 race condition、安全问题那些能过 CI 但生产会出问题的 bug。

问题：自动审查工具总会有误报。有些是假阳性，有些是你已经修了的。没有分类层，评论堆积起来就会被忽略。

gstack 的解法：`/review` 和 `/ship` 是 Greptile 感知的。

- 有效问题：添加到关键发现，发布前修复
- 已修复问题：自动回复确认
- 假阳性：推回去，你确认后发出解释

还会学习：每个你确认的假阳性会保存到 `~/.gstack/greptile-history.md`，未来运行自动跳过已知模式。`/retro` 还会追踪 Greptile 的准确率。

### 示例

```
你：/ship

Claude: [同步 main，跑测试，预发布审查...]

        Greptile 在 PR 上发现 3 条评论：

        [有效] payment_service.rb:47 — Race condition:
        并发扣款可能重复收费。建议 DB 级咨询锁。

        [已修复] user.rb:12 — 缺少 email 空值检查
        → 已在 commit abc1234 修复。自动回复。

        [假阳性] auth.rb:88 — "Token 比较应该用常量时间"
        → 已经用 secure_compare 了。

        正在修复 payment_service.rb 的 race condition...
        应用咨询锁。提交：fix: address Greptile review

        共 3 条评论。1 个真实修复。1 个自动确认。1 个假阳性推回。
        额外时间：约 30 秒。
```

---

## 五、安装和使用

### 安装（全局）

在 Claude Code 里粘贴：

```
Install gstack: run `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` then add a "gstack" section to CLAUDE.md that says to use the /browse skill from gstack for all web browsing, never use mcp__claude-in-chrome__* tools, and lists the available skills: /plan-ceo-review, /plan-eng-review, /review, /ship, /browse, /qa, /setup-browser-cookies, /retro. Then ask the user if they also want to add gstack to the current project so teammates get it.
```

### 安装（项目级）

让团队成员也能用：

```
Add gstack to this project: run `cp -Rf ~/.claude/skills/gstack .claude/skills/gstack && rm -rf .claude/skills/gstack/.git && cd .claude/skills/gstack && ./setup` then add a "gstack" section to this project's CLAUDE.md...
```

注意：项目里会提交真实文件（不是子模块），`git clone` 就能用。二进制文件和 `node_modules/` 被 gitignore 忽略，团队成员只需运行 `cd .claude/skills/gstack && ./setup` 一次来构建。

### 依赖

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Git](https://git-scm.com/)
- [Bun](https://bun.sh/) v1.0+

`/browse` 会编译二进制文件——支持 macOS 和 Linux（x64 和 arm64）。

---

## 六、谁适合用 gstack？

Garry 说得很清楚：

> "This is not a prompt pack for beginners. It is an operating system for people who ship."

这不是给初学者的 prompt 合集，而是给能落地的人的操作系统。

如果你：
- 已经重度使用 Claude Code
- 想要一致、高严谨度的工作流，而不是模糊的通用模式
- 想告诉模型"现在用哪种脑子"：创始人品味、工程严谨、偏执审查、快速执行

那 gstack 就是为你设计的。

---

## 七、我的使用建议

### 1. 从 `/plan-ceo-review` 开始

几乎所有功能我都从 plan mode 开始。描述想建什么，然后用 `/plan-ceo-review` 压力测试是不是在做正确的事。

### 2. 产品方向锁定后再切工程

只有产品方向定了，才切换到工程、审查、发布、测试模式。

### 3. 用 Conductor 跑多个并行会话

gstack 在一个会话里很强大，在十个会话里更强大。

### 4. `/qa` 比手动测试快 10 倍

在功能分支上，直接 `/qa`，它会自动识别你改动的页面并测试。

---

## 八、写在最后

我为什么对 gstack 这么兴奋？

它解决的不是"AI 能不能写代码"，而是"AI 能不能用正确的方式思考"。

大多数 AI 工具在追求"更智能"，而 gstack 在追求"更合适的认知模式"。

规划时像创始人，工程时像技术负责人，审查时像偏执工程师，发布时像发布机器，测试时像 QA 专家。

这是一种不同的构建软件的方式。

Garry 在 README 最后写了一段招聘广告，我贴一下，因为这段话本身就很有 YC 风格：

```
+----------------------------------------------------------------------------+
|                                                                            |
|   Are you a great software engineer who loves to write 10K LOC/day         |
|   and land 10 PRs a day like Garry?                                        |
|                                                                            |
|   Come work at YC: ycombinator.com/software                                |
|                                                                            |
|   Extremely competitive salary and equity.                                 |
|   Now hiring in San Francisco, Dogpatch District.                          |
|   Come join the revolution.                                                |
|                                                                            |
+----------------------------------------------------------------------------+
```

**革命已经开始了。**

---

## 参考资料

- **项目地址：** https://github.com/garrytan/gstack
- **作者：** Garry Tan，YC 总裁兼 CEO
- **技术文档：** [ARCHITECTURE.md](https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md), [BROWSER.md](https://github.com/garrytan/gstack/blob/main/BROWSER.md)
- **Conductor（多会话并行）：** https://conductor.build
- **Greptile（代码审查）：** https://greptile.com

---

**公众号：** 龙虾 AI 工程师
**作者：** OpenClaw
**日期：** 2026 年 3 月 15 日

*如果这篇文章对你有帮助，欢迎转发给更多工程师。*

# YC 总裁开源 AI 工作流：4 天 1.2 万星，把 Claude Code 变成一支工程团队

一套能直接上手的"认知操作系统"，8 个斜杠命令让 Claude Code 从"通用助手"变成"专家团队"。

![gstack 8 种认知模式](file:///Users/wp931120/lobsterai/project/wp_work/20260315_gstack/gstack-modes.svg)

4 天 1.2 万星，GitHub 趋势榜第一。YC 总裁 Garry Tan 把他管理投后公司的工程方法论开源了。

---

> 📖 **本文解读内容来源**
> 项目地址：https://github.com/garrytan/gstack
> 作者：Garry Tan，YC 总裁兼 CEO

---

## 为什么需要 gstack？

你让同一个模型同时做产品规划、技术评审、代码审查、QA 测试，结果往往是"四不像"。

Garry Tan 说得直白："Planning is not review. Review is not shipping. Founder taste is not engineering rigor. 把这些混在一起，只会得到一个平庸的混合体。"

gstack 用 8 个命令显式切换认知模式：`/plan-ceo-review`（创始人视角）、`/plan-eng-review`（技术负责人）、`/review`（偏执工程师）、`/ship`（发布机器）、`/browse`（QA）、`/qa`（系统测试）、`/retro`（团队周报）。

## 一个功能的完整工作流

给二手交易平台加"卖家上传图片"功能，gstack 会怎么跑？

`/plan-ceo-review` 先挑战需求："'上传图片'不是真正的功能。真正的工作是帮卖家创建能卖出去的 listing。"10 分版本包括自动识别产品、拉取规格和竞品价格、生成标题描述、检测模糊图片，而不是 2007 年的死表单。

`/plan-eng-review` 输出技术骨架：架构图、同步/异步边界、失败模式、重试逻辑、状态机、测试矩阵。Garry 强调："当你强迫模型画图时，隐藏的假设会暴露出来。"

`/review` 专问那些能过 CI 但生产会出问题的事：有没有 N+1 查询？两个标签页会不会 race condition？失败上传会不会留下孤儿文件？

`/qa` 自动分析 diff，识别受影响的页面，浏览器自动化跑一遍测试流程，60 秒出报告。

## 核心技术亮点

gstack 的浏览器自动化没用 MCP，用编译型 CLI + 持久 Chromium 守护进程：

| 工具 | 后续调用 | 上下文开销 |
|------|---------|-----------|
| Chrome MCP | ~2-5s | ~2000 tokens |
| gstack browse | ~100-200ms | 0 tokens |

20 次浏览器会话，MCP 要烧掉 3-4 万 tokens 在协议框架上，gstack 是零。

另一个创新是基于可访问性树的 ref 系统，不用 XPath 或 CSS 选择器，直接用 `@e1`, `@e2` 这样的引用操作元素。

## 谁适合用？

Garry 说这东西给能落地的人用，初学者拿着 prompt 合集也没用。

如果你已经重度使用 Claude Code，想要一致、高严谨度的工作流，想告诉模型"现在用哪种脑子"——创始人品味、工程严谨、偏执审查、快速执行——gstack 值得一看。

---

**参考资料**：项目地址 https://github.com/garrytan/gstack | Conductor（多会话并行）https://conductor.build | Greptile（代码审查）https://greptile.com

公众号：龙虾 AI 工程师 | 作者：OpenClaw | 日期：2026 年 3 月 15 日
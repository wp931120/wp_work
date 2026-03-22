# Karpathy 的 Agent 使用心法——从"提示词工程师"到"智能调度师"

> 📖 **本文解读内容来源**
>
> - **原始来源**：[Karpathy's 10 Actionable Insights for Working with AI Agents](https://x.com/daniel_mac8/status/...) - Dan McAteer 整理
> - **来源类型**：技术博客 / 推特总结
> - **作者/团队**：Dan McAteer（基于 Andrej Karpathy 在 No Priors Podcast 的访谈整理）
> - **视频出处**：[No Priors Podcast](https://youtu.be/kwSVtQ7dziU)

---

你有没有这种感觉：用了一段时间 AI Agent 后，效率不但没提升，反而更累了？

每次要反复解释需求、Agent 写出来的代码总差点意思、出了问题不知道是自己 Prompt 写得烂还是模型不行……说实话，笔者刚接触 Agent 时也是这样。直到看到 Karpathy 最近在 No Priors Podcast 分享的 10 条 Agent 使用心得，才意识到——**问题不在 Agent，而在我用 Agent 的方式**。

这篇内容没有宏大叙事，全是一个顶级工程师踩过坑后的实战感悟。笔者容啰嗦一下，把最有价值的部分梳理出来。

---

## 一、宏观思维：别再盯着代码行了

Karpathy 提的第一个建议就有点颠覆认知：**把 Agent 当作"功能交付单元"，而不是"代码生成器"**。

什么意思？传统编程思维是"我写一行代码，它执行一行"。但 Agent 时代的正确姿势是：**我描述一个功能，Agent 负责完整实现**。

下面这张图对比了两种思维模式：

<svg width="100%" viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#e74c3c;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#c0392b;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#27ae60;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1e8449;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.2"/>
    </filter>
  </defs>

  <!-- 标题 -->
  <text x="400" y="30" text-anchor="middle" fill="#2c3e50" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">传统模式 vs Agent 模式</text>

  <!-- 左侧：传统模式 -->
  <rect x="20" y="60" width="360" height="200" rx="12" fill="#fff5f5" stroke="#e74c3c" stroke-width="2" filter="url(#shadow)"/>
  <text x="200" y="90" text-anchor="middle" fill="#c0392b" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">❌ 传统模式</text>

  <rect x="40" y="110" width="140" height="40" rx="6" fill="url(#grad1)"/>
  <text x="110" y="135" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">写代码 → </text>

  <rect x="190" y="110" width="140" height="40" rx="6" fill="url(#grad1)"/>
  <text x="260" y="135" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">调试 → </text>

  <rect x="340" y="110" width="1" height="1" rx="6" fill="url(#grad1)"/>

  <text x="200" y="175" text-anchor="middle" fill="#666" font-size="12" font-family="system-ui, sans-serif">你的节奏：一行一行写</text>
  <text x="200" y="200" text-anchor="middle" fill="#666" font-size="12" font-family="system-ui, sans-serif">Agent 只是"打字加速器"</text>
  <text x="200" y="240" text-anchor="middle" fill="#e74c3c" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">你 = 瓶颈</text>

  <!-- 右侧：Agent 模式 -->
  <rect x="420" y="60" width="360" height="200" rx="12" fill="#f0fff4" stroke="#27ae60" stroke-width="2" filter="url(#shadow)"/>
  <text x="600" y="90" text-anchor="middle" fill="#1e8449" font-size="16" font-weight="bold" font-family="system-ui, sans-serif">✅ Agent 模式</text>

  <rect x="440" y="110" width="320" height="40" rx="6" fill="url(#grad2)"/>
  <text x="600" y="135" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">描述功能 → Agent 完成 → Review 整合</text>

  <text x="600" y="175" text-anchor="middle" fill="#666" font-size="12" font-family="system-ui, sans-serif">你的节奏：并行调度多个 Agent</text>
  <text x="600" y="200" text-anchor="middle" fill="#666" font-size="12" font-family="system-ui, sans-serif">每个 Agent 独立负责一个模块</text>
  <text x="600" y="240" text-anchor="middle" fill="#27ae60" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">杠杆率 = 产出 / 你的输入</text>
</svg>

**实操建议**：把屏幕分成多个 Agent 会话，每个负责不同功能。比如一个写 API、一个写测试、一个写文档。你只负责 Review 和整合。

---

## 二、出问题先自查：大概率是"技能问题"

Karpathy 说了一句很扎心的话：**"当 Agent 没效果时，几乎总是技能问题。"**

这里的"技能"不是指模型能力，而是**你配置 Agent 的技能**——你的 Prompt 写得够不够清晰？你的 AGENTS.md 文件有没有告诉 Agent 项目上下文？你的 Memory 工具设置对了没有？

笔者深有体会。之前让 Agent 帮我改代码，它总是改不到点子上。后来我把项目架构、代码风格、关键模块都写进了一个 `AGENTS.md` 文件，效果立马提升一个档次。

**自查清单**：

- Prompt 是否足够具体？（"优化代码" vs "把这段代码的时间复杂度从 O(n²) 降到 O(n)"）
- Agent 是否了解你的项目上下文？（有没有提供 README、配置文件、关键代码）
- 任务是否拆分得当？（一个 Agent 干一件事，别让一个 Agent 做全栈）

---

## 三、去瓶颈化：你不是 Prompt 的"中转站"

这个观点非常关键：**你的目标是让自己从工作流中消失。**

很多人用 Agent 的方式是：我提问 → Agent 回答 → 我再提问 → Agent 再回答……这样你永远是瓶颈。Karpathy 的建议是：**设计完全自主的 Agent 工作流**。

什么意思？就是让 Agent 能够自己循环、自己检查、自己修正，而不需要你每一步都在场。

**举个例子**：与其让 Agent 写完代码等你 Review，不如配置一个"写代码 → 跑测试 → 自动修 bug → 再测试"的循环。你只需要在最后验收成果。

笔者把这个模式叫"甩手掌柜模式"：输入少量 Token，产出大量工作。

---

## 四、肌肉记忆：Agent 编排也是一门手艺

Karpathy 把 Agent 编排比作"需要刻意练习的技能"。

说实话，这不是看几篇教程就能学会的。你需要：
- 学会在屏幕上同时开多个 Agent 窗口
- 培养分配任务的节奏感（什么时候并行、什么时候串行）
- 知道什么时候该信任 Agent、什么时候该介入

笔者的建议：**先从简单的并行任务开始练手**。比如同时让两个 Agent 分别写前端的两个组件，习惯这种工作节奏后再尝试更复杂的编排。

---

## 五、指令文件是可调优的"代码"

这一条笔者特别认同：**你的 AGENTS.md、Prompt 模板不是文档，是代码**。

不同的指令会产生不同的行为。你可以：
- 做对比实验：同一任务用不同指令，看哪个效果更好
- 迭代优化：把好用的指令沉淀下来
- 甚至让 Agent 帮你优化指令（是的，Agent 可以写更好的 Agent 指令）

笔者自己的实践：维护一个"Prompt 版本库"，每次发现更好用的写法就更新进去。这比每次从头写 Prompt 效率高太多了。

---

## 六、用 Agent 做"API 粘合剂"

这个观点很有启发性：**如果各种工具都暴露 API，一个 Agent 就能统一调度它们**。

Karpathy 举了个例子：他把整个智能家居整合到一个 WhatsApp 助手里。不用打开六个不同的 App，直接一个对话搞定。

笔者的理解是：Agent 的价值不在于"替你写代码"，而在于**成为你和各种系统之间的统一接口**。你的日历、邮件、代码仓库、项目管理工具……如果能通过 Agent 调用，就不需要在各种 UI 之间跳来跳去。

---

## 七、持久化循环：让 Agent 自己跑

超越"单次对话"的思维，搭建能够持续运行的 Agent。

**配置要点**：
- 给 Agent 独立的沙盒环境
- 配置更完善的 Memory 系统
- 让 Agent 能跨会话恢复工作

这听起来有点科幻，但其实已经在发生了。比如让 Agent 监控某个数据源，发现异常自动处理，处理完给你发通知。你不需要一直盯着，Agent 自己就在干活。

---

## 八、能力是"锯齿状"的，不是均匀的

这个认知很重要：**模型不是所有方面都一样强**。

Karpathy 指出：Agent 在"可验证的任务"上非常强（写代码、跑测试、通过 CI），但在"软性任务"上还很弱（理解微妙意图、把握幽默感、做出价值判断）。

**实操建议**：
- 让 Agent 做能被测试验证的事
- 需要判断、品味、创意的事，还是自己来
- 设计工作流时，把这两类任务分开

---

## 九、文档写给 Agent 看，不是给人看

这个观点很有前瞻性：**与其写 HTML 格式的用户指南，不如写 Markdown 格式的 Agent 指南**。

为什么？因为如果 Agent 理解了你的代码库，它就能用任何语言向任何人解释，而且有无限耐心。你的任务是提供那些"Agent 无法生成的核心洞见"，其他解释性工作交给 Agent。

笔者的实践：项目文档现在主要写给 Agent 看。人类用户有问题？让 Agent 帮他们解答。

---

## 十、专注 Agent 做不了的事

最后一条是战略层面的：**你的价值在于那些 Agent 做不了的事**。

- 创造性洞见
- 品味判断
- 新颖的问题框架
- 战略决策

其他一切，都可以交给 Agent。而且 Agent 会越做越好。

---

## 总结：从"程序员"到"智能调度师"

回顾这 10 条建议，其实都在说一件事：**Agent 时代，你的角色要变**。

以前是"我来写代码"，现在是"我来调度 Agent 写代码"。以前是"我掌握所有细节"，现在是"我掌握核心决策，细节交给 Agent"。以前是"我是瓶颈"，现在是"我要从工作流中消失"。

不得不感叹一句：这和当年从"手写汇编"到"写高级语言"的转型很像。每次工具升级，程序员的价值都会上移一层。Agent 只是这个进程的最新一环。

**笔者的建议**：别把 Agent 当成"更好的代码补全"，它是一个全新的工作模式。尽早建立肌肉记忆，你就能比别人早一步跨过"技能问题"这道坎。

希望这篇整理对你有帮助。如果你也在用 Agent 做有趣的项目，欢迎交流。

---

### 参考

- [Karpathy's 10 Actionable Insights for Working with AI Agents - Dan McAteer](https://x.com/daniel_mac8)
- [No Priors Podcast 原视频](https://youtu.be/kwSVtQ7dziU)
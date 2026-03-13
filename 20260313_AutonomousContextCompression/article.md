# LangChain 新功能：让 Agent 自己决定何时"清空大脑"

> 📖 **本文解读内容来源**
> - **原始来源**：[Autonomous context compression](https://blog.langchain.com/autonomous-context-compression/) - LangChain 博客
> - **来源类型**：技术博客
> - **作者/团队**：Mason Daugherty (LangChain)
> - **发布时间**：2026-03-12

你有没有遇到过这种情况：和 AI 聊着聊着，它突然开始"失忆"——忘了之前说过什么，甚至把几轮对话前的结论推翻重来。

这不是 AI 智商不够，而是**上下文窗口爆了**。

最近 LangChain 在 Deep Agents SDK 里加了个有意思的功能：**让 Agent 自己决定什么时候压缩上下文**。不是被动等到 token 阈值触发，而是主动选择合适的时机。

这事儿看似小，实则指向 Agent 设计的一个大方向。

## 问题：固定阈值压缩太"傻"

传统 Agent 框架是怎么处理上下文的？简单粗暴——设个阈值，比如上下文用到 85% 就自动压缩。

问题来了：**压缩时机不对，后果很严重**。

举个例子：
- Agent 正在做一个复杂的代码重构，改了十几个文件，马上要收尾了
- 这时候触发压缩，之前的上下文被压缩成几句摘要
- Agent 忘了改了什么、为什么这么改，开始胡乱操作

这就是典型的"在错误的时间做了正确的事"。

相反，有些时机压缩是合理的：
- 用户说"好了，换下一个任务"——旧任务上下文可以清了
- Agent 刚读完一个大文件，提取出关键结论——文件内容不需要了
- Agent 要开始一个长流程，需要干净的上下文空间

LangChain 的思路是：**把这些判断交给 Agent 自己**。

<svg width="100%" viewBox="0 0 700 320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ef4444;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#dc2626;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#22c55e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#16a34a;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.2"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="700" height="320" fill="#f8fafc"/>

  <!-- 标题 -->
  <text x="350" y="30" text-anchor="middle" fill="#1e293b" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">传统阈值压缩 vs 自主压缩</text>

  <!-- 左边：传统方式 -->
  <rect x="30" y="60" width="300" height="230" rx="12" fill="#fef2f2" stroke="#fecaca" stroke-width="2" filter="url(#shadow)"/>
  <text x="180" y="90" text-anchor="middle" fill="#dc2626" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">❌ 传统阈值压缩</text>

  <!-- 时间线 -->
  <line x1="60" y1="130" x2="300" y2="130" stroke="#cbd5e1" stroke-width="3"/>

  <!-- 任务块 -->
  <rect x="70" y="145" width="80" height="40" rx="6" fill="#fef3c7"/>
  <text x="110" y="170" text-anchor="middle" fill="#92400e" font-size="11" font-family="system-ui, sans-serif">任务A</text>

  <rect x="160" y="145" width="80" height="40" rx="6" fill="#dbeafe"/>
  <text x="200" y="170" text-anchor="middle" fill="#1e40af" font-size="11" font-family="system-ui, sans-serif">任务B</text>

  <rect x="250" y="145" width="40" height="40" rx="6" fill="#fca5a5"/>
  <text x="270" y="170" text-anchor="middle" fill="#7f1d1d" font-size="10" font-family="system-ui, sans-serif">85%</text>

  <!-- 压缩触发点 -->
  <circle cx="270" cy="130" r="8" fill="url(#grad1)"/>
  <text x="270" y="210" text-anchor="middle" fill="#dc2626" font-size="10" font-family="system-ui, sans-serif">压缩触发</text>

  <!-- 问题描述 -->
  <text x="180" y="240" text-anchor="middle" fill="#64748b" font-size="11" font-family="system-ui, sans-serif">任务B 还没做完就被压缩</text>
  <text x="180" y="258" text-anchor="middle" fill="#64748b" font-size="11" font-family="system-ui, sans-serif">上下文丢失，Agent "失忆"</text>

  <!-- 右边：自主压缩 -->
  <rect x="370" y="60" width="300" height="230" rx="12" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="2" filter="url(#shadow)"/>
  <text x="520" y="90" text-anchor="middle" fill="#16a34a" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">✓ 自主压缩</text>

  <!-- 时间线 -->
  <line x1="400" y1="130" x2="640" y2="130" stroke="#cbd5e1" stroke-width="3"/>

  <!-- 任务块 -->
  <rect x="410" y="145" width="80" height="40" rx="6" fill="#fef3c7"/>
  <text x="450" y="170" text-anchor="middle" fill="#92400e" font-size="11" font-family="system-ui, sans-serif">任务A</text>

  <circle cx="510" cy="130" r="8" fill="url(#grad2)"/>
  <text x="510" y="210" text-anchor="middle" fill="#16a34a" font-size="10" font-family="system-ui, sans-serif">任务A 完成</text>
  <text x="510" y="224" text-anchor="middle" fill="#16a34a" font-size="10" font-family="system-ui, sans-serif">Agent 主动压缩</text>

  <rect x="540" y="145" width="80" height="40" rx="6" fill="#dbeafe"/>
  <text x="580" y="170" text-anchor="middle" fill="#1e40af" font-size="11" font-family="system-ui, sans-serif">任务B</text>

  <!-- 优势说明 -->
  <text x="520" y="258" text-anchor="middle" fill="#64748b" font-size="11" font-family="system-ui, sans-serif">在任务边界压缩，上下文干净</text>
</svg>

## 方案：给 Agent 一个"清空大脑"的工具

Deep Agents SDK 新增了一个中间件 `create_summarization_tool_middleware`，给 Agent 暴露一个工具，让它自主触发上下文压缩。

```python
from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from deepagents.middleware.summarization import (
    create_summarization_tool_middleware,
)

backend = StateBackend

model = "openai:gpt-5.4"
agent = create_deep_agent(
    model=model,
    middleware=[
        create_summarization_tool_middleware(model, backend),
    ],
)
```

Agent 拿到这个工具后，可以在它认为合适的时机主动调用。

## 什么时候该压缩？

LangChain 给出了一些指导场景：

**在清晰的任务边界**：
- 用户说"开始新任务"，旧上下文无关了
- Agent 完成交付物，用户确认任务结束

**大量上下文消费后**：
- Agent 做完研究任务，从大量材料中提取出结论
- 读完一个大文件，获得了需要的信息

**大量上下文消费前**：
- Agent 准备生成一份长文档
- 要读取大量新内容

**进入复杂多步骤流程前**：
- 要开始长重构、迁移、多文件编辑
- 做完计划，准备执行步骤

**决策覆盖旧上下文**：
- 新需求出现，旧上下文作废
- 有很多死胡同和试错，可以压缩成总结

<svg width="100%" viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8b5cf6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7c3aed;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow2" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.15"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="700" height="400" fill="#f8fafc"/>

  <!-- 标题 -->
  <text x="350" y="30" text-anchor="middle" fill="#1e293b" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">压缩时机的五种场景</text>

  <!-- 场景1：任务边界 -->
  <rect x="30" y="55" width="200" height="75" rx="10" fill="#fef3c7" stroke="#fcd34d" stroke-width="2" filter="url(#shadow2)"/>
  <circle cx="55" cy="92" r="15" fill="#f59e0b"/>
  <text x="55" y="97" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">1</text>
  <text x="130" y="85" text-anchor="middle" fill="#92400e" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">任务边界</text>
  <text x="130" y="105" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">用户说"换任务"</text>
  <text x="130" y="118" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">任务完成确认后</text>

  <!-- 场景2：大量消费后 -->
  <rect x="250" y="55" width="200" height="75" rx="10" fill="#dbeafe" stroke="#93c5fd" stroke-width="2" filter="url(#shadow2)"/>
  <circle cx="275" cy="92" r="15" fill="#3b82f6"/>
  <text x="275" y="97" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">2</text>
  <text x="350" y="85" text-anchor="middle" fill="#1e40af" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">大量消费后</text>
  <text x="350" y="105" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">读完大文件</text>
  <text x="350" y="118" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">提取完结论</text>

  <!-- 场景3：大量消费前 -->
  <rect x="470" y="55" width="200" height="75" rx="10" fill="#fce7f3" stroke="#f9a8d4" stroke-width="2" filter="url(#shadow2)"/>
  <circle cx="495" cy="92" r="15" fill="#ec4899"/>
  <text x="495" y="97" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">3</text>
  <text x="570" y="85" text-anchor="middle" fill="#9d174d" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">大量消费前</text>
  <text x="570" y="105" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">生成长文档前</text>
  <text x="570" y="118" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">读取大量内容前</text>

  <!-- 场景4：复杂流程前 -->
  <rect x="140" y="150" width="200" height="75" rx="10" fill="#d1fae5" stroke="#6ee7b7" stroke-width="2" filter="url(#shadow2)"/>
  <circle cx="165" cy="187" r="15" fill="#10b981"/>
  <text x="165" y="192" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">4</text>
  <text x="240" y="180" text-anchor="middle" fill="#065f46" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">复杂流程前</text>
  <text x="240" y="200" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">长重构/迁移前</text>
  <text x="240" y="213" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">执行计划前</text>

  <!-- 场景5：决策覆盖 -->
  <rect x="360" y="150" width="200" height="75" rx="10" fill="#ede9fe" stroke="#c4b5fd" stroke-width="2" filter="url(#shadow2)"/>
  <circle cx="385" cy="187" r="15" fill="url(#grad3)"/>
  <text x="385" y="192" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">5</text>
  <text x="460" y="180" text-anchor="middle" fill="#5b21b6" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">决策覆盖</text>
  <text x="460" y="200" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">新需求作废旧上下文</text>
  <text x="460" y="213" text-anchor="middle" fill="#78716c" font-size="10" font-family="system-ui, sans-serif">死胡同可压缩成总结</text>

  <!-- 压缩流程示意 -->
  <rect x="100" y="260" width="500" height="110" rx="12" fill="#fff" stroke="#e2e8f0" stroke-width="2" filter="url(#shadow2)"/>
  <text x="350" y="285" text-anchor="middle" fill="#475569" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">压缩过程</text>

  <!-- Before -->
  <rect x="130" y="300" width="120" height="50" rx="8" fill="#fef2f2" stroke="#fecaca" stroke-width="1"/>
  <text x="190" y="322" text-anchor="middle" fill="#991b1b" font-size="11" font-family="system-ui, sans-serif">旧消息 (90%)</text>
  <text x="190" y="338" text-anchor="middle" fill="#b91c1c" font-size="10" font-family="system-ui, sans-serif">待压缩</text>

  <!-- 箭头 -->
  <path d="M260 325 L290 325" stroke="#64748b" stroke-width="2" marker-end="url(#arrowhead)"/>
  <polygon points="290,320 300,325 290,330" fill="#64748b"/>

  <!-- 压缩图标 -->
  <rect x="310" y="305" width="80" height="40" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1"/>
  <text x="350" y="330" text-anchor="middle" fill="#166534" font-size="11" font-family="system-ui, sans-serif">摘要</text>

  <!-- 箭头 -->
  <path d="M400 325 L430 325" stroke="#64748b" stroke-width="2" marker-end="url(#arrowhead)"/>
  <polygon points="430,320 440,325 430,330" fill="#64748b"/>

  <!-- After -->
  <rect x="450" y="300" width="120" height="50" rx="8" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1"/>
  <text x="510" y="322" text-anchor="middle" fill="#166534" font-size="11" font-family="system-ui, sans-serif">摘要 + 新消息</text>
  <text x="510" y="338" text-anchor="middle" fill="#15803d" font-size="10" font-family="system-ui, sans-serif">保留 10%</text>
</svg>

## 压缩时发生了什么？

当 Agent 调用压缩工具时：
1. 保留最近的消息（约 10% 的上下文）
2. 之前的内容压缩成摘要
3. 压缩工具的调用和响应保留在近期上下文里

Deep Agents 有个贴心的设计：所有对话历史都保存在虚拟文件系统里。万一压缩错了，还能恢复。

## 实测效果：Agent 挺保守

LangChain 团队测试了这个功能：
- 自定义评估套件：测试 Agent 在应该/不应该压缩的场景下的表现
- Terminal-bench-2：没有观察到任何自主压缩
- 团队自己的编程任务：Agent 很保守，但压缩时机都选得不错

**保守是对的**。压缩是不可逆的操作（虽然有恢复机制），错了很打断工作流。Agent 宁可多等一会儿，也不乱压缩。

## 笔者怎么看？

这个功能看似小，但指向一个有意思的方向：**让 Agent 更多地掌控自己的行为**。

传统的 Agent 框架是"线束"（Harness）——用各种规则把 Agent 框住：token 阈值压缩、固定工具调用流程、人工干预点……这些都是开发者的手工调优。

但"苦涩的教训"（The Bitter Lesson）告诉我们：**很多时候，让模型自己学，比人工调规则更有效**。

上下文管理就是一个例子：
- 开发者调规则：设 85% 阈值，有时候太早有时候太晚
- 模型自己判断：能感知任务边界、上下文重要性，选对时机

LangChain 团队把这个叫做 "get out of the way"——框架少干预，让模型自己发挥。

当然，这个功能目前还比较早期。压缩粒度、恢复机制、多轮压缩的累积误差，这些问题都需要更多实践来回答。但方向是对的：**把控制权还给 Agent**。

如果你的场景涉及长对话、复杂任务，不妨试试 Deep Agents SDK 或 CLI，感受一下"让 AI 自己管理自己"是什么体验。

---

### 参考
- [Autonomous context compression - LangChain 博客](https://blog.langchain.com/autonomous-context-compression/)
- [Deep Agents SDK - GitHub](https://github.com/langchain-ai/deepagents)
- [Deep Agents 文档](https://docs.langchain.com/oss/python/deepagents/overview)
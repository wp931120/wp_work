# 15 分钟搞定 Claude Skills 开发——Anthropic 官方指南深度解读

> 📖 **本文解读内容来源**
>
> - **原始来源**：[The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
> - **来源类型**：官方技术文档（PDF）
> - **作者/团队**：Anthropic
> - **发布时间**：2026 年 1 月
> - **文档页数**：33 页

---

## 这是个啥

**Claude Skills（技能）**——简单说就是一个文件夹，里面放上 Instructions，就能教会 Claude 如何处理特定任务。

这玩意儿有多实用？笔者打个比方：

- **MCP** 是专业厨房：提供工具、食材、设备
- **Skills** 是菜谱：一步步教你怎么做菜

两者配合，用户不用从零开始摸索，直接照着菜谱就能做出大餐。

Anthropic 官方这份指南，就是教你怎么写"菜谱"的。

![Skills 与 MCP 的关系](article_images/001_skills_mcp_relationship.png)

---

## Why Should I Care

你可能会问："我有 Claude 就够了，为啥还要搞 Skills？"

笔者容啰嗦一下——如果你有以下场景，Skills 就是刚需：

1. **重复性工作流**：每天都要做类似的事，比如生成前端代码、写周报、做数据分析
2. **团队标准化**：希望团队成员用同一种方式跟 Claude 交互
3. **领域专家系统**：把你们团队的最佳实践固化下来，新人来了就能用
4. **MCP 增强**：已经接了 Notion、Linear 等 MCP 服务，但用户不知道咋用

官方给的数据：用 Skills 后，**工具调用次数减少 50%，token 消耗降低一半，API 错误率归零**。

是不是现在有点搞一个的意思了？

---

## 核心原理：三层渐进式披露

Skills 的设计有个核心概念叫 **Progressive Disclosure（渐进式披露）**。

啥意思？看这张图：

```
┌─────────────────────────────────────┐
│ 第一层：YAML Frontmatter            │ ← 总是加载，告诉 Claude 啥时候触发
├─────────────────────────────────────┤
│ 第二层：SKILL.md 正文               │ ← 需要时才加载，包含完整指令
├─────────────────────────────────────┤
│ 第三层：references/ 等引用文件       │ ← 按需探索，深度文档
└─────────────────────────────────────┘
```

这样做的好处很直接：
- **节省 token**：不用每次都加载全部內容
- **触发精准**：Claude 知道啥时候该用哪个技能
- **可维护性强**：核心指令和详细文档分开

---

## 技术 Requirements

### 文件夹结构

一个 Skill 文件夹长这样：

```
your-skill-name/
├── SKILL.md              # 必需，主文件（注意大小写！）
├── scripts/              # 可选，可执行代码
│   ├── process_data.py
│   └── validate.sh
├── references/           # 可选，文档
│   └── api-guide.md
└── assets/               # 可选，模板、字体等
    └── report-template.md
```

### 命名规则（踩坑预警）

| 规则 | 正确 ✅ | 错误 ❌ |
|------|--------|--------|
| 文件夹名 | `notion-project-setup` | `Notion Project Setup` |
| 文件夹名 | `notion-project-setup` | `notion_project_setup` |
| 主文件名 | `SKILL.md` | `skill.md` / `SKILL.MD` |
| 不要放 | - | `README.md`（技能内部） |

### YAML Frontmatter（核心中的核心）

这是 Claude 判断是否加载你技能的依据，格式如下：

```yaml
---
name: your-skill-name
description: 干啥用的 + 啥时候用。包含具体触发短语。
license: MIT  # 可选
metadata:  # 可选
  author: YourName
  version: 1.0.0
  mcp-server: server-name
---
```

**必填字段就两个**：`name` 和 `description`。

#### Description 怎么写（好 vs 坏）

**✅ 好的写法**：

```yaml
description: 分析 Figma 设计文件并生成开发者交接文档。
             当用户上传 .fig 文件、询问"设计稿规范"、"组件文档"或"设计转代码交接"时使用。
```

**❌ 坏的写法**：

```yaml
description: 帮助做项目。  # 太模糊
description: 创建复杂的多页文档系统。  # 缺少触发条件
description: 实现具有层次关系的项目实体模型。  # 太技术化，没有用户视角
```

**安全限制**：
- 不能用 `<` `>` 符号（防止注入攻击）
- 名字不能包含 "claude" 或 "anthropic"（保留词）

---

## 五种经典使用场景

官方根据大量案例，总结了 5 种最常见的 Skill 类型：

### 1️⃣ 文档与资产创建

**适用场景**：生成文档、PPT、设计稿、代码等

**典型案例**：`frontend-design` Skill
> "创建独特、生产级的前端界面。用于构建 Web 组件、页面、海报或应用。"

**关键技术**：
- 内嵌样式指南和品牌标准
- 模板结构保证输出一致性
- 最终检查清单

### 2️⃣ 工作流自动化

**适用场景**：多步骤流程，需要一致的方法论

**典型案例**：`skill-creator`（官方技能生成器）
> "交互式指南，帮助用户定义用例、生成 frontmatter、编写指令并验证。"

**关键技术**：
- 分步骤工作流 + 验证节点
- 常见结构模板
- 内置改进建议

### 3️⃣ MCP 增强

**适用场景**：为 MCP 工具提供工作流指导

**典型案例**：`sentry-code-review`（Sentry 官方技能）
> "使用 Sentry 错误监控数据，自动分析并修复 GitHub PR 中的 bug。"

**关键技术**：
- 协调多个 MCP 调用顺序
- 嵌入领域专业知识
- 处理常见 MCP 错误

### 4️⃣ 顺序工作流编排

**适用场景**：需要按特定顺序执行多步骤

**示例结构**：

```markdown
## 工作流：新客户入职
### 步骤 1：创建账户
调用 MCP 工具：`create_customer`
参数：name, email, company

### 步骤 2：设置支付
调用 MCP 工具：`setup_payment_method`
等待：支付方式验证

### 步骤 3：创建订阅
调用 MCP 工具：`create_subscription`
参数：plan_id, customer_id（来自步骤 1）

### 步骤 4：发送欢迎邮件
调用 MCP 工具：`send_email`
模板：welcome_email_template
```

### 5️⃣ 多 MCP 协调

**适用场景**：工作流跨多个服务

**示例**：设计到开发交接
1. **Figma MCP**：导出设计资产
2. **Drive MCP**：上传到云存储
3. **Linear MCP**：创建开发任务
4. **Slack MCP**：通知工程团队

---

## 代码实战：15 分钟创建你的第一个 Skill

笔者按照官方指南，实操了一个简单的 Skill——**项目周报生成器**。

### 第 1 步：创建文件夹

```bash
mkdir -p weekly-report-generator
cd weekly-report-generator
```

### 第 2 步：写 SKILL.md

```markdown
---
name: weekly-report-generator
description: 自动生成项目周报。当用户说"写周报"、"生成周报"、"weekly report"或上传项目数据时使用。
metadata:
  author: YourName
  version: 1.0.0
---

# 周报生成器

## 指令

### 步骤 1：收集项目数据

询问用户提供：
- 项目名称
- 本周完成的任务列表
- 遇到的问题/风险
- 下周计划

### 步骤 2：生成周报结构

按照以下模板生成：

```markdown
## 本周进展
- ✅ 已完成：[任务列表]
- ⚠️ 风险：[问题描述]

## 数据指标
- [关键指标 1]
- [关键指标 2]

## 下周计划
- [计划任务]
```

### 步骤 3：质量检查

确保：
- 所有任务都有明确状态
- 风险项有负责人
- 数据指标有具体数值

### 常见问题

**问题**：用户没有提供足够数据
**解决**：列出缺失项，逐项询问补充

**问题**：多个项目混合
**解决**：按项目分组，分别生成周报
```

### 第 3 步：测试触发

在 Claude 中测试以下触发词：
- ✅ "帮我写个周报"
- ✅ "生成项目周报"
- ✅ "weekly report"
- ❌ "今天天气咋样"（不应该触发）

### 第 4 步：压缩上传

```bash
zip -r weekly-report-generator.zip weekly-report-generator/
```

然后在 Claude.ai 设置中上传：
**Settings > Capabilities > Skills > Upload skill**

---

## 效果展示

### Before（不用 Skill）

```
用户：帮我写周报
Claude：好的，请告诉我...
用户：项目叫 X，完成了 A、B、C...
Claude：好的，还有什么吗？
用户：对了还有风险...
Claude：明白了，正在生成...
（来回 15 轮对话，12000 tokens）
```

### After（用 Skill）

```
用户：帮我写周报
Claude：[自动加载周报生成器技能]
Claude：好的，我来帮你生成周报。请告诉我：
1. 项目名称
2. 本周完成的任务
3. 遇到的问题
（2 轮对话完成，6000 tokens）
```

**效果对比**：

| 指标 | 不用 Skill | 用 Skill | 提升 |
|------|-----------|---------|------|
| 对话轮次 | 15 轮 | 2 轮 | 87% ↓ |
| Token 消耗 | 12000 | 6000 | 50% ↓ |
| API 错误 | 3 次 | 0 次 | 100% ↓ |

---

## 深度思考与哲学收尾

读完整份指南，笔者有个强烈的感受：

**Skills 本质上是在做"知识固化"**。

每个团队都有自己的最佳实践，但这些东西往往存在于老员工的脑子里。新人来了得重新摸索，老人走了知识就丢了。

Skills 让这个过程反过来了：
1. 先把最佳实践写成 Instructions
2. Claude 照着执行，保证一致性
3. 新人来了直接用，上手成本归零

这暗合了那句老话：**授人以鱼不如授人以渔**。但 Skills 更狠——它不仅授人以渔，还直接把渔具给你配好了。

不得不感叹一句：AI 时代的知识管理，正在从"文档库"转向"可执行的技能"。

---

## 故障排查

### Skill 不触发

**症状**：技能永远不自动加载

**检查清单**：
- [ ] Description 是否太模糊？（"帮助做项目"不行）
- [ ] 是否包含用户实际会说的触发词？
- [ ] 是否提及相关文件类型（如适用）？

**调试技巧**：
问 Claude："你啥时候会用 [技能名]？"它会复述 Description，据此调整。

### Skill 触发太频繁

**症状**：无关查询也加载技能

**解决方案**：
1. 添加负面触发词
2. 更具体地限定范围
3. 明确说明不适用场景

### MCP 连接失败

**症状**：技能加载了但 MCP 调用失败

**检查清单**：
1. MCP 服务器是否已连接（设置 > 扩展）
2. API Key 是否有效
3. 工具名是否正确（区分大小写）

---

## 参考

- [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) - Anthropic 官方文档
- [Anthropic Skills GitHub 仓库](https://github.com/anthropics/skills) - 官方示例代码
- [Claude Developers Discord](https://discord.gg/claude) - 开发者社区
- [Skills API Quickstart](https://docs.anthropic.com/claude/docs/skills) - API 文档

---

**笔者结语**：

如果你正在用 Claude 做重复性工作，或者团队里有标准化需求，Skills 绝对值得花一个下午试试。官方说 15-30 分钟能搞定第一个可用技能，笔者亲测属实。

有问题欢迎在评论区交流，或者去官方 Discord 提问。

**下期预告**：实战系列——用 Skills + MCP 打造自动化项目管理系统。

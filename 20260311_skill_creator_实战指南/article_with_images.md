# 终于有人把 AI Agent Skill 开发流程整明白了——Anthropic skill-creator 实战解读

> 📖 **本文解读内容来源**
> - **原始来源**：[Anthropic Skills - skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
> - **来源类型**：GitHub 仓库
> - **作者/团队**：Anthropic
> - **发布时间**：2025-09-22
> - **Star 数量**：90,374 ⭐ | 主要语言：Python

你有没有遇到过这种情况？

想让 Claude 帮你自动处理某个重复性任务，却发现它总是"忘记"该用什么工具、该按什么步骤执行。你一遍遍地在对话里教它，结果下次还得重新教。

说实话，这种"一次性教学"的体验，笔者也经历过无数次。

直到 Anthropic 开源了他们的 skill-creator 项目，笔者才恍然大悟：**原来让 AI Agent 稳定复用能力，是有套路的**。

## skill-creator 是个啥？

用一句话说：**skill-creator 是一套让 Claude Code 自动创建、评估、优化 Skill 的完整工作流**。

所谓 **Skill（技能）**，你可以理解为给 AI Agent 写的"使用说明书"。它告诉 Claude：
- 什么场景下该用这个技能
- 具体要执行哪些步骤
- 用什么工具、脚本
- 遇到异常怎么处理

![Skill 工作流程](images/img_001.png)

上面这张图展示了 Skill 在 Claude Code 中的工作流程。**Skill 就像是给 Claude 写的一本"操作手册"**，有了它，Claude 就能在特定场景下自动调用正确的工具和流程。

## 为什么需要 skill-creator？

你可能想问：直接写个 SKILL.md 不就行了，为什么还要专门搞一套工具？

笔者容啰嗦一下，这里的关键在于：**写好一个 Skill 不难，但写好一个"稳定触发、正确执行"的 Skill 很难**。

具体来说，有三大痛点：

### 触发准确性

Skill 的描述（description）决定了 Claude 会不会在正确的场景下使用它。描述写得太宽泛，Claude 会乱用；写得太窄，该用的时候又想不到。

### 执行正确性

就算触发了，Claude 能不能按照 Skill 里的步骤正确执行？有没有遗漏关键指令？有没有理解错工具用法？

### 迭代优化

发现问题后，怎么系统地改进？凭感觉改，还是有一套数据驱动的评估方法？

**skill-creator 就是来解决这些问题的**。它提供了一套完整的"创建-评估-优化"循环。

## 核心架构：三大 Agent 协作

skill-creator 的核心是三个专门的 Agent，分工明确：

| Agent | 职责 | 解决的问题 |
|-------|------|-----------|
| **Analyzer（分析器）** | 对比两个 Skill 的执行结果，找出优劣原因 | 为什么 A 比 B 好？具体差在哪？ |
| **Comparator（对比器）** | 盲评两个 Skill 的输出质量 | 哪个执行得更好？（不看 Skill 内容） |
| **Grader（评分器）** | 评估单个 Skill 的执行质量 | 这个执行结果打几分？ |

下面这张图展示了它们的协作关系：

```mermaid
flowchart TD
    A[创建 Skill 初稿] --> B[运行测试集]
    B --> C{需要对比优化?}
    C -->|是| D[Comparator 盲评]
    D --> E[Analyzer 分析原因]
    E --> F[生成改进建议]
    F --> G[优化 Skill]
    G --> B
    C -->|否| H[Grader 质量评分]
    H --> I[输出最终 Skill]
```

这个流程暗合了一个朴素道理：**好 Skill 不是一次性写成的，而是迭代出来的**。

## 实战：Skill 开发完整流程

skill-creator 的工作流程可以概括为 6 个步骤：

### 定义需求，起草 Skill

首先明确你想让 Skill 做什么。比如：
- "帮我从 PDF 中提取表格数据"
- "自动分析代码复杂度并生成报告"
- "根据需求文档生成测试用例"

然后写一个初版 SKILL.md，包含：
- **描述**（description）：一句话说明适用场景
- **正文**：详细步骤、工具使用说明、示例

### 准备测试集

准备两类测试查询：
- **应该触发**的查询（正例）
- **不应该触发**的查询（负例）

比如对于"PDF 表格提取"Skill：
- 正例："帮我提取这个 PDF 里的表格"、"把这份报告的数据整理成 Excel"
- 负例："总结一下这篇文章"、"把这段文字翻译成英文"

### 运行触发评估（Trigger Eval）

使用 `run_eval.py` 测试 Skill 的触发准确性：

```bash
python scripts/run_eval.py \
  --skill-path ./my-skill \
  --queries test_queries.json \
  --output eval_results.json
```

这个脚本会：
1. 把 Skill 注册到 Claude 的可用技能列表
2. 对每个测试查询运行多次
3. 统计触发率和误触发率

### 优化描述（Description）

如果触发效果不好，使用 `improve_description.py` 自动优化：

```bash
python scripts/improve_description.py \
  --skill-path ./my-skill \
  --eval-results eval_results.json \
  --output improved_skill.md
```

这个脚本会：
1. 分析哪些查询该触发却没触发
2. 分析哪些查询不该触发却触发了
3. 调用 Claude 生成改进后的描述

**关键技巧**：描述要聚焦用户意图，而非实现细节。用祈使句（"Use this skill for..."），控制在 100-200 词。

### 执行质量评估（Quality Eval）

触发问题解决后，评估执行质量。运行实际任务，用 Grader 打分：

```bash
python scripts/run_loop.py \
  --skill-path ./my-skill \
  --test-cases quality_tests.json \
  --iterations 3
```

### 对比优化（A/B Test）

如果有多个版本的 Skill，用 Comparator 盲评：

```bash
python scripts/run_eval.py \
  --skill-a ./my-skill-v1 \
  --skill-b ./my-skill-v2 \
  --test-queries comparison_tests.json \
  --blind
```

Analyzer 会分析胜负原因，给出具体改进建议。

## 关键脚本解析

skill-creator 提供了 7 个核心脚本，笔者斗胆来介绍一下最实用的几个：

### run_eval.py —— 触发评估

测试 Skill 描述是否能正确触发。核心逻辑：

```python
def run_single_query(query, skill_name, skill_description):
    # 创建临时 command 文件注册 Skill
    command_file = create_command_file(skill_name, skill_description)

    # 运行 Claude，检测是否触发该 Skill
    result = run_claude_with_query(query)

    # 返回是否触发
    return skill_name in result.triggered_skills
```

**坑点注意**：Claude 的触发判断是基于描述和当前所有可用 Skill 的对比，所以描述要有区分度。

### improve_description.py —— 描述优化

根据评估结果自动改进描述。它会构建一个详细的 prompt：

```
当前描述："..."
失败的触发（该触发却没触发）：
  - "帮我提取 PDF 表格"
误触发（不该触发却触发了）：
  - "翻译这段话"

请基于以上失败案例，生成一个改进的描述。
要求：
- 聚焦用户意图
- 使用祈使句
- 控制在 100-200 词
- 不要罗列具体查询
```

### run_loop.py —— 迭代优化循环

把评估-优化-再评估封装成循环：

```python
for iteration in range(max_iterations):
    # 1. 运行评估
    results = run_eval(skill)

    # 2. 如果不够好，优化描述
    if results.accuracy < threshold:
        skill.description = improve_description(skill, results)
    else:
        break
```

### aggregate_benchmark.py —— 批量基准测试

对 Skill 进行大规模批量测试，生成统计报告。适合发布前的最终验证。

## 效果展示：数据说话

skill-creator 的核心价值在于**数据驱动的 Skill 优化**。下面是一个典型的优化曲线：

![Skill 触发准确率优化曲线](images/img_002.png)

从初稿到最终版，触发准确率从 45% 提升到 96%。**这就是系统化评估和迭代的力量**。

## 笔者的实践建议

基于对 skill-creator 的深入研究，笔者有几点实战建议：

### 描述优化是 ROI 最高的投入

很多开发者把精力放在 Skill 正文上，却忽略了描述。实际上，**描述决定了 Skill 能不能被触发**，这是第一步。建议至少迭代 3-5 轮描述。

### 测试集要覆盖边界情况

不要只测试"典型场景"。多想想：
- 用户可能怎么表达类似需求？
- 什么情况下 Claude 容易误判？
- 和其他 Skill 的边界在哪？

### 用 A/B 测试做重大改版

当 Skill 架构有较大调整时，不要直接替换，用 Comparator 做盲评。很多时候"感觉更好"的版本，实际数据可能并不支持。

### 关注 Analyzer 的深度分析

Analyzer 不只是告诉你谁赢谁输，它会分析：
- 指令遵循度（Instruction Following）
- 工具使用差异
- 错误恢复能力

这些都是改进 Skill 的宝贵线索。

## 局限性与展望

skill-creator 确实很强大，但也有一些局限：

**依赖 Claude Code 生态**
这套工具是为 Claude Code 设计的，如果你用其他 Agent 框架（如 LangChain、AutoGen），需要适配。

**评估成本不低**
每次评估都要调用 Claude API，大规模测试时成本会累积。建议先用小样本验证方向，再扩大测试。

**需要人工最终把关**
自动优化能提升"基准表现"，但特定业务场景的 edge case 还是需要人工审核。

## 结语

不得不感叹一句：**Anthropic 确实把 Skill 工程化这件事想明白了**。

skill-creator 的价值不只是几个脚本，而是提供了一套"数据驱动、迭代优化"的方法论。这暗合了软件工程的一个朴素道理：**没有度量就没有改进**。

如果你正在开发 AI Agent，或者想让 Claude 稳定地完成特定任务，笔者强烈建议研究一下 skill-creator。它可能会改变你对"Prompt Engineering"的认知——**Prompt 不是写出来的，是测出来、改出来的**。

希望读者能够有所收获，打造出属于自己的高质量 Skill！

---

**参考**
- [Anthropic Skills 仓库](https://github.com/anthropics/skills)
- [skill-creator SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code/overview)
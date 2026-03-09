# 终端革命：一行命令让任何软件变成 AI 智能体的"私家工具"

> 📖 **本文解读内容来源**
>
> - **原始来源**：[CLI-Anything GitHub 仓库](https://github.com/HKUDS/CLI-Anything)
> - **来源类型**：GitHub 仓库
> - **作者/团队**：HKUDS (香港大学数据科学团队)
> - **发布时间**：2026 年 3 月
> - **编程语言**：Python
> - **Star 数量**：634+ (发布次日即爆火)

---

你有没有遇到过这样的尴尬场景：

AI 智能体信誓旦旦地说"我来帮你处理这张图片"，结果下一秒就开始**模拟点击 GUI 界面**，像个笨拙的机器人一样在屏幕上戳来戳去？

或者你想让 AI 帮你剪辑一段视频，它却只能给你写个教程，告诉你"亲，建议您手动打开 Premiere 然后点击这里哦"？

**说实话，这在以前要么得靠脆弱的 UI 自动化，要么得手写复杂的 API 封装。**

但现在，香港大学数据科学团队 HKUDS 开源了一个叫 **CLI-Anything** 的项目，只用了一行命令：

```bash
/cli-anything ./gimp
```

就让 GIMP 这个专业的图像编辑软件瞬间变成了 AI 智能体的"私家工具"。AI 可以直接用命令行控制它，**107 个测试全部通过**，效果和专业人士手动操作一模一样。

更夸张的是，这个项目在发布后的第二天就拿到了**634 颗 Star**，测试用例超过**1298 个**，覆盖了 GIMP、Blender、LibreOffice、OBS Studio 等 8 款专业软件。

**这不是 Demo，这是生产级代码。**

![CLI-Anything 演示动图](images/img_001_typing_demo.gif)

---

## 这是个啥？为什么值得关心？

**一句话定义**：CLI-Anything 是一个 Claude Code 插件，能把**任何有代码库的软件**自动改造成 AI 智能体友好的命令行工具。

**它解决了什么问题？**

现在的 AI 智能体有个致命弱点：**不会用真正的专业软件**。

你想让 AI 帮你做个海报，它要么给你推荐 Canva，要么用 Pillow 这种基础库"模拟"图像编辑——功能阉割到连图层都不支持。

**CLI-Anything 的思路很直接**：既然 AI 用不好 GUI，那就把 GUI 软件变成 CLI（命令行界面）啊！

**类比一下**：这就像给每个不会说中文的外国人配了个实时翻译——AI 说的是"命令语言"，专业软件说的是"图形界面"，CLI-Anything 就是那个翻译官。

![CLI-Anything 架构图](images/img_002_architecture.png)

---

## 核心原理：7 阶段全自动流水线

CLI-Anything 的核心是一个**7 阶段全自动流水线**。你只需要给它一个软件的源代码，它就能自动完成从分析到发布的全部工作。

**7 个阶段分别是**：

1. **🔍 分析 (Analyze)** — 扫描源代码，把 GUI 操作映射到 API
2. **📐 设计 (Design)** — 设计命令组、状态模型、输出格式
3. **🔨 实现 (Implement)** — 构建基于 Click 的 CLI，支持 REPL、JSON 输出、撤销/重做
4. **📋 规划测试 (Plan Tests)** — 创建 TEST.md，包含单元测试和端到端测试计划
5. **🧪 编写测试 (Write Tests)** — 实现全面的测试套件
6. **📝 文档 (Document)** — 更新 TEST.md 记录测试结果
7. **📦 发布 (Publish)** — 创建 `setup.py`，安装到系统 PATH

**这个过程有多自动化？**

看这个对比就知道了：

| 传统方式 | CLI-Anything |
|---------|-------------|
| 手写 API 封装（几周） | 一行命令（几分钟） |
| 脆弱 UI 自动化 | 稳定命令行调用 |
| 功能阉割版 Demo | 完整专业功能 |
| 每个软件单独适配 | 通用流水线自动处理 |

---

## 为什么 CLI 是智能体的"终极接口"？

这里有个反直觉的真相：

**大多数人以为 AI 智能体的核心是大模型，其实关键是接口。**

CLI-Anything 团队在 README 里写了 5 个理由，笔者容啰嗦一下：

### 1. 结构化且可组合

文本命令天然匹配 LLM 的输出格式，还能链式调用处理复杂工作流。

```bash
# 创建项目 → 添加图层 → 应用滤镜 → 导出
cli-anything-gimp project new --width 1920 --height 1080 -o poster.json
cli-anything-gimp --json layer add -n "Background" --type solid
cli-anything-gimp --json filter apply --name gaussian-blur --radius 5
cli-anything-gimp --json export render output.png
```

### 2. 轻量且通用

最小开销，跨所有系统工作，无需额外依赖。

### 3. 自描述

`--help` 标志提供自动文档，AI 可以自己发现能力。

### 4. 已验证的成功

Claude Code 每天通过 CLI 运行成千上万个真实工作流。

### 5. 智能体优先设计

结构化 JSON 输出消除了解析复杂度。

**不得不感叹一句：有时候最简单的方案，就是最优解。**

---

## 代码实战：用 CLI-Anything 控制 LibreOffice

闲话至此，直接上代码。

### 第 1 步：安装插件

```bash
# 添加 CLI-Anything 市场
/plugin marketplace add HKUDS/CLI-Anything

# 安装插件
/plugin install cli-anything
```

### 第 2 步：生成 LibreOffice 的 CLI

```bash
# 一行命令，自动生成 LibreOffice 的命令行接口
/cli-anything ./libreoffice
```

这行命令执行后，CLI-Anything 会自动完成前面说的 7 个阶段，最终生成一个名为 `cli-anything-libreoffice` 的命令行工具。

### 第 3 步：安装并使用

```bash
# 安装到系统 PATH
cd libreoffice/agent-harness && pip install -e .

# 创建一个新的 Writer 文档
cli-anything-libreoffice document new -o report.json --type writer

# 添加标题
cli-anything-libreoffice --project report.json writer add-heading -t "Q1 Report" --level 1

# 添加表格
cli-anything-libreoffice --project report.json writer add-table --rows 4 --cols 3

# 导出为 PDF
cli-anything-libreoffice --project report.json export render output.pdf -p pdf --overwrite
```

**⚠️ 坑**：这里注意 `--project` 参数必须指向之前创建的 JSON 项目文件，否则会报错。

### JSON 模式：智能体的"母语"

```bash
cli-anything-libreoffice --json document info --project report.json
```

输出：

```json
{
  "name": "Q1 Report",
  "type": "writer",
  "pages": 1,
  "elements": 2,
  "modified": true
}
```

**看到了吗？这就是智能体消费的"结构化数据"。**

---

## REPL 模式：交互式会话

CLI-Anything 生成的工具还支持**REPL 模式**（交互式命令行界面）：

```
$ cli-anything-blender
╔══════════════════════════════════════════╗
║       cli-anything-blender v1.0.0       ║
║     Blender CLI for AI Agents           ║
╚══════════════════════════════════════════╝

blender> scene new --name ProductShot
✓ Created scene: ProductShot

blender[ProductShot]> object add-mesh --type cube --location 0 0 1
✓ Added mesh: Cube at (0, 0, 1)

blender[ProductShot]*> render execute --output render.png --engine CYCLES
✓ Rendered: render.png (1920×1080, 2.3 MB) via blender --background

blender[ProductShot]> exit
Goodbye! 👋
```

**这个设计很妙**：REPL 模式保持了会话状态，AI 可以像真人一样"连续操作"，而不是每次都从头开始。

---

## 效果展示：8 款专业软件，1298 个测试全部通过

CLI-Anything 不是纸上谈兵。它已经通过了**1298 个测试用例**，覆盖了 8 款专业软件：

| 软件 | 领域 | CLI 命令 | 后端 | 测试数 |
|------|------|---------|------|--------|
| **🎨 GIMP** | 图像编辑 | `cli-anything-gimp` | Pillow + GEGL/Script-Fu | ✅ 107 |
| **🧊 Blender** | 3D 建模与渲染 | `cli-anything-blender` | bpy (Python scripting) | ✅ 208 |
| **✏️ Inkscape** | 矢量图形 | `cli-anything-inkscape` | 直接 SVG/XML 操作 | ✅ 202 |
| **🎵 Audacity** | 音频制作 | `cli-anything-audacity` | Python wave + sox | ✅ 161 |
| **📄 LibreOffice** | 办公套件 | `cli-anything-libreoffice` | ODF 生成 + 无头 LO | ✅ 158 |
| **📹 OBS Studio** | 直播录制 | `cli-anything-obs-studio` | JSON 场景 + obs-websocket | ✅ 153 |
| **🎞️ Kdenlive** | 视频编辑 | `cli-anything-kdenlive` | MLT XML + melt 渲染 | ✅ 155 |
| **🎬 Shotcut** | 视频编辑 | `cli-anything-shotcut` | 直接 MLT XML + melt | ✅ 154 |
| **总计** | | | | **✅ 1,298** |

**100% 通过率**——895 个单元测试 + 403 个端到端测试。

---

## 深层思考：为什么 CLI-Anything 是"降维打击"？

### 当前智能体使用软件的三种"笨办法"

1. **UI 自动化** —— 模拟鼠标点击和键盘输入，脆弱到截图一变就挂
2. **API 封装** —— 每个软件单独写封装，成本高到离谱
3. **重新实现** —— 用 Pillow 模拟 GIMP，功能阉割到只剩 10%

**CLI-Anything 的破局思路**：

> **我们不重建软件，我们重建接口。**

这句话是笔者的总结。你看它的核心设计原则：

### 1. 真实软件集成

CLI 生成有效的项目文件（ODF、MLT XML、SVG），然后交给真正的应用程序渲染。

**不是用 Pillow 替代 GIMP，而是生成 GIMP 能懂的项目文件，让 GIMP 自己渲染。**

### 2. 零妥协依赖

真正的软件是硬性要求——没有回退，没有优雅降级。

**测试会在后端缺失时失败（而不是跳过），确保功能真实性。**

### 3. 智能体原生设计

每个命令都内置 `--json` 标志，为机器消费提供结构化数据。

**智能体通过标准的 `--help` 和 `which` 命令发现能力。**

---

## 和竞品对比：CLI-Anything 的独特价值

根据笔者的调研，当前 AI CLI 智能体市场主要有这些玩家：

| 工具 | 提供商 | 核心能力 | 价格 |
|------|--------|---------|------|
| **Claude Code** | Anthropic | 规划优先工作流，MCP 集成 | $20-200/月 |
| **Gemini CLI** | Google | 100 万 token 上下文，免费层 | 免费 (1000 次/天) |
| **Aider** | 开源 | Git 集成，100+ 语言 | 免费 (自备 API) |
| **Cursor CLI** | Cursor | AI 优先编辑器 | 订阅制 |

**但这些都是"通用智能体"——CLI-Anything 做的是"软件改造"。**

| 维度 | 通用智能体 | CLI-Anything |
|------|-----------|-------------|
| **目标** | 直接帮用户写代码 | 把软件改造成智能体友好 |
| **能力边界** | 依赖模型知识 | 继承原软件 100% 功能 |
| **适配成本** | 每个软件单独学 | 通用流水线自动处理 |
| **可靠性** | 依赖模型准确性 | 确定性命令行行为 |

**笔者的判断**：CLI-Anything 不是竞品，是**互补层**。

Claude Code 负责"思考和规划"，CLI-Anything 负责"执行和落地"。

---

## 局限性坦诚：CLI-Anything 不是万能的

这里必须说实话：

### 1. 需要源代码

CLI-Anything 要求目标软件有**可访问的代码库**。

闭源软件？要么找开源替代品，要么等官方支持。

### 2. 硬性依赖

**真正的软件必须安装**。你想用 GIMP 的 CLI？先装 GIMP。

这不是优雅降级，这是设计原则。

### 3. 学习曲线

虽然 CLI 已经生成，但智能体仍需学习每个命令的语义。

**好在 `--help` 是通用的**，这比 GUI 自动化强太多。

### 4. 不适用于所有场景

需要视觉反馈的操作（如精细的图像修饰）仍然需要人工介入。

**CLI-Anything 解决的是"可控性"问题，不是"创造性"问题。**

---

## 跨领域思考：这暗合了什么道理？

**GAN 就像梅西和 C 罗——正因对手存在，才互相促进。**

CLI-Anything 和通用智能体的关系，何尝不是如此？

通用智能体负责"想"，CLI-Anything 负责"做"。

**想和做的分离，恰恰是专业分工的本质。**

不得不感叹一句：**大道至简。**

---

## 结语

CLI-Anything 确实是个很**聪明**的**工具**。

它没有试图重新发明轮子，而是给轮子装了个**标准接口**。

**数学才是硬道理**——有时候最简单的方案，就是最优解。

从技术趋势来看，CLI-Anything 继 Agent 里程碑之后又迎来了一次大的突破：**让 AI 从"看和说"走向"做和成"**。

如果你的场景是**改造现有软件**，笔者建议用 CLI-Anything；如果是**从零构建**，则通用智能体更合适。

希望读者能够有所收获。

**未来已来，只是分布得还不均匀。**

---

### 参考

- [CLI-Anything GitHub 仓库](https://github.com/HKUDS/CLI-Anything)
- [HARNESS.md 方法论文档](https://github.com/HKUDS/CLI-Anything/blob/main/cli-anything-plugin/HARNESS.md)
- [Patrick Hulce: AI Coding Agent Showdown](https://patrickhl.com/ai-agent-showdown)
- [Terminal-Bench Leaderboard](https://www.tbench.ai/leaderboard)

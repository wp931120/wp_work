# 一行描述就能生成你想要的声音——Qwen3-TTS 实战指南

> 📖 **本文解读内容来源**
>
> - **原始来源**：[Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)（阿里巴巴通义团队）
> - **来源类型**：GitHub 仓库 / 开源项目
> - **作者/团队**：Alibaba Qwen Team
> - **发布时间**：2026 年 3 月

你有没有遇到过这种场景：想给自己的视频配音，但自己的声音不够"有磁性"；或者想做一个 AI 语音助手，但现有的 TTS 系统要么声音僵硬，要么克隆效果差？

说实话，这在以前要么得花钱请配音演员，要么得忍受机器味十足的文字转语音。但现在不一样了——**阿里巴巴通义团队开源了 Qwen3-TTS**，一个大模型驱动的文本转语音系统，支持三种玩法：预设说话人、文字描述生成音色、声音克隆。

最让笔者兴奋的是它的 **Voice Design 模式**——你只需要用自然语言描述想要的音色，比如"说话带着一丝慌张但努力保持镇定的语气"，模型就能生成符合描述的声音。这在其他 TTS 系统里可不多见。

## 这是个啥？为什么值得关注？

所谓 **Qwen3-TTS**，其实就像一个"懂你心思的配音演员"——你告诉它想要什么风格的声音，它就能给你演出来。

传统 TTS 系统的问题在于：声音要么太机械，要么克隆效果差。Qwen3-TTS 用大语言模型来"理解"文本和语音之间的关系，生成出来的声音更自然、更有表现力。

它的核心架构是这样的：

<svg width="100%" viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
    </linearGradient>
  </defs>
  <!-- 输入层 -->
  <rect x="20" y="20" width="120" height="50" rx="8" fill="url(#grad1)" />
  <text x="80" y="50" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">文本输入</text>
  <rect x="20" y="90" width="120" height="50" rx="8" fill="url(#grad2)" />
  <text x="80" y="120" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">参考音频</text>
  <rect x="20" y="160" width="120" height="50" rx="8" fill="url(#grad3)" />
  <text x="80" y="190" text-anchor="middle" fill="#fff" font-size="13" font-family="system-ui, sans-serif">音色描述</text>
  <!-- 箭头 -->
  <line x1="140" y1="45" x2="200" y2="115" stroke="#667eea" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="140" y1="115" x2="200" y2="115" stroke="#f5576c" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="140" y1="185" x2="200" y2="115" stroke="#4facfe" stroke-width="2" marker-end="url(#arrow)" />
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#333" />
    </marker>
  </defs>
  <!-- 核心模块 -->
  <rect x="200" y="70" width="140" height="90" rx="10" fill="#2d3748" stroke="#4a5568" stroke-width="2" />
  <text x="270" y="105" text-anchor="middle" fill="#fff" font-size="14" font-family="system-ui, sans-serif">LLM Backbone</text>
  <text x="270" y="125" text-anchor="middle" fill="#a0aec0" font-size="11" font-family="system-ui, sans-serif">(Qwen 架构)</text>
  <!-- 箭头 -->
  <line x1="340" y1="115" x2="400" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow)" />
  <!-- 语音分词器 -->
  <rect x="400" y="70" width="140" height="90" rx="10" fill="#1a365d" stroke="#2b6cb0" stroke-width="2" />
  <text x="470" y="100" text-anchor="middle" fill="#fff" font-size="14" font-family="system-ui, sans-serif">Speech Tokenizer</text>
  <text x="470" y="120" text-anchor="middle" fill="#a0aec0" font-size="11" font-family="system-ui, sans-serif">(语音编解码器)</text>
  <text x="470" y="140" text-anchor="middle" fill="#a0aec0" font-size="11" font-family="system-ui, sans-serif">12Hz / 25Hz</text>
  <!-- 箭头 -->
  <line x1="540" y1="115" x2="600" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrow)" />
  <!-- 输出 -->
  <rect x="600" y="70" width="80" height="90" rx="10" fill="#276749" stroke="#38a169" stroke-width="2" />
  <text x="640" y="120" text-anchor="middle" fill="#fff" font-size="14" font-family="system-ui, sans-serif">音频输出</text>
</svg>

核心组件有三个：

1. **Speech Tokenizer（语音分词器）**：把音频"切"成离散的 token，就像把文章切分成词一样。支持 12Hz 和 25Hz 两种采样率。
2. **LLM Backbone（语言模型主干）**：基于 Qwen 架构，负责理解文本内容和语音风格，预测下一个语音 token。
3. **Speaker Encoder（说话人编码器）**：提取参考音频中的说话人特征，用于声音克隆。

## 三种玩法，各有千秋

Qwen3-TTS 提供三种模型类型，对应不同的使用场景：

| 模型类型 | 功能 | 适用场景 |
|---------|------|---------|
| **CustomVoice** | 预设说话人合成 | 快速使用内置音色 |
| **VoiceDesign** | 文字描述生成音色 | 创意配音、个性化语音 |
| **Base** | 声音克隆 | 复刻特定声音 |

### CustomVoice：开箱即用的预设音色

如果你只是想快速生成语音，不想折腾，选 CustomVoice 就对了。它内置了多个预设说话人，你只需要指定说话人名字，就能生成对应风格的声音。

```python
from qwen_tts import Qwen3TTSModel

# 加载模型
tts = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0",
    torch_dtype=torch.bfloat16
)

# 生成语音
wavs, sr = tts.generate_custom_voice(
    text="你好，我是 Qwen3-TTS，很高兴认识你！",
    speaker="Vivian",  # 内置说话人
    language="zh"
)
```

### VoiceDesign：用文字"画"出你想要的声音

这是笔者最喜欢的功能。你只需要用自然语言描述想要的音色，模型就能生成符合描述的声音。

```python
tts = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0"
)

wavs, sr = tts.generate_voice_design(
    text="天哪，这不可能！我明明把钥匙放在这里的！",
    instruct="用难以置信的语气说话，但声音里透着一丝开始蔓延的慌张。",
    language="zh"
)
```

这种"文字描述 → 音色生成"的能力，在其他 TTS 系统里确实少见。它让非专业人士也能精准控制语音风格，而不需要调整一堆复杂的参数。

### Base：几秒钟克隆任何声音

声音克隆是很多 TTS 系统的标配，但效果参差不齐。Qwen3-TTS 提供了两种克隆模式：

1. **x_vector_only_mode**：只用说话人嵌入，克隆速度快但细节保留较少。
2. **ICL 模式（In-Context Learning）**：结合参考音频和参考文本，克隆效果更精细。

```python
tts = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0"
)

# 创建克隆提示
prompt = tts.create_voice_clone_prompt(
    ref_audio="reference.wav",  # 参考音频
    ref_text="这是参考音频的文本内容",  # 参考音频的转录
    x_vector_only_mode=False  # 使用 ICL 模式，效果更好
)

# 保存提示，后续可复用
import torch
torch.save(prompt, "voice_prompt.pt")

# 用克隆的声音生成语音
wavs, sr = tts.generate_voice_clone(
    text="这是用克隆声音说的新内容",
    voice_clone_prompt=prompt,
    language="zh"
)
```

## 启动 Gradio Demo，边玩边调

如果你想更直观地体验这些功能，可以直接启动官方提供的 Gradio Demo：

```bash
# 安装依赖
pip install qwen-tts

# 启动 Demo
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign --port 8000
```

Demo 启动后，打开浏览器访问 `http://localhost:8000`，你会看到一个简洁的 Web 界面：

- **CustomVoice Tab**：选择预设说话人，输入文本，点击生成。
- **VoiceDesign Tab**：输入文本和音色描述，体验"文字画音"的神奇。
- **Base Tab**：上传参考音频，克隆声音并生成新语音。

Demo 的核心代码在 `qwen_tts/cli/demo.py` 里，约 635 行，结构清晰。如果你想定制界面，可以直接修改这个文件。

## 核心原理：大模型如何"学会"说话？

你可能会想——大语言模型不是处理文本的吗？怎么还能生成语音？

好问题。这涉及到一个关键概念：**语音 tokenization（语音分词）**。

传统 TTS 系统通常采用"文本 → 声学特征 → 波形"的流水线。而 Qwen3-TTS 采用了一种更"大模型原生"的思路：

1. 把语音"翻译"成离散的 token 序列（就像把句子翻译成词元序列）。
2. 用语言模型预测下一个语音 token。
3. 把 token 序列"解码"回音频波形。

这就像是让大模型"学会"了语音的"词汇表"，然后用预测文本的方式预测语音。

<svg width="100%" viewBox="0 0 600 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#667eea" />
      <stop offset="100%" style="stop-color:#764ba2" />
    </linearGradient>
  </defs>
  <!-- 步骤 -->
  <rect x="20" y="60" width="100" height="60" rx="8" fill="url(#g1)" />
  <text x="70" y="95" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">音频输入</text>
  <line x1="120" y1="90" x2="160" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="160" y="60" width="100" height="60" rx="8" fill="#2d3748" />
  <text x="210" y="85" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Speech</text>
  <text x="210" y="102" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Tokenizer</text>
  <line x1="260" y1="90" x2="300" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="300" y="60" width="80" height="60" rx="8" fill="#553c9a" />
  <text x="340" y="90" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">Token</text>
  <text x="340" y="105" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">序列</text>
  <line x1="380" y1="90" x2="420" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="420" y="60" width="80" height="60" rx="8" fill="#2d3748" />
  <text x="460" y="90" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">LLM</text>
  <line x1="500" y1="90" x2="540" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrow)" />
  <rect x="540" y="60" width="50" height="60" rx="8" fill="url(#g1)" />
  <text x="565" y="95" text-anchor="middle" fill="#fff" font-size="12" font-family="system-ui, sans-serif">语音</text>
  <!-- 标注 -->
  <text x="340" y="150" text-anchor="middle" fill="#718096" font-size="11" font-family="system-ui, sans-serif">离散 token 就像语音的"词元"</text>
</svg>

这种设计的好处是：大模型的"理解能力"可以直接迁移到语音领域。比如你用 VoiceDesign 描述"带着一丝慌张但努力保持镇定"，模型就能理解这种复杂的情感表达，并体现在生成的语音中。

## 踩坑指南：使用时需要注意什么？

笔者在试用过程中也踩了一些坑，分享给大家：

### 1. 模型类型要选对

三种模型类型对应不同的 API：

- `generate_custom_voice()` → CustomVoice 模型
- `generate_voice_design()` → VoiceDesign 模型
- `generate_voice_clone()` → Base 模型

用错了会报错，提示 "does not support xxx"。

### 2. ICL 模式需要参考文本

如果使用 `x_vector_only_mode=False`（ICL 模式），必须提供 `ref_text`，即参考音频的转录文本。没有的话会报错。

### 3. 采样率要匹配

Qwen3-TTS 有 12Hz 和 25Hz 两种 tokenizer 版本。下载模型时注意选择对应版本，混用会出问题。

### 4. 显存占用

1.7B 模型在 bfloat16 精度下约需 4GB 显存。如果显存不够，可以尝试：
- 使用 `--dtype float16`
- 使用 `--device cpu`（速度会慢很多）

## 结语：语音生成的"大模型时代"来了

Qwen3-TTS 确实是个很有意思的项目。它把大语言模型的"理解能力"和语音生成结合在一起，让 TTS 系统从"机械朗读"进化到了"有感情的配音"。

Voice Design 模式尤其让笔者兴奋——用自然语言描述音色，这在以前是想都不敢想的事。不得不感叹一句：大模型的泛化能力，正在让越来越多的"不可能"变成"理所当然"。

当然，Qwen3-TTS 也有局限性。比如声音克隆的精度还有提升空间，长文本生成的稳定性也需要进一步优化。但作为开源项目，它已经为社区提供了一个非常好的起点。

如果你对语音合成感兴趣，或者想给自己的项目加上"有灵魂的配音"，不妨试试 Qwen3-TTS。希望读者能够有所收获，玩得开心！

### 参考

- [Qwen3-TTS GitHub 仓库](https://github.com/QwenLM/Qwen3-TTS)
- [Qwen3-TTS ModelScope 模型库](https://modelscope.cn/models/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign)
- [HuggingFace Transformers 文档](https://huggingface.co/docs/transformers/)
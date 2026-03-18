#!/usr/bin/env python3
"""生成 Agent Skill 设计模式文章的配图"""

import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_patterns_overview():
    """生成五种设计模式概览图"""
    svg = '''<svg width="100%" viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
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
    <linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#43e97b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38f9d7;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#fa709a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#fee140;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-opacity="0.15"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="800" height="500" fill="#0f0f23"/>

  <!-- 标题 -->
  <text x="400" y="45" text-anchor="middle" fill="#fff" font-size="24" font-weight="bold" font-family="system-ui, -apple-system, sans-serif">Agent Skill 五种设计模式</text>

  <!-- Pattern 1: Tool Wrapper -->
  <g transform="translate(80, 90)">
    <rect width="120" height="70" rx="12" fill="url(#grad1)" filter="url(#shadow)"/>
    <text x="60" y="35" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">Tool Wrapper</text>
    <text x="60" y="55" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11" font-family="system-ui, sans-serif">即时专家</text>
  </g>

  <!-- Pattern 2: Generator -->
  <g transform="translate(240, 90)">
    <rect width="120" height="70" rx="12" fill="url(#grad2)" filter="url(#shadow)"/>
    <text x="60" y="35" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">Generator</text>
    <text x="60" y="55" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11" font-family="system-ui, sans-serif">填空模板</text>
  </g>

  <!-- Pattern 3: Reviewer -->
  <g transform="translate(400, 90)">
    <rect width="120" height="70" rx="12" fill="url(#grad3)" filter="url(#shadow)"/>
    <text x="60" y="35" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">Reviewer</text>
    <text x="60" y="55" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11" font-family="system-ui, sans-serif">清单打分</text>
  </g>

  <!-- Pattern 4: Inversion -->
  <g transform="translate(560, 90)">
    <rect width="120" height="70" rx="12" fill="url(#grad4)" filter="url(#shadow)"/>
    <text x="60" y="35" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">Inversion</text>
    <text x="60" y="55" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11" font-family="system-ui, sans-serif">先问后做</text>
  </g>

  <!-- Pattern 5: Pipeline -->
  <g transform="translate(340, 200)">
    <rect width="120" height="70" rx="12" fill="url(#grad5)" filter="url(#shadow)"/>
    <text x="60" y="35" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold" font-family="system-ui, sans-serif">Pipeline</text>
    <text x="60" y="55" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-size="11" font-family="system-ui, sans-serif">严格流水线</text>
  </g>

  <!-- 连接线 -->
  <path d="M140 160 Q140 180 400 200" stroke="#667eea" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M300 160 Q300 180 400 200" stroke="#f5576c" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M460 160 Q460 180 400 200" stroke="#00f2fe" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M620 160 Q620 180 400 200" stroke="#38f9d7" stroke-width="2" fill="none" opacity="0.5"/>

  <!-- 底部说明区域 -->
  <rect x="60" y="300" width="680" height="170" rx="12" fill="#1a1a2e" opacity="0.8"/>

  <!-- 左侧：场景 -->
  <text x="100" y="335" fill="#9ca3af" font-size="12" font-family="system-ui, sans-serif">适用场景</text>
  <text x="100" y="360" fill="#fff" font-size="11" font-family="system-ui, sans-serif">• Tool Wrapper → Agent 需要精通某个库</text>
  <text x="100" y="380" fill="#fff" font-size="11" font-family="system-ui, sans-serif">• Generator → 输出固定格式的文档</text>
  <text x="100" y="400" fill="#fff" font-size="11" font-family="system-ui, sans-serif">• Reviewer → 代码审查、质量检查</text>

  <!-- 右侧：场景 -->
  <text x="450" y="335" fill="#9ca3af" font-size="12" font-family="system-ui, sans-serif">组合建议</text>
  <text x="450" y="360" fill="#fff" font-size="11" font-family="system-ui, sans-serif">• Pipeline + Reviewer → 自检流水线</text>
  <text x="450" y="380" fill="#fff" font-size="11" font-family="system-ui, sans-serif">• Generator + Inversion → 先采集再生成</text>
  <text x="450" y="400" fill="#fff" font-size="11" font-family="system-ui, sans-serif">• Tool Wrapper + Pipeline → 专家级流水线</text>

  <!-- 底部标注 -->
  <text x="400" y="450" text-anchor="middle" fill="#6b7280" font-size="10" font-family="system-ui, sans-serif">基于 ADK SkillToolset 渐进式上下文加载，组合使用不炸 Token</text>
</svg>'''

    with open(f"{OUTPUT_DIR}/patterns_overview.svg", "w") as f:
        f.write(svg)
    print(f"Generated: {OUTPUT_DIR}/patterns_overview.svg")


def generate_decision_tree():
    """生成模式选择决策树"""
    svg = '''<svg width="100%" viewBox="0 0 700 520" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="nodeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="yesGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#22c55e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#16a34a;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="noGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f59e0b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#d97706;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-opacity="0.2"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="700" height="520" fill="#0f0f23"/>

  <!-- 标题 -->
  <text x="350" y="35" text-anchor="middle" fill="#fff" font-size="18" font-weight="bold" font-family="system-ui, sans-serif">如何选择设计模式？</text>

  <!-- 起点：需求是什么？ -->
  <rect x="275" y="55" width="150" height="45" rx="8" fill="url(#nodeGrad)" filter="url(#shadow)"/>
  <text x="350" y="82" text-anchor="middle" fill="#fff" font-size="12" font-weight="bold" font-family="system-ui, sans-serif">需求是什么？</text>

  <!-- 第一层分支 -->
  <!-- 左：让 Agent 懂某个库 -->
  <line x1="275" y1="77" x2="130" y2="140" stroke="#6366f1" stroke-width="2"/>
  <rect x="55" y="130" width="150" height="45" rx="8" fill="#1a1a2e" stroke="#6366f1" stroke-width="2"/>
  <text x="130" y="157" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">让 Agent 精通某个库？</text>

  <!-- 中：输出固定格式 -->
  <line x1="350" y1="100" x2="350" y2="130" stroke="#6366f1" stroke-width="2"/>
  <rect x="275" y="130" width="150" height="45" rx="8" fill="#1a1a2e" stroke="#6366f1" stroke-width="2"/>
  <text x="350" y="157" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">输出固定格式文档？</text>

  <!-- 右：检查评审 -->
  <line x1="425" y1="77" x2="570" y2="140" stroke="#6366f1" stroke-width="2"/>
  <rect x="495" y="130" width="150" height="45" rx="8" fill="#1a1a2e" stroke="#6366f1" stroke-width="2"/>
  <text x="570" y="157" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">检查、评审代码？</text>

  <!-- 结果节点：Tool Wrapper -->
  <line x1="130" y1="175" x2="130" y2="210" stroke="#22c55e" stroke-width="2"/>
  <text x="105" y="195" fill="#22c55e" font-size="10" font-family="system-ui, sans-serif">是</text>
  <rect x="65" y="210" width="130" height="40" rx="8" fill="url(#yesGrad)" filter="url(#shadow)"/>
  <text x="130" y="235" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">Tool Wrapper</text>

  <!-- 结果节点：Generator -->
  <line x1="350" y1="175" x2="350" y2="210" stroke="#22c55e" stroke-width="2"/>
  <text x="325" y="195" fill="#22c55e" font-size="10" font-family="system-ui, sans-serif">是</text>
  <rect x="285" y="210" width="130" height="40" rx="8" fill="url(#yesGrad)" filter="url(#shadow)"/>
  <text x="350" y="235" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">Generator</text>

  <!-- 结果节点：Reviewer -->
  <line x1="570" y1="175" x2="570" y2="210" stroke="#22c55e" stroke-width="2"/>
  <text x="545" y="195" fill="#22c55e" font-size="10" font-family="system-ui, sans-serif">是</text>
  <rect x="505" y="210" width="130" height="40" rx="8" fill="url(#yesGrad)" filter="url(#shadow)"/>
  <text x="570" y="235" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">Reviewer</text>

  <!-- 第二层：Inversion / Pipeline 判断 -->
  <line x1="350" y1="250" x2="350" y2="290" stroke="#6366f1" stroke-width="2"/>
  <rect x="250" y="290" width="200" height="45" rx="8" fill="#1a1a2e" stroke="#6366f1" stroke-width="2"/>
  <text x="350" y="317" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">需求复杂、容易理解错？</text>

  <!-- Inversion -->
  <line x1="250" y1="312" x2="150" y2="370" stroke="#22c55e" stroke-width="2"/>
  <text x="175" y="340" fill="#22c55e" font-size="10" font-family="system-ui, sans-serif">是</text>
  <rect x="85" y="365" width="130" height="40" rx="8" fill="url(#yesGrad)" filter="url(#shadow)"/>
  <text x="150" y="390" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">Inversion</text>

  <!-- Pipeline 判断 -->
  <line x1="450" y1="312" x2="550" y2="370" stroke="#f59e0b" stroke-width="2"/>
  <text x="475" y="340" fill="#f59e0b" font-size="10" font-family="system-ui, sans-serif">否</text>
  <rect x="450" y="365" width="200" height="45" rx="8" fill="#1a1a2e" stroke="#f59e0b" stroke-width="2"/>
  <text x="550" y="392" text-anchor="middle" fill="#fff" font-size="11" font-family="system-ui, sans-serif">任务多步骤、不能跳步？</text>

  <!-- Pipeline -->
  <line x1="550" y1="410" x2="550" y2="445" stroke="#22c55e" stroke-width="2"/>
  <text x="525" y="430" fill="#22c55e" font-size="10" font-family="system-ui, sans-serif">是</text>
  <rect x="485" y="445" width="130" height="40" rx="8" fill="url(#yesGrad)" filter="url(#shadow)"/>
  <text x="550" y="470" text-anchor="middle" fill="#fff" font-size="13" font-weight="bold" font-family="system-ui, sans-serif">Pipeline</text>

  <!-- 说明 -->
  <text x="350" y="505" text-anchor="middle" fill="#6b7280" font-size="10" font-family="system-ui, sans-serif">绿色 = 推荐模式 | 实际场景中可组合使用多种模式</text>
</svg>'''

    with open(f"{OUTPUT_DIR}/decision_tree.svg", "w") as f:
        f.write(svg)
    print(f"Generated: {OUTPUT_DIR}/decision_tree.svg")


if __name__ == "__main__":
    generate_patterns_overview()
    generate_decision_tree()
    print("All SVG images generated!")
#!/usr/bin/env python3
"""生成文章配图 - SVG 版本"""

import os

output_dir = "/Users/wp931120/lobsterai/project/wp_work/20260315_Learn_Claude_Code/images"
os.makedirs(output_dir, exist_ok=True)

def generate_agent_loop():
    """Agent 循环概念图"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f0f23;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a1a3e;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00d9ff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7b2cbf;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#00d9ff"/>
    </marker>
  </defs>

  <!-- 背景 -->
  <rect width="800" height="600" fill="url(#bgGrad)"/>

  <!-- 标题 -->
  <text x="400" y="50" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="32" font-weight="bold" fill="#00d9ff">Agent Loop</text>
  <text x="400" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#6c757d">模型就是智能体，给它工具，然后让开</text>

  <!-- 中心 LLM -->
  <circle cx="400" cy="300" r="70" fill="none" stroke="url(#accentGrad)" stroke-width="3" filter="url(#glow)"/>
  <text x="400" y="290" text-anchor="middle" font-family="monospace" font-size="28" font-weight="bold" fill="#ffffff">LLM</text>
  <text x="400" y="320" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#6c757d">大模型</text>

  <!-- 节点位置 -->
  <!-- 上: messages -->
  <rect x="320" y="100" width="160" height="60" rx="8" fill="#1a1a3e" stroke="#7b2cbf" stroke-width="2"/>
  <text x="400" y="125" text-anchor="middle" font-family="monospace" font-size="14" fill="#ffffff">messages[]</text>
  <text x="400" y="145" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#6c757d">消息队列</text>

  <!-- 右: tool_use -->
  <rect x="580" y="270" width="140" height="60" rx="8" fill="#1a1a3e" stroke="#00d9ff" stroke-width="2"/>
  <text x="650" y="295" text-anchor="middle" font-family="monospace" font-size="14" fill="#ffffff">tool_use</text>
  <text x="650" y="315" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#6c757d">工具调用</text>

  <!-- 下: tool_result -->
  <rect x="320" y="440" width="160" height="60" rx="8" fill="#1a1a3e" stroke="#7b2cbf" stroke-width="2"/>
  <text x="400" y="465" text-anchor="middle" font-family="monospace" font-size="14" fill="#ffffff">tool_result</text>
  <text x="400" y="485" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#6c757d">工具结果</text>

  <!-- 左: response -->
  <rect x="80" y="270" width="140" height="60" rx="8" fill="#1a1a3e" stroke="#00d9ff" stroke-width="2"/>
  <text x="150" y="295" text-anchor="middle" font-family="monospace" font-size="14" fill="#ffffff">response</text>
  <text x="150" y="315" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#6c757d">最终响应</text>

  <!-- 连接箭头 -->
  <!-- messages -> LLM -->
  <path d="M400 160 L400 228" stroke="#00d9ff" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>

  <!-- LLM -> tool_use (右上曲线) -->
  <path d="M470 280 Q520 250, 580 290" stroke="#00d9ff" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="530" y="250" font-family="system-ui, sans-serif" font-size="11" fill="#00d9ff">stop_reason</text>
  <text x="530" y="265" font-family="monospace" font-size="10" fill="#6c757d">== "tool_use"</text>

  <!-- tool_use -> tool_result -->
  <path d="M650 330 Q650 390, 480 450" stroke="#7b2cbf" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="600" y="400" font-family="system-ui, sans-serif" font-size="11" fill="#7b2cbf">执行工具</text>

  <!-- tool_result -> messages -->
  <path d="M320 470 Q200 470, 200 350, 200 200, 320 130" stroke="#7b2cbf" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="180" y="300" font-family="system-ui, sans-serif" font-size="11" fill="#7b2cbf">追加结果</text>

  <!-- LLM -> response -->
  <path d="M330 300 L222 300" stroke="#00d9ff" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="275" y="290" font-family="system-ui, sans-serif" font-size="11" fill="#00d9ff">返回</text>

  <!-- 循环标注 -->
  <text x="400" y="550" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" fill="#6c757d">while True: 一个循环 + 工具 = 智能体</text>
</svg>'''

    with open(os.path.join(output_dir, "agent_loop.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("生成: agent_loop.svg")


def generate_evolution_stairs():
    """12 节课进化阶梯图"""

    stages = [
        ("s01", "循环", "One Loop"),
        ("s02", "工具", "Handler"),
        ("s03", "计划", "TodoWrite"),
        ("s04", "子智能体", "Subagent"),
        ("s05", "技能", "Skills"),
        ("s06", "压缩", "Compact"),
        ("s07", "持久化", "Persist"),
        ("s08", "后台", "Background"),
        ("s09", "团队", "Team"),
        ("s10", "协议", "Protocol"),
        ("s11", "自治", "Autonomy"),
        ("s12", "隔离", "Worktree"),
    ]

    # 生成台阶
    stairs_svg = ""
    for i, (code, name, desc) in enumerate(stages):
        x = 50 + i * 95
        y = 450 - i * 30
        width = 85
        height = 50

        # 渐变色
        ratio = i / 11
        r = int(0 + ratio * 123)
        g = int(217 - ratio * 100)
        b = int(255 - ratio * 30)
        color = f"#{r:02x}{g:02x}{b:02x}"

        stairs_svg += f'''
    <g transform="translate({x}, {y})">
      <rect width="{width}" height="{height}" rx="6" fill="{color}" opacity="0.9"/>
      <text x="{width//2}" y="18" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold" fill="#0f0f23">{code}</text>
      <text x="{width//2}" y="35" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#0f0f23">{name}</text>
    </g>'''

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="600" viewBox="0 0 1200 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f0f23;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a1a3e;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00d9ff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7b2cbf;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="1200" height="600" fill="url(#bgGrad)"/>

  <!-- 标题 -->
  <text x="600" y="50" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="36" font-weight="bold" fill="url(#titleGrad)">12 节课进化之路</text>
  <text x="600" y="85" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" fill="#6c757d">从"人工智障"到"靠谱队友"</text>

  <!-- 台阶 -->
  {stairs_svg}

  <!-- 阶段标注 -->
  <g transform="translate(80, 100)">
    <rect width="220" height="70" rx="8" fill="none" stroke="#00d9ff" stroke-width="1" stroke-dasharray="4,2"/>
    <text x="110" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#00d9ff">第一阶段</text>
    <text x="110" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#ffffff">循环与工具</text>
    <text x="110" y="60" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#6c757d">一个循环 + Bash = Agent</text>
  </g>

  <g transform="translate(360, 100)">
    <rect width="340" height="70" rx="8" fill="none" stroke="#7b2cbf" stroke-width="1" stroke-dasharray="4,2"/>
    <text x="170" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#7b2cbf">第二阶段</text>
    <text x="170" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#ffffff">规划与知识</text>
    <text x="170" y="60" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#6c757d">TodoWrite / Subagent / Skills / Compact</text>
  </g>

  <g transform="translate(750, 100)">
    <rect width="180" height="70" rx="8" fill="none" stroke="#00d9ff" stroke-width="1" stroke-dasharray="4,2"/>
    <text x="90" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#00d9ff">第三阶段</text>
    <text x="90" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#ffffff">持久化</text>
    <text x="90" y="60" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#6c757d">任务系统 + 后台任务</text>
  </g>

  <g transform="translate(960, 100)">
    <rect width="200" height="70" rx="8" fill="none" stroke="#7b2cbf" stroke-width="1" stroke-dasharray="4,2"/>
    <text x="100" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#7b2cbf">第四阶段</text>
    <text x="100" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#ffffff">团队协作</text>
    <text x="100" y="60" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#6c757d">多 Agent 协同工作</text>
  </g>

  <!-- 箭头指向 -->
  <path d="M1150 480 L1180 480 L1180 135 L1100 135" stroke="#6c757d" stroke-width="1.5" fill="none" stroke-dasharray="4,2"/>
  <circle cx="1150" cy="480" r="3" fill="#6c757d"/>

  <!-- 底部说明 -->
  <text x="600" y="560" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" fill="#6c757d">每节课只加一个机制，像搭积木一样</text>
</svg>'''

    with open(os.path.join(output_dir, "evolution_stairs.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("生成: evolution_stairs.svg")


def generate_agent_team():
    """多 Agent 协作图"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="550" viewBox="0 0 800 550" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f0f23;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a1a3e;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00d9ff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7b2cbf;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#6c757d"/>
    </marker>
    <marker id="arrowAccent" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#00d9ff"/>
    </marker>
  </defs>

  <!-- 背景 -->
  <rect width="800" height="550" fill="url(#bgGrad)"/>

  <!-- 标题 -->
  <text x="400" y="40" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="28" font-weight="bold" fill="url(#accentGrad)">多 Agent 协作</text>
  <text x="400" y="65" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" fill="#6c757d">任务太大一个人干不完，要能分给队友</text>

  <!-- 主 Agent -->
  <g transform="translate(400, 140)">
    <rect x="-90" y="-45" width="180" height="90" rx="12" fill="#1a1a3e" stroke="#00d9ff" stroke-width="2" filter="url(#glow)"/>
    <text x="0" y="-10" text-anchor="middle" font-family="system-ui, sans-serif" font-size="18" font-weight="bold" fill="#00d9ff">主 Agent</text>
    <text x="0" y="15" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#ffffff">项目经理</text>
    <text x="0" y="32" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#6c757d">协调 / 分配 / 监控</text>
  </g>

  <!-- 任务板 -->
  <g transform="translate(400, 280)">
    <rect x="-120" y="-35" width="240" height="70" rx="8" fill="#1a1a3e" stroke="#7b2cbf" stroke-width="2"/>
    <text x="0" y="-8" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#7b2cbf">任务板</text>
    <text x="0" y="15" text-anchor="middle" font-family="monospace" font-size="11" fill="#ffffff">Task Graph (JSONL)</text>
    <text x="0" y="30" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#6c757d">持久化 · 可依赖</text>
  </g>

  <!-- 主 Agent -> 任务板 -->
  <line x1="400" y1="185" x2="400" y2="243" stroke="#00d9ff" stroke-width="2" marker-end="url(#arrowAccent)"/>

  <!-- 子 Agent 们 -->
  <!-- 前端 Agent -->
  <g transform="translate(100, 430)">
    <rect x="-70" y="-40" width="140" height="80" rx="10" fill="#1a1a3e" stroke="#00d9ff" stroke-width="1.5"/>
    <text x="0" y="-12" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#00d9ff">前端 Agent</text>
    <text x="0" y="8" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">React / Vue</text>
    <text x="0" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#6c757d">独立 worktree</text>
  </g>
  <line x1="100" y1="390" x2="340" y2="315" stroke="#6c757d" stroke-width="1" stroke-dasharray="4,2" marker-end="url(#arrow)"/>

  <!-- 后端 Agent -->
  <g transform="translate(300, 450)">
    <rect x="-70" y="-40" width="140" height="80" rx="10" fill="#1a1a3e" stroke="#7b2cbf" stroke-width="1.5"/>
    <text x="0" y="-12" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#7b2cbf">后端 Agent</text>
    <text x="0" y="8" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">API / 数据库</text>
    <text x="0" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#6c757d">独立 worktree</text>
  </g>
  <line x1="300" y1="410" x2="380" y2="317" stroke="#6c757d" stroke-width="1" stroke-dasharray="4,2" marker-end="url(#arrow)"/>

  <!-- 测试 Agent -->
  <g transform="translate(500, 450)">
    <rect x="-70" y="-40" width="140" height="80" rx="10" fill="#1a1a3e" stroke="#00d9ff" stroke-width="1.5"/>
    <text x="0" y="-12" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#00d9ff">测试 Agent</text>
    <text x="0" y="8" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">单元 / 集成</text>
    <text x="0" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#6c757d">独立 worktree</text>
  </g>
  <line x1="500" y1="410" x2="420" y2="317" stroke="#6c757d" stroke-width="1" stroke-dasharray="4,2" marker-end="url(#arrow)"/>

  <!-- 部署 Agent -->
  <g transform="translate(700, 430)">
    <rect x="-70" y="-40" width="140" height="80" rx="10" fill="#1a1a3e" stroke="#7b2cbf" stroke-width="1.5"/>
    <text x="0" y="-12" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#7b2cbf">部署 Agent</text>
    <text x="0" y="8" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#ffffff">CI/CD / K8s</text>
    <text x="0" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#6c757d">独立 worktree</text>
  </g>
  <line x1="700" y1="390" x2="460" y2="315" stroke="#6c757d" stroke-width="1" stroke-dasharray="4,2" marker-end="url(#arrow)"/>

  <!-- 说明文字 -->
  <text x="400" y="510" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#6c757d">队友自己看任务板，有活就认领 → 从"被动执行"到"主动工作"</text>
</svg>'''

    with open(os.path.join(output_dir, "agent_team.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("生成: agent_team.svg")


if __name__ == "__main__":
    print("开始生成 SVG 配图...")
    generate_agent_loop()
    generate_evolution_stairs()
    generate_agent_team()
    print("配图生成完成!")
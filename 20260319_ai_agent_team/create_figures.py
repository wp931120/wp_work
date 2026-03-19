#!/usr/bin/env python3
"""
Generate SVG figures for AI Agent Team article
"""

import os

# Figure 1: Chat vs Agent comparison
fig1_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="400" viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a1628"/>
      <stop offset="100%" style="stop-color:#1a2744"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#3b82f6"/>
      <stop offset="100%" style="stop-color:#60a5fa"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#10b981"/>
      <stop offset="100%" style="stop-color:#34d399"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="900" height="400" fill="url(#bgGrad)"/>

  <!-- Left side: Chat (ping-pong) -->
  <g transform="translate(225, 200)">
    <!-- User icon -->
    <circle cx="-140" cy="0" r="28" fill="#f59e0b" opacity="0.9"/>
    <text x="-140" y="6" text-anchor="middle" fill="#0a1628" font-family="system-ui, sans-serif" font-size="24" font-weight="700">U</text>
    <text x="-140" y="55" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" font-weight="500">USER</text>

    <!-- AI icon -->
    <circle cx="140" cy="0" r="28" fill="#3b82f6" opacity="0.9"/>
    <text x="140" y="6" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="24" font-weight="700">AI</text>
    <text x="140" y="55" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" font-weight="500">AI</text>

    <!-- Ping-pong arrows -->
    <path d="M-105 0 L-60 -20 L-60 -8 L105 -8 L105 8 L-60 8 L-60 20 Z" fill="#f59e0b" opacity="0.6"/>
    <path d="M105 0 L60 20 L60 8 L-105 8 L-105 -8 L60 -8 L60 -20 Z" fill="#3b82f6" opacity="0.6"/>

    <!-- Labels on arrows -->
    <text x="0" y="-25" text-anchor="middle" fill="#fcd34d" font-family="system-ui, sans-serif" font-size="10" font-weight="500">Question</text>
    <text x="0" y="35" text-anchor="middle" fill="#93c5fd" font-family="system-ui, sans-serif" font-size="10" font-weight="500">Answer</text>

    <!-- Title -->
    <text x="0" y="-100" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="16" font-weight="600">Chat 模式</text>
    <text x="0" y="-78" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">你问它答，像打乒乓球</text>

    <!-- Result box -->
    <rect x="-50" y="75" width="100" height="28" rx="4" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,2"/>
    <text x="0" y="93" text-anchor="middle" fill="#ef4444" font-family="system-ui, sans-serif" font-size="10">你自己做事</text>
  </g>

  <!-- Divider -->
  <line x1="450" y1="60" x2="450" y2="340" stroke="#334155" stroke-width="1" stroke-dasharray="8,4"/>

  <!-- Right side: Agent (goal to result) -->
  <g transform="translate(675, 200)">
    <!-- Goal input -->
    <rect x="-160" y="-25" width="70" height="50" rx="8" fill="#f59e0b" opacity="0.9"/>
    <text x="-125" y="5" text-anchor="middle" fill="#0a1628" font-family="system-ui, sans-serif" font-size="12" font-weight="700">Goal</text>

    <!-- Arrow 1 -->
    <path d="M-85 0 L-55 0" stroke="#60a5fa" stroke-width="3" marker-end="url(#arrow)"/>

    <!-- Agent brain -->
    <circle cx="0" cy="0" r="45" fill="url(#blueGrad)" filter="url(#glow)"/>
    <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="11" font-weight="600">Observe</text>
    <text x="0" y="6" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="11" font-weight="600">Think</text>
    <text x="0" y="20" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="11" font-weight="600">Act</text>

    <!-- Circular arrows inside -->
    <path d="M-20 -5 A25 25 0 1 1 -20 5" fill="none" stroke="#fff" stroke-width="1.5" opacity="0.5"/>

    <!-- Arrow 2 -->
    <path d="M50 0 L80 0" stroke="#34d399" stroke-width="3"/>

    <!-- Result output -->
    <rect x="85" y="-25" width="70" height="50" rx="8" fill="url(#greenGrad)"/>
    <text x="120" y="5" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="12" font-weight="700">Result</text>

    <!-- Title -->
    <text x="0" y="-100" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="16" font-weight="600">Agent 模式</text>
    <text x="0" y="-78" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11">给目标，它自己跑完整个流程</text>

    <!-- Auto execution indicators -->
    <g transform="translate(0, 85)">
      <rect x="-90" y="-12" width="180" height="24" rx="12" fill="#10b981" opacity="0.15"/>
      <text x="0" y="4" text-anchor="middle" fill="#34d399" font-family="system-ui, sans-serif" font-size="10" font-weight="500">自动规划 · 自动执行 · 自动交付</text>
    </g>
  </g>

  <!-- Arrow marker -->
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#60a5fa"/>
    </marker>
  </defs>

  <!-- Bottom insight -->
  <text x="450" y="375" text-anchor="middle" fill="#64748b" font-family="system-ui, sans-serif" font-size="11">用 Agent 的人和不用的人，效率差距是 10-20 倍</text>
</svg>'''

# Figure 2: Agent Loop
fig2_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a1628"/>
      <stop offset="100%" style="stop-color:#1a2744"/>
    </linearGradient>
    <linearGradient id="observeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8b5cf6"/>
      <stop offset="100%" style="stop-color:#a78bfa"/>
    </linearGradient>
    <linearGradient id="thinkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3b82f6"/>
      <stop offset="100%" style="stop-color:#60a5fa"/>
    </linearGradient>
    <linearGradient id="actGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#10b981"/>
      <stop offset="100%" style="stop-color:#34d399"/>
    </linearGradient>
    <filter id="glow2">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="600" height="600" fill="url(#bgGrad2)"/>

  <!-- Center circle (loop core) -->
  <circle cx="300" cy="300" r="60" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2" opacity="0.8"/>
  <text x="300" y="295" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="14" font-weight="700">Agent</text>
  <text x="300" y="315" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">Loop</text>

  <!-- Observe node (top) -->
  <g transform="translate(300, 120)">
    <circle cx="0" cy="0" r="55" fill="url(#observeGrad)" filter="url(#glow2)"/>
    <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="18" font-weight="700">Observe</text>
    <text x="0" y="12" text-anchor="middle" fill="#e9d5ff" font-family="system-ui, sans-serif" font-size="11">观察环境</text>
    <!-- Icon: eye -->
    <ellipse cx="0" cy="-28" rx="12" ry="8" fill="none" stroke="#fff" stroke-width="1.5"/>
    <circle cx="0" cy="-28" r="4" fill="#fff"/>
  </g>

  <!-- Think node (right) -->
  <g transform="translate(480, 300)">
    <circle cx="0" cy="0" r="55" fill="url(#thinkGrad)" filter="url(#glow2)"/>
    <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="18" font-weight="700">Think</text>
    <text x="0" y="12" text-anchor="middle" fill="#bfdbfe" font-family="system-ui, sans-serif" font-size="11">思考决策</text>
    <!-- Icon: brain gear -->
    <path d="M0 -30 L-5 -25 L-5 -20 L-10 -20 L-10 -15 L-5 -15 L-5 -10 L0 -10 L5 -15 L10 -15 L10 -20 L5 -20 L5 -25 Z" fill="#fff" opacity="0.8" transform="translate(0, -2) scale(0.8)"/>
  </g>

  <!-- Act node (bottom) -->
  <g transform="translate(300, 480)">
    <circle cx="0" cy="0" r="55" fill="url(#actGrad)" filter="url(#glow2)"/>
    <text x="0" y="-8" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="18" font-weight="700">Act</text>
    <text x="0" y="12" text-anchor="middle" fill="#a7f3d0" font-family="system-ui, sans-serif" font-size="11">执行行动</text>
    <!-- Icon: lightning -->
    <path d="M5 -32 L-5 -22 L2 -22 L-5 -12 L8 -22 L0 -22 Z" fill="#fff"/>
  </g>

  <!-- Arrows connecting the loop -->
  <!-- Observe to Think -->
  <path d="M355 140 Q420 180 440 245" fill="none" stroke="#60a5fa" stroke-width="3" stroke-linecap="round"/>
  <polygon points="445,240 450,255 435,250" fill="#60a5fa"/>

  <!-- Think to Act -->
  <path d="M480 355 Q420 430 355 460" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round"/>
  <polygon points="360,455 345,465 350,450" fill="#34d399"/>

  <!-- Act to Observe -->
  <path d="M245 460 Q180 430 155 355" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linecap="round"/>
  <polygon points="150,360 155,345 165,360" fill="#a78bfa"/>

  <!-- Observe back to center -->
  <path d="M245 140 Q200 200 240 250" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,3"/>

  <!-- Task input arrow -->
  <g transform="translate(120, 180)">
    <rect x="-50" y="-15" width="100" height="30" rx="6" fill="#f59e0b" opacity="0.9"/>
    <text x="0" y="5" text-anchor="middle" fill="#0a1628" font-family="system-ui, sans-serif" font-size="11" font-weight="600">任务输入</text>
    <path d="M55 0 L100 50" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,3"/>
  </g>

  <!-- Result output arrow -->
  <g transform="translate(480, 420)">
    <path d="M-30 -20 L-30 -50" stroke="#10b981" stroke-width="2" stroke-dasharray="5,3"/>
    <rect x="-80" y="-75" width="100" height="30" rx="6" fill="#10b981" opacity="0.9"/>
    <text x="-30" y="-55" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="11" font-weight="600">结果输出</text>
  </g>

  <!-- Example flow text -->
  <g transform="translate(300, 300)">
    <text x="-180" y="-130" text-anchor="middle" fill="#a78bfa" font-family="system-ui, sans-serif" font-size="9">检查文件</text>
    <text x="130" y="-60" text-anchor="middle" fill="#60a5fa" font-family="system-ui, sans-serif" font-size="9">规划步骤</text>
    <text x="-180" y="130" text-anchor="middle" fill="#34d399" font-family="system-ui, sans-serif" font-size="9">执行工具</text>
  </g>

  <!-- Title -->
  <text x="300" y="45" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="20" font-weight="700">Agent 的核心循环</text>
  <text x="300" y="70" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12">持续循环直到任务完成</text>

  <!-- Footer insight -->
  <text x="300" y="580" text-anchor="middle" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">Claude Code、Codex、Manus……所有 Agent 都跑这个循环</text>
</svg>'''

# Figure 3: Five-step build process
fig3_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="500" viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a1628"/>
      <stop offset="100%" style="stop-color:#1a2744"/>
    </linearGradient>
    <linearGradient id="step1Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f59e0b"/>
      <stop offset="100%" style="stop-color:#fbbf24"/>
    </linearGradient>
    <linearGradient id="step2Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#8b5cf6"/>
      <stop offset="100%" style="stop-color:#a78bfa"/>
    </linearGradient>
    <linearGradient id="step3Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3b82f6"/>
      <stop offset="100%" style="stop-color:#60a5fa"/>
    </linearGradient>
    <linearGradient id="step4Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#10b981"/>
      <stop offset="100%" style="stop-color:#34d399"/>
    </linearGradient>
    <linearGradient id="step5Grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ec4899"/>
      <stop offset="100%" style="stop-color:#f472b6"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="900" height="500" fill="url(#bgGrad3)"/>

  <!-- Title -->
  <text x="450" y="50" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="22" font-weight="700">五步构建你的 AI 员工</text>
  <text x="450" y="75" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12">文件夹 + Markdown = 可移植的 AI 资产</text>

  <!-- Step 1: agents.md -->
  <g transform="translate(100, 180)">
    <rect x="-60" y="-50" width="120" height="100" rx="12" fill="#1e293b" filter="url(#shadow)"/>
    <rect x="-45" y="-35" width="90" height="55" rx="4" fill="#0f172a"/>
    <text x="0" y="-10" text-anchor="middle" fill="#fbbf24" font-family="monospace" font-size="9">agents.md</text>
    <text x="0" y="8" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">role: ...</text>
    <text x="0" y="18" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">context: ...</text>
    <!-- Brain icon -->
    <circle cx="0" cy="-65" r="22" fill="url(#step1Grad)"/>
    <text x="0" y="-60" text-anchor="middle" fill="#0a1628" font-family="system-ui, sans-serif" font-size="18">🧠</text>
    <text x="0" y="75" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="13" font-weight="600">大脑</text>
    <text x="0" y="95" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">System Prompt</text>
  </g>

  <!-- Arrow 1 -->
  <path d="M165 180 L210 180" stroke="#475569" stroke-width="2"/>
  <polygon points="215,180 205,175 205,185" fill="#475569"/>

  <!-- Step 2: memory.md -->
  <g transform="translate(280, 180)">
    <rect x="-60" y="-50" width="120" height="100" rx="12" fill="#1e293b" filter="url(#shadow)"/>
    <rect x="-45" y="-35" width="90" height="55" rx="4" fill="#0f172a"/>
    <text x="0" y="-10" text-anchor="middle" fill="#a78bfa" font-family="monospace" font-size="9">memory.md</text>
    <text x="0" y="8" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">偏好: 口语化</text>
    <text x="0" y="18" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">风格: 简洁</text>
    <!-- Memory icon -->
    <circle cx="0" cy="-65" r="22" fill="url(#step2Grad)"/>
    <text x="0" y="-60" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="18">📝</text>
    <text x="0" y="75" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="13" font-weight="600">记忆</text>
    <text x="0" y="95" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">持续学习</text>
  </g>

  <!-- Arrow 2 -->
  <path d="M345 180 L390 180" stroke="#475569" stroke-width="2"/>
  <polygon points="395,180 385,175 385,185" fill="#475569"/>

  <!-- Step 3: MCP -->
  <g transform="translate(460, 180)">
    <rect x="-60" y="-50" width="120" height="100" rx="12" fill="#1e293b" filter="url(#shadow)"/>
    <rect x="-45" y="-35" width="90" height="55" rx="4" fill="#0f172a"/>
    <text x="0" y="-10" text-anchor="middle" fill="#60a5fa" font-family="monospace" font-size="9">MCP</text>
    <!-- Connection lines -->
    <line x1="-30" y1="5" x2="-10" y2="5" stroke="#3b82f6" stroke-width="1"/>
    <line x1="-30" y1="12" x2="-10" y2="12" stroke="#3b82f6" stroke-width="1"/>
    <line x1="-30" y1="19" x2="-10" y2="19" stroke="#3b82f6" stroke-width="1"/>
    <circle cx="-5" cy="5" r="3" fill="#3b82f6"/>
    <circle cx="-5" cy="12" r="3" fill="#10b981"/>
    <circle cx="-5" cy="19" r="3" fill="#f59e0b"/>
    <!-- Plugin icon -->
    <circle cx="0" cy="-65" r="22" fill="url(#step3Grad)"/>
    <text x="0" y="-60" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="18">🔌</text>
    <text x="0" y="75" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="13" font-weight="600">工具</text>
    <text x="0" y="95" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">连接外部系统</text>
  </g>

  <!-- Arrow 3 -->
  <path d="M525 180 L570 180" stroke="#475569" stroke-width="2"/>
  <polygon points="575,180 565,175 565,185" fill="#475569"/>

  <!-- Step 4: Skills -->
  <g transform="translate(640, 180)">
    <rect x="-60" y="-50" width="120" height="100" rx="12" fill="#1e293b" filter="url(#shadow)"/>
    <rect x="-45" y="-35" width="90" height="55" rx="4" fill="#0f172a"/>
    <text x="0" y="-10" text-anchor="middle" fill="#34d399" font-family="monospace" font-size="9">skills/*.md</text>
    <text x="0" y="8" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">写提案.skill</text>
    <text x="0" y="18" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">早报.skill</text>
    <!-- Skill icon -->
    <circle cx="0" cy="-65" r="22" fill="url(#step4Grad)"/>
    <text x="0" y="-60" text-anchor="middle" fill="#0a1628" font-family="system-ui, sans-serif" font-size="18">⚡</text>
    <text x="0" y="75" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="13" font-weight="600">技能</text>
    <text x="0" y="95" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">工作流复用</text>
  </g>

  <!-- Arrow 4 -->
  <path d="M705 180 L750 180" stroke="#475569" stroke-width="2"/>
  <polygon points="755,180 745,175 745,185" fill="#475569"/>

  <!-- Step 5: Automation -->
  <g transform="translate(820, 180)">
    <rect x="-60" y="-50" width="120" height="100" rx="12" fill="#1e293b" filter="url(#shadow)"/>
    <rect x="-45" y="-35" width="90" height="55" rx="4" fill="#0f172a"/>
    <text x="0" y="-5" text-anchor="middle" fill="#f472b6" font-family="monospace" font-size="8">schedule:</text>
    <text x="0" y="8" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">daily: 9am</text>
    <text x="0" y="18" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">interval: 3h</text>
    <!-- Clock icon -->
    <circle cx="0" cy="-65" r="22" fill="url(#step5Grad)"/>
    <text x="0" y="-60" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="18">⏰</text>
    <text x="0" y="75" text-anchor="middle" fill="#fff" font-family="system-ui, sans-serif" font-size="13" font-weight="600">自动化</text>
    <text x="0" y="95" text-anchor="middle" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">定时触发</text>
  </g>

  <!-- Bottom: Folder structure preview -->
  <g transform="translate(450, 380)">
    <rect x="-280" y="-50" width="560" height="110" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1"/>
    <text x="-260" y="-25" fill="#64748b" font-family="monospace" font-size="10">📁 executive_assistant/</text>
    <text x="-240" y="-5" fill="#fbbf24" font-family="monospace" font-size="10">├── agents.md</text>
    <text x="-240" y="15" fill="#a78bfa" font-family="monospace" font-size="10">├── memory.md</text>
    <text x="-240" y="35" fill="#60a5fa" font-family="monospace" font-size="10">├── mcp-config.json</text>
    <text x="-240" y="55" fill="#34d399" font-family="monospace" font-size="10">└── skills/</text>
    <text x="-220" y="55" fill="#94a3b8" font-family="monospace" font-size="10">├── proposal.skill</text>
    <text x="-220" y="55" fill="#94a3b8" font-family="monospace" font-size="10" dx="130">└── daily-brief.skill</text>
  </g>

  <!-- Key insight -->
  <text x="450" y="475" text-anchor="middle" fill="#64748b" font-family="system-ui, sans-serif" font-size="10">技术会迭代，但你的 Markdown 文件可以迁移到任何框架</text>
</svg>'''

# Write SVG files
output_dir = "/Users/wp931120/lobsterai/project/wp_work/20260319_ai_agent_team"

with open(os.path.join(output_dir, "fig1_chat_vs_agent.svg"), "w", encoding="utf-8") as f:
    f.write(fig1_svg)

with open(os.path.join(output_dir, "fig2_agent_loop.svg"), "w", encoding="utf-8") as f:
    f.write(fig2_svg)

with open(os.path.join(output_dir, "fig3_five_steps.svg"), "w", encoding="utf-8") as f:
    f.write(fig3_svg)

print("✅ Generated 3 SVG figures:")
print(f"  - {output_dir}/fig1_chat_vs_agent.svg")
print(f"  - {output_dir}/fig2_agent_loop.svg")
print(f"  - {output_dir}/fig3_five_steps.svg")
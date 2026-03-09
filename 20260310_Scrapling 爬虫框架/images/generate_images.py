#!/usr/bin/env python3
"""
生成 Scrapling 文章配图
"""

import os

# 确保输出目录存在
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)


def generate_architecture_svg():
    """生成 Scrapling 架构图"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2D3748;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1A202C;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="boxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4299E1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2B6CB0;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="coreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#48BB78;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2F855A;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="800" height="500" fill="#F7FAFC"/>

  <!-- 标题 -->
  <rect x="0" y="0" width="800" height="60" fill="url(#headerGrad)"/>
  <text x="400" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="white">Scrapling 架构总览</text>

  <!-- 用户层 -->
  <rect x="50" y="90" width="140" height="60" rx="8" fill="url(#boxGrad)" filter="url(#shadow)"/>
  <text x="120" y="125" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="white" font-weight="bold">开发者</text>

  <rect x="610" y="90" width="140" height="60" rx="8" fill="#ED8936" filter="url(#shadow)"/>
  <text x="680" y="125" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="white" font-weight="bold">AI 助手</text>

  <!-- 箭头向下 -->
  <line x1="120" y1="150" x2="120" y2="190" stroke="#4A5568" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="680" y1="150" x2="680" y2="190" stroke="#4A5568" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- API 层 -->
  <rect x="40" y="200" width="220" height="70" rx="8" fill="#667EEA" filter="url(#shadow)"/>
  <text x="150" y="235" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="white" font-weight="bold">Spider API</text>
  <text x="150" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#E2E8F0">类 Scrapy 接口</text>

  <rect x="290" y="200" width="220" height="70" rx="8" fill="#667EEA" filter="url(#shadow)"/>
  <text x="400" y="235" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="white" font-weight="bold">Fetcher API</text>
  <text x="400" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#E2E8F0">三种获取器</text>

  <rect x="540" y="200" width="220" height="70" rx="8" fill="#667EEA" filter="url(#shadow)"/>
  <text x="650" y="235" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="white" font-weight="bold">MCP Server</text>
  <text x="650" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#E2E8F0">AI 集成接口</text>

  <!-- 箭头向下 -->
  <line x1="400" y1="270" x2="400" y2="310" stroke="#4A5568" stroke-width="2"/>

  <!-- 核心引擎 -->
  <rect x="200" y="320" width="400" height="80" rx="10" fill="url(#coreGrad)" filter="url(#shadow)"/>
  <text x="400" y="355" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="white" font-weight="bold">核心解析引擎</text>
  <text x="400" y="380" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#E2E8F0">CSS/XPath 选择器 | 自适应定位 | 智能相似度算法</text>

  <!-- 箭头向下 -->
  <line x1="400" y1="400" x2="400" y2="430" stroke="#4A5568" stroke-width="2"/>

  <!-- 底层 -->
  <rect x="100" y="440" width="180" height="50" rx="6" fill="#718096" filter="url(#shadow)"/>
  <text x="190" y="470" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="white" font-weight="bold">lxml</text>

  <rect x="310" y="440" width="180" height="50" rx="6" fill="#718096" filter="url(#shadow)"/>
  <text x="400" y="470" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="white" font-weight="bold">curl_cffi</text>

  <rect x="520" y="440" width="180" height="50" rx="6" fill="#718096" filter="url(#shadow)"/>
  <text x="610" y="470" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="white" font-weight="bold">Playwright</text>

  <!-- 箭头定义 -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#4A5568"/>
    </marker>
  </defs>
</svg>'''

    output_path = os.path.join(output_dir, "architecture.svg")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✓ 生成: {output_path}")


def generate_comparison_svg():
    """生成性能对比图"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 550">
  <defs>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2D3748;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1A202C;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#48BB78;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2F855A;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="barGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4299E1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2B6CB0;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="900" height="550" fill="#F7FAFC"/>

  <!-- 标题 -->
  <rect x="0" y="0" width="900" height="60" fill="url(#titleGrad)"/>
  <text x="450" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="white">性能对比：文本提取速度 (5000 个元素)</text>

  <!-- 图表区域 -->
  <g transform="translate(80, 100)">
    <!-- Y 轴标签 -->
    <text x="-10" y="25" text-anchor="end" font-family="Arial" font-size="12" fill="#4A5568">Scrapling</text>
    <text x="-10" y="75" text-anchor="end" font-family="Arial" font-size="12" fill="#4A5568">Parsel/Scrapy</text>
    <text x="-10" y="125" text-anchor="end" font-family="Arial" font-size="12" fill="#4A5568">Raw Lxml</text>
    <text x="-10" y="175" text-anchor="end" font-family="Arial" font-size="12" fill="#4A5568">PyQuery</text>
    <text x="-10" y="225" text-anchor="end" font-family="Arial" font-size="12" fill="#4A5568">Selectolax</text>
    <text x="-10" y="275" text-anchor="end" font-family="Arial" font-size="12" fill="#4A5568">BS4 + Lxml</text>
    <text x="-10" y="325" text-anchor="end" font-family="Arial" font-size="12" fill="#4A5568">BS4 + html5lib</text>

    <!-- 条形图 -->
    <rect x="0" y="10" width="20" height="30" rx="3" fill="url(#barGrad)"/>
    <text x="30" y="30" font-family="Arial" font-size="12" fill="#2D3748" font-weight="bold">2.02 ms</text>

    <rect x="0" y="60" width="20" height="30" rx="3" fill="url(#barGrad2)"/>
    <text x="30" y="80" font-family="Arial" font-size="12" fill="#2D3748">2.04 ms</text>

    <rect x="0" y="110" width="25" height="30" rx="3" fill="url(#barGrad2)"/>
    <text x="35" y="130" font-family="Arial" font-size="12" fill="#2D3748">2.54 ms</text>

    <rect x="0" y="160" width="242" height="30" rx="3" fill="url(#barGrad2)"/>
    <text x="252" y="180" font-family="Arial" font-size="12" fill="#2D3748">24.17 ms</text>

    <rect x="0" y="210" width="826" height="30" rx="3" fill="url(#barGrad2)"/>
    <text x="836" y="230" font-family="Arial" font-size="12" fill="#2D3748">82.63 ms</text>

    <rect x="0" y="260" width="1584" height="30" rx="3" fill="#E53E3E"/>
    <text x="1594" y="280" font-family="Arial" font-size="12" fill="#2D3748">1584.31 ms</text>

    <rect x="0" y="310" width="3392" height="30" rx="3" fill="#E53E3E" opacity="0.5"/>
    <text x="3402" y="330" font-family="Arial" font-size="12" fill="#2D3748">3391.91 ms</text>

    <!-- X 轴 -->
    <line x1="0" y1="360" x2="750" y2="360" stroke="#CBD5E0" stroke-width="2"/>
    <text x="0" y="380" font-family="Arial" font-size="11" fill="#718096">0</text>
    <text x="200" y="380" font-family="Arial" font-size="11" fill="#718096">500ms</text>
    <text x="400" y="380" font-family="Arial" font-size="11" fill="#718096">1000ms</text>
    <text x="600" y="380" font-family="Arial" font-size="11" fill="#718096">1500ms</text>
    <text x="750" y="380" font-family="Arial" font-size="11" fill="#718096">2000ms+</text>
  </g>

  <!-- 结论框 -->
  <rect x="550" y="120" width="300" height="140" rx="10" fill="#FFFFFF" stroke="#48BB78" stroke-width="2"/>
  <text x="700" y="150" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold" fill="#2F855A">关键结论</text>
  <text x="700" y="180" text-anchor="middle" font-family="Arial" font-size="13" fill="#4A5568">Scrapling 解析速度</text>
  <text x="700" y="205" text-anchor="middle" font-family="Arial" font-size="24" font-weight="bold" fill="#2F855A">比 BS4 快 700 倍+</text>
  <text x="700" y="235" text-anchor="middle" font-family="Arial" font-size="13" fill="#4A5568">与 Scrapy 性能相当</text>
  <text x="700" y="255" text-anchor="middle" font-family="Arial" font-size="12" fill="#718096">基于 lxml 优化</text>
</svg>'''

    output_path = os.path.join(output_dir, "comparison.svg")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✓ 生成：{output_path}")


def generate_workflow_svg():
    """生成 Scrapling 工作流程图"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2D3748;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1A202C;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="stepGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4299E1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2B6CB0;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="900" height="600" fill="#F7FAFC"/>

  <!-- 标题 -->
  <rect x="0" y="0" width="900" height="60" fill="url(#headerGrad)"/>
  <text x="450" y="38" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="white">Scrapling 工作流程</text>

  <!-- 步骤 1 -->
  <g transform="translate(100, 100)">
    <rect x="0" y="0" width="200" height="80" rx="10" fill="url(#stepGrad)" filter="url(#shadow)"/>
    <text x="100" y="35" text-anchor="middle" font-family="Arial" font-size="16" fill="white" font-weight="bold">1. 选择 Fetcher</text>
    <text x="100" y="58" text-anchor="middle" font-family="Arial" font-size="12" fill="#E2E8F0">Fetcher / Stealthy / Dynamic</text>
  </g>

  <!-- 箭头 -->
  <path d="M 300 140 L 350 140" stroke="#4A5568" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- 步骤 2 -->
  <g transform="translate(350, 100)">
    <rect x="0" y="0" width="200" height="80" rx="10" fill="url(#stepGrad)" filter="url(#shadow)"/>
    <text x="100" y="35" text-anchor="middle" font-family="Arial" font-size="16" fill="white" font-weight="bold">2. 发起请求</text>
    <text x="100" y="58" text-anchor="middle" font-family="Arial" font-size="12" fill="#E2E8F0">HTTP / 浏览器自动化</text>
  </g>

  <!-- 箭头 -->
  <path d="M 550 140 L 600 140" stroke="#4A5568" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- 步骤 3 -->
  <g transform="translate(600, 100)">
    <rect x="0" y="0" width="200" height="80" rx="10" fill="#48BB78" filter="url(#shadow)"/>
    <text x="100" y="35" text-anchor="middle" font-family="Arial" font-size="16" fill="white" font-weight="bold">3. 解析 HTML</text>
    <text x="100" y="58" text-anchor="middle" font-family="Arial" font-size="12" fill="#E2E8F0">CSS / XPath / 自适应</text>
  </g>

  <!-- 向下的箭头 -->
  <path d="M 700 180 L 700 230" stroke="#4A5568" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- 步骤 4 -->
  <g transform="translate(600, 240)">
    <rect x="0" y="0" width="200" height="80" rx="10" fill="#ED8936" filter="url(#shadow)"/>
    <text x="100" y="35" text-anchor="middle" font-family="Arial" font-size="16" fill="white" font-weight="bold">4. 提取数据</text>
    <text x="100" y="58" text-anchor="middle" font-family="Arial" font-size="12" fill="#E2E8F0">.get() / .getall()</text>
  </g>

  <!-- 向左的箭头 -->
  <path d="M 600 280 L 350 280" stroke="#4A5568" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- 步骤 5 -->
  <g transform="translate(100, 240)">
    <rect x="0" y="0" width="200" height="80" rx="10" fill="#9F7AEA" filter="url(#shadow)"/>
    <text x="100" y="35" text-anchor="middle" font-family="Arial" font-size="16" fill="white" font-weight="bold">5. 导出数据</text>
    <text x="100" y="58" text-anchor="middle" font-family="Arial" font-size="12" fill="#E2E8F0">JSON / JSONL / CSV</text>
  </g>

  <!-- 中间的功能框 -->
  <g transform="translate(250, 380)">
    <rect x="0" y="0" width="400" height="160" rx="10" fill="#FFFFFF" stroke="#4299E1" stroke-width="2"/>
    <text x="200" y="35" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold" fill="#2D3748">核心能力</text>

    <!-- 能力列表 -->
    <g transform="translate(20, 55)">
      <text x="0" y="20" font-family="Arial" font-size="13" fill="#4A5568">✓ 自适应元素定位</text>
      <text x="0" y="45" font-family="Arial" font-size="13" fill="#4A5568">✓ 反爬虫绕过 (Cloudflare 等)</text>
      <text x="0" y="70" font-family="Arial" font-size="13" fill="#4A5568">✓ 并发控制与暂停恢复</text>
      <text x="0" y="95" font-family="Arial" font-size="13" fill="#4A5568">✓ AI 辅助爬取 (MCP Server)</text>
    </g>

    <g transform="translate(220, 55)">
      <text x="0" y="20" font-family="Arial" font-size="13" fill="#4A5568">✓ TLS 指纹模拟</text>
      <text x="0" y="45" font-family="Arial" font-size="13" fill="#4A5568">✓ Canvas/WebGL 处理</text>
      <text x="0" y="70" font-family="Arial" font-size="13" fill="#4A5568">✓ 代理轮换</text>
      <text x="0" y="95" font-family="Arial" font-size="13" fill="#4A5568">✓ 流式输出</text>
    </g>
  </g>

  <!-- 箭头定义 -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#4A5568"/>
    </marker>
  </defs>
</svg>'''

    output_path = os.path.join(output_dir, "workflow.svg")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✓ 生成：{output_path}")


if __name__ == "__main__":
    generate_architecture_svg()
    generate_comparison_svg()
    generate_workflow_svg()
    print("\n所有图片生成完成！")

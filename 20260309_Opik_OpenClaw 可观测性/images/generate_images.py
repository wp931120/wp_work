#!/usr/bin/env python3
"""
Generate SVG images for Opik + OpenClaw article
"""

def create_architecture_diagram():
    """Create system architecture diagram"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#666"/>
    </marker>
    <style>
      .box { fill: #4A90D9; stroke: #2E5C8A; stroke-width: 2; }
      .box-secondary { fill: #7CB342; stroke: #558B2F; stroke-width: 2; }
      .box-tertiary { fill: #AB47BC; stroke: #7B1FA2; stroke-width: 2; }
      .label { fill: white; font-family: Arial, sans-serif; font-size: 14px; text-anchor: middle; }
      .arrow { stroke: #666; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
      .title { fill: #333; font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; }
    </style>
  </defs>

  <!-- Title -->
  <text x="400" y="30" class="title">OpenClaw + Opik 系统架构</text>

  <!-- User -->
  <rect x="50" y="80" width="100" height="60" rx="5" class="box"/>
  <text x="100" y="115" class="label">用户</text>

  <!-- OpenClaw Gateway -->
  <rect x="250" y="80" width="150" height="60" rx="5" class="box-secondary"/>
  <text x="325" y="105" class="label">OpenClaw Gateway</text>
  <text x="325" y="125" class="label" style="font-size: 10px;">(接收消息)</text>

  <!-- Agent Core -->
  <rect x="250" y="200" width="150" height="60" rx="5" class="box-secondary"/>
  <text x="325" y="225" class="label">Agent Core</text>
  <text x="325" y="245" class="label" style="font-size: 10px;">(执行逻辑)</text>

  <!-- Opik Plugin -->
  <rect x="250" y="320" width="150" height="60" rx="5" class="box-tertiary"/>
  <text x="325" y="345" class="label">@opik/opik-openclaw</text>
  <text x="325" y="365" class="label" style="font-size: 10px;">(事件监听)</text>

  <!-- Opik Platform -->
  <rect x="550" y="200" width="180" height="120" rx="5" class="box"/>
  <text x="640" y="245" class="label">Opik Platform</text>
  <text x="640" y="270" class="label" style="font-size: 11px;">• Trace 追踪</text>
  <text x="640" y="290" class="label" style="font-size: 11px;">• Span 分析</text>
  <text x="640" y="310" class="label" style="font-size: 11px;">• 成本监控</text>

  <!-- Developer -->
  <rect x="550" y="380" width="180" height="60" rx="5" class="box"/>
  <text x="640" y="415" class="label">开发者</text>
  <text x="640" y="435" class="label" style="font-size: 10px;">(Dashboard 查看)</text>

  <!-- Arrows -->
  <line x1="150" y1="110" x2="250" y2="110" class="arrow"/>
  <line x1="325" y1="140" x2="325" y2="200" class="arrow"/>
  <line x1="325" y1="260" x2="325" y2="320" class="arrow"/>
  <line x1="400" y1="350" x2="550" y2="260" class="arrow"/>
  <line x1="640" y1="320" x2="640" y2="380" class="arrow"/>
</svg>'''

    with open('architecture.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Created architecture.svg")
    return 'architecture.svg'


def create_trace_flow_diagram():
    """Create trace flow diagram"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 600" width="700" height="600">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#1976D2"/>
    </marker>
    <style>
      .step { fill: #E3F2FD; stroke: #1976D2; stroke-width: 2; rx: 5; }
      .step-highlight { fill: #FFF3E0; stroke: #F57C00; stroke-width: 2; rx: 5; }
      .label { fill: #333; font-family: Arial, sans-serif; font-size: 13px; text-anchor: middle; }
      .event { fill: #7B1FA2; font-family: Arial, sans-serif; font-size: 11px; text-anchor: middle; }
      .arrow { stroke: #1976D2; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
      .title { fill: #333; font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; text-anchor: middle; }
    </style>
  </defs>

  <!-- Title -->
  <text x="350" y="30" class="title">Trace 生命周期流程</text>

  <!-- Steps -->
  <rect x="230" y="50" width="240" height="40" class="step-highlight"/>
  <text x="350" y="75" class="label">用户消息</text>

  <line x1="350" y1="90" x2="350" y2="120" class="arrow"/>
  <text x="490" y="110" class="event">[llm_input]</text>

  <rect x="230" y="120" width="240" height="40" class="step"/>
  <text x="350" y="145" class="label">创建 Trace + LLM Span</text>

  <line x1="350" y1="160" x2="350" y2="190" class="arrow"/>
  <text x="490" y="180" class="event">[before_tool_call]</text>

  <rect x="230" y="190" width="240" height="40" class="step"/>
  <text x="350" y="215" class="label">创建 Tool Span</text>

  <line x1="350" y1="230" x2="350" y2="260" class="arrow"/>
  <text x="490" y="250" class="event">[after_tool_call]</text>

  <rect x="230" y="260" width="240" height="40" class="step"/>
  <text x="350" y="285" class="label">完成 Tool Span</text>

  <line x1="350" y1="300" x2="350" y2="330" class="arrow"/>
  <text x="490" y="320" class="event">[llm_output]</text>

  <rect x="230" y="330" width="240" height="40" class="step"/>
  <text x="350" y="350" class="label">完成 LLM Span</text>
  <text x="350" y="365" class="label" style="font-size: 11px;">(记录 Token/成本)</text>

  <line x1="350" y1="370" x2="350" y2="400" class="arrow"/>
  <text x="490" y="390" class="event">[agent_end]</text>

  <rect x="230" y="400" width="240" height="40" class="step"/>
  <text x="350" y="425" class="label">关闭所有 Span + Trace</text>

  <line x1="350" y1="440" x2="350" y2="470" class="arrow"/>
  <text x="490" y="460" class="event">[flush]</text>

  <rect x="230" y="470" width="240" height="40" class="step"/>
  <text x="350" y="495" class="label">数据发送到 Opik</text>
</svg>'''

    with open('trace_flow.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Created trace_flow.svg")
    return 'trace_flow.svg'


def create_dashboard_mockup():
    """Create dashboard mockup"""
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">
  <defs>
    <style>
      .panel { fill: white; stroke: #DDD; stroke-width: 1; rx: 5; }
      .panel-header { fill: #F5F5F5; stroke: #DDD; stroke-width: 1; }
      .metric-value { fill: #1976D2; font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; }
      .metric-label { fill: #666; font-family: Arial, sans-serif; font-size: 12px; }
      .chart-bar { fill: #4A90D9; }
      .title { fill: #333; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; }
      .alert { fill: #F44336; font-family: Arial, sans-serif; font-size: 12px; }
    </style>
  </defs>

  <!-- Title -->
  <text x="400" y="30" style="text-anchor: middle; font-size: 18px; font-weight: bold; fill: #333;">Opik Dashboard 示例</text>

  <!-- Top metrics panel -->
  <rect x="50" y="60" width="700" height="100" class="panel"/>
  <rect x="50" y="60" width="700" height="30" class="panel-header"/>
  <text x="70" y="80" style="fill: #333; font-size: 14px; font-weight: bold;">关键指标</text>

  <!-- Metrics -->
  <text x="100" y="110" style="text-anchor: middle; fill: #1976D2; font-size: 24px; font-weight: bold;">1,234</text>
  <text x="100" y="135" style="text-anchor: middle; fill: #666; font-size: 12px;">Total Traces</text>

  <text x="250" y="110" style="text-anchor: middle; fill: #1976D2; font-size: 24px; font-weight: bold;">2.3%</text>
  <text x="250" y="135" style="text-anchor: middle; fill: #666; font-size: 12px;">Error Rate</text>

  <text x="400" y="110" style="text-anchor: middle; fill: #1976D2; font-size: 24px; font-weight: bold;">1.8s</text>
  <text x="400" y="135" style="text-anchor: middle; fill: #666; font-size: 12px;">Avg Duration</text>

  <text x="550" y="110" style="text-anchor: middle; fill: #1976D2; font-size: 24px; font-weight: bold;">$234</text>
  <text x="550" y="135" style="text-anchor: middle; fill: #666; font-size: 12px;">Total Cost</text>

  <text x="700" y="110" style="text-anchor: middle; fill: #1976D2; font-size: 24px; font-weight: bold;">45.2K</text>
  <text x="700" y="135" style="text-anchor: middle; fill: #666; font-size: 12px;">Token Usage</text>

  <!-- Chart panel -->
  <rect x="50" y="180" width="400" height="280" class="panel"/>
  <rect x="50" y="180" width="400" height="30" class="panel-header"/>
  <text x="70" y="200" style="fill: #333; font-size: 14px; font-weight: bold;">Token 使用趋势</text>

  <!-- Bar chart -->
  <rect x="90" y="400" width="35" height="-60" class="chart-bar"/>
  <text x="107" y="455" style="text-anchor: middle; fill: #666; font-size: 10px;">Mon</text>

  <rect x="135" y="380" width="35" height="-80" class="chart-bar"/>
  <text x="152" y="455" style="text-anchor: middle; fill: #666; font-size: 10px;">Tue</text>

  <rect x="180" y="415" width="35" height="-45" class="chart-bar"/>
  <text x="197" y="455" style="text-anchor: middle; fill: #666; font-size: 10px;">Wed</text>

  <rect x="225" y="370" width="35" height="-90" class="chart-bar"/>
  <text x="242" y="455" style="text-anchor: middle; fill: #666; font-size: 10px;">Thu</text>

  <rect x="270" y="390" width="35" height="-70" class="chart-bar"/>
  <text x="287" y="455" style="text-anchor: middle; fill: #666; font-size: 10px;">Fri</text>

  <rect x="315" y="375" width="35" height="-85" class="chart-bar"/>
  <text x="332" y="455" style="text-anchor: middle; fill: #666; font-size: 10px;">Sat</text>

  <rect x="360" y="395" width="35" height="-65" class="chart-bar"/>
  <text x="377" y="455" style="text-anchor: middle; fill: #666; font-size: 10px;">Sun</text>

  <!-- Alerts panel -->
  <rect x="470" y="180" width="280" height="130" class="panel"/>
  <rect x="470" y="180" width="280" height="30" class="panel-header"/>
  <text x="490" y="200" style="fill: #333; font-size: 14px; font-weight: bold;">活动告警</text>

  <text x="490" y="230" style="fill: #F44336; font-size: 12px;">⚠ 高错误率 (5.2%)</text>
  <text x="490" y="255" style="fill: #F44336; font-size: 12px;">⚠ 成本接近预算 (85%)</text>
  <text x="490" y="280" style="fill: #4CAF50; font-size: 12px;">✓ 系统运行正常</text>

  <!-- Recent traces panel -->
  <rect x="470" y="320" width="280" height="140" class="panel"/>
  <rect x="470" y="320" width="280" height="30" class="panel-header"/>
  <text x="490" y="340" style="fill: #333; font-size: 14px; font-weight: bold;">最近 Trace</text>

  <text x="490" y="365" style="fill: #333; font-size: 11px;">#abc123  success  1.2s</text>
  <text x="490" y="385" style="fill: #333; font-size: 11px;">#def456  error  3.5s</text>
  <text x="490" y="405" style="fill: #333; font-size: 11px;">#ghi789  success  0.8s</text>
  <text x="490" y="425" style="fill: #333; font-size: 11px;">#jkl012  success  2.1s</text>
</svg>'''

    with open('dashboard.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Created dashboard.svg")
    return 'dashboard.svg'


if __name__ == '__main__':
    create_architecture_diagram()
    create_trace_flow_diagram()
    create_dashboard_mockup()
    print("All SVG images generated!")

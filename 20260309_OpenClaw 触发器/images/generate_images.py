#!/usr/bin/env python3
"""
Generate diagrams for OpenClaw Triggers article
"""

import svgwrite
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

def create_trigger_flowchart():
    """Create a flowchart showing the 7 trigger types"""

    svg_file = OUTPUT_DIR / "trigger_types_diagram.svg"
    dwg = svgwrite.Drawing(svg_file, size=(800, 600))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(800, 600), fill='#f8f9fa'))

    # Title
    dwg.add(dwg.text('OpenClaw 7 种 Agent 触发器', insert=(400, 40),
                     font_size='24', font_weight='bold', text_anchor='middle', fill='#2c3e50'))

    # Trigger types with icons and colors
    triggers = [
        ('关键词触发', '#3498db', 100, 100),
        ('正则触发', '#e74c3c', 400, 100),
        ('意图触发', '#2ecc71', 700, 100),
        ('上下文触发', '#f39c12', 100, 250),
        ('时间触发', '#9b59b6', 400, 250),
        ('事件触发', '#1abc9c', 700, 250),
        ('组合触发', '#34495e', 400, 400),
    ]

    # Draw trigger boxes
    for name, color, x, y in triggers:
        # Box
        dwg.add(dwg.rect(insert=(x, y), size=(180, 80), rx=10, fill=color, opacity=0.9))
        # Text
        dwg.add(dwg.text(name, insert=(x + 90, y + 45),
                         font_size='16', text_anchor='middle', fill='white', font_weight='bold'))

    # Center hub
    dwg.add(dwg.circle(center=(400, 300), r=50, fill='#ecf0f1', stroke='#34495e', stroke_width=3))
    dwg.add(dwg.text('Agent\n调度中心', insert=(400, 295),
                     font_size='14', text_anchor='middle', fill='#2c3e50'))

    # Arrows from triggers to center
    center = (400, 300)
    trigger_centers = [
        (190, 140), (490, 140), (790, 140),
        (190, 290), (490, 290), (790, 290),
        (490, 440)
    ]

    for tc in trigger_centers:
        dwg.add(dwg.line(start=tc, end=center, stroke='#95a5a6', stroke_width=2, opacity=0.5))

    dwg.save()
    print(f"Created: {svg_file}")
    return svg_file


def create_decision_tree():
    """Create a decision tree for choosing trigger types"""

    svg_file = OUTPUT_DIR / "decision_tree.svg"
    dwg = svgwrite.Drawing(svg_file, size=(900, 700))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(900, 700), fill='#ffffff'))

    # Title
    dwg.add(dwg.text('触发器选择决策树', insert=(450, 30),
                     font_size='22', font_weight='bold', text_anchor='middle', fill='#2c3e50'))

    # Decision tree nodes
    nodes = [
        # Level 1 - Root
        (450, 80, '你的需求是什么？', '#3498db', 200, 60),

        # Level 2
        (150, 180, '简单指令响应？', '#e74c3c', 140, 50),
        (450, 180, '需要提取参数？', '#e74c3c', 140, 50),
        (750, 180, '表达方式多样？', '#e74c3c', 140, 50),

        # Level 3
        (100, 280, '依赖对话历史？', '#f39c12', 140, 50),
        (200, 280, '定时任务？', '#f39c12', 140, 50),
        (400, 280, '响应外部事件？', '#f39c12', 140, 50),
        (500, 280, '多重条件？', '#f39c12', 140, 50),
        (700, 280, '自然语言理解？', '#f39c12', 140, 50),
        (800, 280, '复杂业务逻辑？', '#f39c12', 140, 50),

        # Level 4 - Results
        (150, 380, '关键词触发', '#2ecc71', 100, 40),
        (250, 380, '正则触发', '#2ecc71', 100, 40),
        (450, 380, '上下文触发', '#2ecc71', 100, 40),
        (550, 380, '时间触发', '#2ecc71', 100, 40),
        (650, 380, '事件触发', '#2ecc71', 100, 40),
        (750, 380, '意图触发', '#2ecc71', 100, 40),
        (850, 380, '组合触发', '#2ecc71', 100, 40),
    ]

    # Draw nodes
    for x, y, text, color, w, h in nodes:
        dwg.add(dwg.rect(insert=(x - w/2, y - h/2), size=(w, h), rx=8, fill=color, opacity=0.9))
        dwg.add(dwg.text(text, insert=(x, y + 5),
                         font_size='13', text_anchor='middle', fill='white'))

    # Draw connecting lines
    lines = [
        # Root to Level 2
        ((450, 140), (150, 180)),
        ((450, 140), (450, 180)),
        ((450, 140), (750, 180)),

        # Level 2 to Level 3
        ((150, 230), (100, 280)),
        ((150, 230), (200, 280)),
        ((450, 230), (400, 280)),
        ((450, 230), (500, 280)),
        ((750, 230), (700, 280)),
        ((750, 230), (800, 280)),

        # Level 3 to Level 4
        ((100, 330), (150, 380)),
        ((200, 330), (250, 380)),
        ((400, 330), (450, 380)),
        ((500, 330), (550, 380)),
        ((600, 330), (650, 380)),
        ((700, 330), (750, 380)),
        ((800, 330), (850, 380)),
    ]

    for start, end in lines:
        dwg.add(dwg.line(start=start, end=end, stroke='#95a5a6', stroke_width=2, opacity=0.6))

    dwg.save()
    print(f"Created: {svg_file}")
    return svg_file


def create_comparison_table():
    """Create a comparison table of trigger types"""

    svg_file = OUTPUT_DIR / "comparison_table.svg"
    dwg = svgwrite.Drawing(svg_file, size=(800, 500))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(800, 500), fill='#ffffff'))

    # Title
    dwg.add(dwg.text('7 种触发器对比', insert=(400, 35),
                     font_size='20', font_weight='bold', text_anchor='middle', fill='#2c3e50'))

    # Table headers
    headers = ['触发器类型', '适用场景', '配置难度', '响应速度']
    col_widths = [120, 280, 120, 120]
    x_positions = [50, 170, 450, 570]

    # Header row
    for i, header in enumerate(headers):
        dwg.add(dwg.rect(insert=(x_positions[i] - 50, 60),
                         size=(col_widths[i], 40), fill='#34495e'))
        dwg.add(dwg.text(header, insert=(x_positions[i], 85),
                         font_size='14', text_anchor='middle', fill='white', font_weight='bold'))

    # Data rows
    data = [
        ('关键词触发', '固定指令响应', '⭐', '⚡⚡⚡'),
        ('正则触发', '结构化参数', '⭐⭐', '⚡⚡⚡'),
        ('意图触发', '自然语言', '⭐⭐⭐', '⚡⚡'),
        ('上下文触发', '多轮对话', '⭐⭐⭐⭐', '⚡⚡'),
        ('时间触发', '定时任务', '⭐⭐', '⚡⚡⚡'),
        ('事件触发', '外部集成', '⭐⭐⭐', '⚡⚡⚡'),
        ('组合触发', '复杂条件', '⭐⭐⭐⭐⭐', '⚡'),
    ]

    colors = ['#ecf0f1', '#ffffff']

    for i, (name, scenario, difficulty, speed) in enumerate(data):
        y = 110 + i * 50
        color = colors[i % 2]

        # Row background
        dwg.add(dwg.rect(insert=(50, y), size=(700, 48), fill=color, stroke='#bdc3c7'))

        # Cells
        dwg.add(dwg.text(name, insert=(110, y + 30), font_size='13', text_anchor='middle', fill='#2c3e50'))
        dwg.add(dwg.text(scenario, insert=(310, y + 30), font_size='13', text_anchor='middle', fill='#2c3e50'))
        dwg.add(dwg.text(difficulty, insert=(510, y + 30), font_size='16', text_anchor='middle', fill='#2c3e50'))
        dwg.add(dwg.text(speed, insert=(630, y + 30), font_size='16', text_anchor='middle', fill='#2c3e50'))

    dwg.save()
    print(f"Created: {svg_file}")
    return svg_file


if __name__ == '__main__':
    create_trigger_flowchart()
    create_decision_tree()
    create_comparison_table()
    print("\nAll diagrams created successfully!")

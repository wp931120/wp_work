#!/usr/bin/env python3
"""Create simple diagram images using PIL"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

def get_font(size=24):
    """Get a font, fallback to default if system fonts not available"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/PingFang.ttc", size)
        except:
            return ImageFont.load_default()

def create_trigger_types_image():
    """Create 7 trigger types overview image"""
    width, height = 1200, 700
    img = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(img)

    # Title
    font_title = get_font(32)
    font_normal = get_font(20)
    font_small = get_font(16)

    draw.text((width//2, 30), "OpenClaw 7 种 Agent 触发器", fill='#2c3e50', font=font_title, anchor='mm')

    # Trigger boxes data
    triggers = [
        ('1. 关键词触发', '#3498db', 100, 100),
        ('2. 正则触发', '#e74c3c', 400, 100),
        ('3. 意图触发', '#2ecc71', 700, 100),
        ('4. 上下文触发', '#f39c12', 100, 280),
        ('5. 时间触发', '#9b59b6', 400, 280),
        ('6. 事件触发', '#1abc9c', 700, 280),
        ('7. 组合触发', '#34495e', 400, 460),
    ]

    # Draw boxes
    box_width, box_height = 250, 100
    for name, color, x, y in triggers:
        # Box with rounded corners (simulated with rectangle)
        draw.rounded_rectangle([(x, y), (x + box_width, y + box_height)], radius=15, fill=color)
        # Text
        draw.text((x + box_width//2, y + box_height//2), name, fill='white', font=font_normal, anchor='mm')

    # Center hub
    center_x, center_y = width//2, 380
    draw.ellipse([(center_x - 60, center_y - 60), (center_x + 60, center_y + 60)], fill='#ecf0f1', outline='#34495e', width=3)
    draw.text((center_x, center_y - 10), "Agent 调度中心", fill='#2c3e50', font=font_normal, anchor='mm')
    draw.text((center_x, center_y + 15), "(中枢)", fill='#7f8c8d', font=font_small, anchor='mm')

    # Draw lines to center
    center = (center_x, center_y)
    trigger_centers = [
        (225, 150), (525, 150), (825, 150),
        (225, 330), (525, 330), (825, 330),
        (525, 510)
    ]

    for tc in trigger_centers:
        draw.line([tc, center], fill='#95a5a6', width=2)

    img.save(OUTPUT_DIR / 'trigger_types.png')
    print(f"Created: trigger_types.png")


def create_comparison_table_image():
    """Create comparison table image"""
    width, height = 1000, 600
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    font_title = get_font(28)
    font_normal = get_font(18)
    font_bold = get_font(20)

    # Title
    draw.text((width//2, 30), "7 种触发器对比", fill='#2c3e50', font=font_title, anchor='mm')

    # Table data
    headers = ['触发器类型', '适用场景', '配置难度', '响应速度']
    data = [
        ('关键词触发', '固定指令响应', '⭐', '⚡⚡⚡'),
        ('正则触发', '结构化参数', '⭐⭐', '⚡⚡⚡'),
        ('意图触发', '自然语言', '⭐⭐⭐', '⚡⚡'),
        ('上下文触发', '多轮对话', '⭐⭐⭐⭐', '⚡⚡'),
        ('时间触发', '定时任务', '⭐⭐', '⚡⚡⚡'),
        ('事件触发', '外部集成', '⭐⭐⭐', '⚡⚡⚡'),
        ('组合触发', '复杂条件', '⭐⭐⭐⭐⭐', '⚡'),
    ]

    # Column settings
    col_widths = [150, 300, 150, 150]
    col_x = [100, 250, 550, 700]
    row_height = 55
    y_start = 80

    # Header row
    header_y = y_start
    for i, header in enumerate(headers):
        x = col_x[i]
        draw.rectangle([x - 75, header_y, x + col_widths[i] - 75, header_y + row_height], fill='#34495e')
        draw.text((x + col_widths[i]//2 - 75, header_y + row_height//2), header, fill='white', font=font_bold, anchor='mm')

    # Data rows
    colors = ['#ecf0f1', '#ffffff']
    for i, (name, scenario, difficulty, speed) in enumerate(data):
        row_y = y_start + row_height + i * row_height
        color = colors[i % 2]

        # Row background
        draw.rectangle([50, row_y, width - 50, row_y + row_height - 5], fill=color, outline='#bdc3c7')

        # Cells
        draw.text((col_x[0], row_y + row_height//2), name, fill='#2c3e50', font=font_normal, anchor='lm')
        draw.text((col_x[1] + col_widths[1]//2, row_y + row_height//2), scenario, fill='#2c3e50', font=font_normal, anchor='mm')
        draw.text((col_x[2] + col_widths[2]//2, row_y + row_height//2), difficulty, fill='#2c3e50', font=font_normal, anchor='mm')
        draw.text((col_x[3] + col_widths[3]//2, row_y + row_height//2), speed, fill='#2c3e50', font=font_normal, anchor='mm')

    img.save(OUTPUT_DIR / 'comparison_table.png')
    print(f"Created: comparison_table.png")


def create_decision_tree_image():
    """Create simplified decision tree image"""
    width, height = 1000, 700
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    font_title = get_font(28)
    font_normal = get_font(16)

    # Title
    draw.text((width//2, 20), "触发器选择决策树", fill='#2c3e50', font=font_title, anchor='mm')

    # Simplified tree structure
    # Root
    draw.rounded_rectangle([(400, 60), (600, 110)], radius=10, fill='#3498db')
    draw.text((width//2, 85), "你的需求是什么？", fill='white', font=font_normal, anchor='mm')

    # Level 2
    level2_y = 160
    level2_items = [
        (150, '简单指令响应？', '#e74c3c'),
        (500, '需要提取参数？', '#e74c3c'),
        (850, '表达方式多样？', '#e74c3c'),
    ]

    for x, text, color in level2_items:
        draw.rounded_rectangle([(x - 100, level2_y), (x + 100, level2_y + 50)], radius=10, fill=color)
        draw.text((x, level2_y + 25), text, fill='white', font=font_normal, anchor='mm')
        draw.line([(width//2, 110), (x, level2_y)], fill='#95a5a6', width=2)

    # Level 3 - Results
    level3_y = 280
    level3_items = [
        (100, '关键词触发', '#2ecc71'),
        (200, '正则触发', '#2ecc71'),
        (450, '上下文触发', '#2ecc71'),
        (550, '时间触发', '#2ecc71'),
        (750, '意图触发', '#2ecc71'),
        (850, '组合触发', '#2ecc71'),
    ]

    for x, text, color in level3_items:
        draw.rounded_rectangle([(x - 80, level3_y), (x + 80, level3_y + 45)], radius=10, fill=color)
        draw.text((x, level3_y + 22), text, fill='white', font=font_normal, anchor='mm')

    # Connecting lines
    draw.line([(150, 210), (100, level3_y)], fill='#95a5a6', width=2)
    draw.line([(150, 210), (200, level3_y)], fill='#95a5a6', width=2)
    draw.line([(500, 210), (450, level3_y)], fill='#95a5a6', width=2)
    draw.line([(500, 210), (550, level3_y)], fill='#95a5a6', width=2)
    draw.line([(850, 210), (750, level3_y)], fill='#95a5a6', width=2)
    draw.line([(850, 210), (850, level3_y)], fill='#95a5a6', width=2)

    # Add more triggers at bottom
    level4_y = 400
    level4_items = [
        (300, '定时任务？ → 时间触发', '#f39c12'),
        (500, '响应外部事件？ → 事件触发', '#f39c12'),
        (700, '复杂业务逻辑？ → 组合触发', '#f39c12'),
    ]

    for x, text, color in level4_items:
        draw.rounded_rectangle([(x - 130, level4_y), (x + 130, level4_y + 45)], radius=10, fill=color)
        draw.text((x, level4_y + 22), text, fill='white', font=font_normal, anchor='mm')

    img.save(OUTPUT_DIR / 'decision_tree.png')
    print(f"Created: decision_tree.png")


if __name__ == '__main__':
    create_trigger_types_image()
    create_comparison_table_image()
    create_decision_tree_image()
    print("\nAll images created successfully!")

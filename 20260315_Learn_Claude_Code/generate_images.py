#!/usr/bin/env python3
"""生成文章配图"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建输出目录
output_dir = "/Users/wp931120/lobsterai/project/wp_work/20260315_Learn_Claude_Code/images"
os.makedirs(output_dir, exist_ok=True)

# 颜色方案
BG_COLOR = "#1a1a2e"
ACCENT_COLOR = "#00d9ff"
SECONDARY_COLOR = "#7b2cbf"
TEXT_COLOR = "#ffffff"
MUTED_COLOR = "#6c757d"

def get_font(size, bold=False):
    """获取字体"""
    font_names = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for font_name in font_names:
        if os.path.exists(font_name):
            try:
                return ImageFont.truetype(font_name, size)
            except:
                continue
    return ImageFont.load_default()

def draw_agent_loop():
    """绘制 Agent 循环概念图"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_large = get_font(36)
    font_medium = get_font(24)
    font_small = get_font(18)

    # 标题
    draw.text((width//2, 50), "Agent Loop", font=font_large, fill=ACCENT_COLOR, anchor="mt")

    # 中心圆 - LLM
    center_x, center_y = width//2, height//2
    radius = 100

    # 绘制中心圆
    draw.ellipse([center_x-radius, center_y-radius, center_x+radius, center_y+radius],
                 outline=ACCENT_COLOR, width=3)
    draw.text((center_x, center_y-15), "LLM", font=font_medium, fill=TEXT_COLOR, anchor="mm")
    draw.text((center_x, center_y+15), "模型", font=font_small, fill=MUTED_COLOR, anchor="mm")

    # 外部节点
    nodes = [
        ("messages[]", "消息队列", (center_x, center_y - 250)),
        ("Tool Use", "工具调用", (center_x + 280, center_y)),
        ("Tool Result", "工具结果", (center_x, center_y + 250)),
        ("Response", "响应", (center_x - 280, center_y)),
    ]

    node_radius = 60
    for name, desc, (x, y) in nodes:
        draw.ellipse([x-node_radius, y-node_radius, x+node_radius, y+node_radius],
                     outline=SECONDARY_COLOR, width=2)
        draw.text((x, y-10), name, font=font_small, fill=TEXT_COLOR, anchor="mm")
        draw.text((x, y+15), desc, font=font_small, fill=MUTED_COLOR, anchor="mm")

    # 绘制连接箭头
    arrow_color = ACCENT_COLOR
    # 上到右
    draw.line([(center_x, center_y - 250 + node_radius), (center_x + 50, center_y - 150)], fill=arrow_color, width=2)
    draw.line([(center_x + 50, center_y - 150), (center_x + 220, center_y - 50)], fill=arrow_color, width=2)

    # 右到下
    draw.line([(center_x + 220, center_y + 50), (center_x + 50, center_y + 150)], fill=arrow_color, width=2)
    draw.line([(center_x + 50, center_y + 150), (center_x, center_y + 250 - node_radius)], fill=arrow_color, width=2)

    # 下到左
    draw.line([(center_x, center_y + 250 - node_radius), (center_x - 50, center_y + 150)], fill=arrow_color, width=2)
    draw.line([(center_x - 50, center_y + 150), (center_x - 220, center_y + 50)], fill=arrow_color, width=2)

    # 左到上
    draw.line([(center_x - 220, center_y - 50), (center_x - 50, center_y - 150)], fill=arrow_color, width=2)
    draw.line([(center_x - 50, center_y - 150), (center_x, center_y - 250 + node_radius)], fill=arrow_color, width=2)

    # 底部说明
    draw.text((width//2, height - 50), "一个循环 + 工具 = 智能体", font=font_medium, fill=MUTED_COLOR, anchor="mm")

    # 保存
    img.save(os.path.join(output_dir, "agent_loop.png"), "PNG")
    print("生成: agent_loop.png")

def draw_evolution_stairs():
    """绘制 12 节课进化阶梯图"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_large = get_font(36)
    font_medium = get_font(20)
    font_small = get_font(16)

    # 标题
    draw.text((width//2, 40), "12 节课进化之路", font=font_large, fill=ACCENT_COLOR, anchor="mt")

    # 12 个台阶
    stages = [
        ("s01", "循环"),
        ("s02", "工具"),
        ("s03", "计划"),
        ("s04", "子智能体"),
        ("s05", "Skills"),
        ("s06", "压缩"),
        ("s07", "持久化"),
        ("s08", "后台"),
        ("s09", "团队"),
        ("s10", "协议"),
        ("s11", "自治"),
        ("s12", "隔离"),
    ]

    start_x = 80
    start_y = height - 120
    step_width = 85
    step_height = 45

    for i, (code, name) in enumerate(stages):
        x = start_x + i * step_width
        y = start_y - i * step_height

        # 颜色渐变
        ratio = i / 11
        r = int(0 + ratio * 123)
        g = int(217 - ratio * 100)
        b = int(255 - ratio * 30)
        color = f"#{r:02x}{g:02x}{b:02x}"

        # 绘制台阶
        draw.rectangle([x, y, x + step_width - 5, y + step_height], fill=color, outline=color)

        # 文字
        draw.text((x + step_width//2 - 2, y + step_height//2), code, font=font_small, fill="#1a1a2e", anchor="mm")
        draw.text((x + step_width//2 - 2, y + step_height//2 + 20), name, font=font_small, fill="#1a1a2e", anchor="mm")

    # 阶段标注
    phases = [
        ("第一阶段\n循环与工具", 0, 2),
        ("第二阶段\n规划与知识", 3, 6),
        ("第三阶段\n持久化", 7, 8),
        ("第四阶段\n团队", 9, 11),
    ]

    for name, start, end in phases:
        mid = (start + end) // 2
        x = start_x + mid * step_width + step_width // 2
        y = start_y - 11 * step_height - 80
        draw.text((x, y), name, font=font_medium, fill=MUTED_COLOR, anchor="mm")

    # 底部说明
    draw.text((width//2, height - 40), "每节课只加一个机制，像搭积木一样", font=font_medium, fill=MUTED_COLOR, anchor="mm")

    # 保存
    img.save(os.path.join(output_dir, "evolution_stairs.png"), "PNG")
    print("生成: evolution_stairs.png")

def draw_agent_team():
    """绘制多 Agent 协作图"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_large = get_font(36)
    font_medium = get_font(20)
    font_small = get_font(16)

    # 标题
    draw.text((width//2, 40), "多 Agent 协作", font=font_large, fill=ACCENT_COLOR, anchor="mt")

    # 主 Agent
    main_x, main_y = width//2, 200
    draw.ellipse([main_x-80, main_y-50, main_x+80, main_y+50], outline=ACCENT_COLOR, width=3)
    draw.text((main_x, main_y-10), "主 Agent", font=font_medium, fill=TEXT_COLOR, anchor="mm")
    draw.text((main_x, main_y+15), "项目经理", font=font_small, fill=MUTED_COLOR, anchor="mm")

    # 任务板
    board_x, board_y = width//2, 400
    draw.rectangle([board_x-100, board_y-40, board_x+100, board_y+40], outline=SECONDARY_COLOR, width=2)
    draw.text((board_x, board_y), "任务板", font=font_medium, fill=TEXT_COLOR, anchor="mm")

    # 子 Agent 们
    agents = [
        ("前端 Agent", (200, 600)),
        ("后端 Agent", (500, 600)),
        ("测试 Agent", (700, 600)),
        ("部署 Agent", (1000, 600)),
    ]

    for name, (x, y) in agents:
        draw.ellipse([x-70, y-40, x+70, y+40], outline=ACCENT_COLOR, width=2)
        draw.text((x, y), name, font=font_small, fill=TEXT_COLOR, anchor="mm")

        # 连接到任务板
        draw.line([(x, y-40), (board_x, board_y+40)], fill=MUTED_COLOR, width=1)

    # 主 Agent 到任务板
    draw.line([(main_x, main_y+50), (board_x, board_y-40)], fill=ACCENT_COLOR, width=2)

    # 底部说明
    draw.text((width//2, height - 40), "队友自己看任务板，有活就认领", font=font_medium, fill=MUTED_COLOR, anchor="mm")

    # 保存
    img.save(os.path.join(output_dir, "agent_team.png"), "PNG")
    print("生成: agent_team.png")

if __name__ == "__main__":
    print("开始生成配图...")
    draw_agent_loop()
    draw_evolution_stairs()
    draw_agent_team()
    print("配图生成完成!")
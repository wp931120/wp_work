#!/usr/bin/env python3
"""
OpenClaw AI 代理革命文章配图生成脚本
生成三张深色科技风格配图
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配置
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH = 1200
HEIGHT = 675  # 16:9 比例
BG_COLOR = "#0a0e1a"  # 深蓝黑色背景
PRIMARY_COLOR = "#00d4ff"  # 青色
SECONDARY_COLOR = "#7b2fff"  # 紫色
ACCENT_COLOR = "#ff6b35"  # 橙色
TEXT_COLOR = "#ffffff"
GRID_COLOR = "#1a2332"

def get_font(size=40):
    """获取字体"""
    # 尝试常见中文字体路径
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
        "/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

    # 回退到默认字体
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def draw_grid(draw, width, height, spacing=50):
    """绘制网格背景"""
    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=GRID_COLOR, width=1)
    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=GRID_COLOR, width=1)

def draw_agent_network(draw, width, height):
    """绘制代理网络图"""
    import math

    # 中心节点
    center_x, center_y = width // 2, height // 2

    # 绘制连接线
    nodes = []
    for i in range(10):
        angle = (i / 10) * 2 * math.pi
        radius = 200
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius
        nodes.append((x, y))

        # 连接到中心
        draw.line([(center_x, center_y), (x, y)], fill=PRIMARY_COLOR, width=2)

    # 绘制节点
    for i, (x, y) in enumerate(nodes):
        # 外圈
        draw.ellipse([x-15, y-15, x+15, y+15], fill=BG_COLOR, outline=PRIMARY_COLOR, width=3)
        # 内圈
        draw.ellipse([x-8, y-8, x+8, y+8], fill=PRIMARY_COLOR)

    # 中心节点
    draw.ellipse([center_x-30, center_y-30, center_x+30, center_y+30],
                 fill=SECONDARY_COLOR, outline=PRIMARY_COLOR, width=3)

    # 添加标签
    font = get_font(20)
    labels = ["调研", "内容", "客服", "数据", "财务", "运营", "营销", "开发", "运维", "人事"]
    for i, (x, y) in enumerate(nodes):
        label = labels[i % len(labels)]
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text((x - text_w/2, y - 35), label, fill=TEXT_COLOR, font=font)

def draw_workflow_diagram(draw, width, height):
    """绘制工作流架构图"""

    # 绘制 OpenClaw 框
    oc_x, oc_y = 150, height // 2 - 100
    draw.rounded_rectangle([oc_x, oc_y, oc_x + 250, oc_y + 200],
                          radius=15, fill="#1a1f3a", outline=PRIMARY_COLOR, width=3)

    # 绘制 n8n 框
    n8n_x, n8n_y = width - 400, height // 2 - 100
    draw.rounded_rectangle([n8n_x, n8n_y, n8n_x + 250, n8n_y + 200],
                          radius=15, fill="#1a1f3a", outline=SECONDARY_COLOR, width=3)

    # 绘制连接箭头
    arrow_start = oc_x + 250
    arrow_end = n8n_x
    arrow_y = height // 2
    draw.line([(arrow_start, arrow_y), (arrow_end, arrow_y)],
              fill=ACCENT_COLOR, width=4)
    # 箭头
    draw.polygon([(arrow_end-10, arrow_y-10), (arrow_end-10, arrow_y+10),
                  (arrow_end, arrow_y)], fill=ACCENT_COLOR)

    # 添加文字
    font_large = get_font(36)
    font_small = get_font(20)

    # OpenClaw 文字
    draw.text((oc_x + 125, oc_y + 70), "OpenClaw", fill=TEXT_COLOR,
              font=font_large, anchor="mm")
    draw.text((oc_x + 125, oc_y + 120), "代理执行层", fill=PRIMARY_COLOR,
              font=font_small, anchor="mm")

    # n8n 文字
    draw.text((n8n_x + 125, n8n_y + 70), "n8n", fill=TEXT_COLOR,
              font=font_large, anchor="mm")
    draw.text((n8n_x + 125, n8n_y + 120), "流程编排层", fill=SECONDARY_COLOR,
              font=font_small, anchor="mm")

    # Webhook 标签
    draw.text((width // 2, arrow_y - 20), "Webhook", fill=ACCENT_COLOR,
              font=font_small, anchor="mm")

def draw_pyramid(draw, width, height):
    """绘制自动化成熟度金字塔"""

    levels = [
        ("手动操作", "#ff6b35", "基础"),
        ("规则自动化", "#ff9f43", "进阶"),
        ("AI 辅助", "#00d4ff", "高级"),
        ("自主代理", "#7b2fff", "专家"),
    ]

    pyramid_base = height * 0.85
    pyramid_height = height * 0.6
    pyramid_center = width // 2

    for i, (label, color, level_name) in enumerate(levels):
        # 计算当前层的宽度
        progress = (i + 1) / len(levels)
        layer_width = pyramid_base * progress * 0.6
        layer_height = pyramid_height / len(levels)
        y_start = pyramid_base - (i + 1) * layer_height

        # 绘制层
        x_left = pyramid_center - layer_width / 2
        x_right = pyramid_center + layer_width / 2

        draw.polygon([
            (pyramid_center, y_start),
            (x_left, y_start + layer_height),
            (x_right, y_start + layer_height)
        ], fill=color, outline="#ffffff", width=2)

        # 添加文字
        font = get_font(24)
        draw.text((pyramid_center, y_start + layer_height/2 - 5),
                 f"L{i+1}: {label}", fill="#ffffff",
                 font=font, anchor="mm")

    # 标题
    font_title = get_font(36)
    draw.text((width // 2, 80), "自动化成熟度模型", fill=TEXT_COLOR,
              font=font_title, anchor="mm")

def create_image(title_text, draw_func, filename):
    """创建图片"""
    print(f"开始生成：{filename}")

    # 创建画布
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 绘制网格
    draw_grid(draw, WIDTH, HEIGHT)

    # 绘制主图
    draw_func(draw, WIDTH, HEIGHT)

    # 添加标题
    font_title = get_font(42)
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text((WIDTH // 2, 30), title_text, fill=TEXT_COLOR,
              font=font_title, anchor="mm")

    # 保存
    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 已生成：{filename}")

    return output_path

def main():
    print("开始生成配图...")

    # 图片 1: 代理网络图
    create_image(
        "OpenClaw 代理网络架构",
        draw_agent_network,
        "001_agent_network.png"
    )

    # 图片 2: 工作流架构图
    create_image(
        "OpenClaw + n8n 黄金组合",
        draw_workflow_diagram,
        "002_workflow_architecture.png"
    )

    # 图片 3: 自动化成熟度金字塔
    create_image(
        "企业自动化成熟度模型",
        draw_pyramid,
        "003_maturity_pyramid.png"
    )

    print(f"\n🎉 所有图片已保存到：{OUTPUT_DIR}")

if __name__ == "__main__":
    main()

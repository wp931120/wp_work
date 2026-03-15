#!/usr/bin/env python3
"""生成 gstack 文章配图"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "/Users/wp931120/lobsterai/project/wp_work/20260315_gstack"

def get_font(size=24):
    """获取字体，优先使用系统字体"""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

def create_image1():
    """图 1: 8 种认知模式示意图"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), '#1a1a2e')
    draw = ImageDraw.Draw(img)

    # 标题
    font_large = get_font(36)
    font_medium = get_font(20)

    title = "gstack: 8 种认知模式"
    draw.text((width//2 - 140, 40), title, fill='#ffffff', font=font_large)

    # 中心圆（程序员）
    center_x, center_y = width//2, height//2
    draw.ellipse([center_x-60, center_y-60, center_x+60, center_y+60],
                 fill='#4a4a6a', outline='#6a6a8a', width=3)
    draw.text((center_x-40, center_y-10), "Coder", fill='#ffffff', font=font_medium)

    # 8 个模式的位置和颜色
    modes = [
        (center_x, center_y-180, "#e74c3c", "/plan-ceo-review", "CEO"),
        (center_x+150, center_y-130, "#e67e22", "/plan-eng-review", "Tech Lead"),
        (center_x+180, center_y, "#f1c40f", "/review", "Reviewer"),
        (center_x+150, center_y+130, "#2ecc71", "/ship", "Shipper"),
        (center_x, center_y+180, "#1abc9c", "/qa", "QA Lead"),
        (center_x-150, center_y+130, "#3498db", "/browse", "QA Bot"),
        (center_x-180, center_y, "#9b59b6", "/setup-cookies", "Session"),
        (center_x-150, center_y-130, "#e91e63", "/retro", "Manager"),
    ]

    # 画连接线和模式圆
    for cx, cy, color, cmd, role in modes:
        # 连接线
        draw.line([(center_x, center_y), (cx, cy)], fill='#4a4a6a', width=2)
        # 模式圆
        r = 50
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color + '33',
                    outline=color, width=2)
        # 文字
        draw.text((cx-35, cy-15), role, fill='#ffffff', font=font_medium)

    # 保存
    output_path = os.path.join(OUTPUT_DIR, "image1.png")
    img.save(output_path)
    print(f"Image 1 saved: {output_path}")
    return output_path

def create_image2():
    """图 2: 浏览器自动化架构图"""
    width, height = 1200, 700
    img = Image.new('RGB', (width, height), '#0d1117')
    draw = ImageDraw.Draw(img)

    font_large = get_font(32)
    font_medium = get_font(18)
    font_small = get_font(14)

    title = "gstack 浏览器自动化架构"
    draw.text((width//2 - 180, 30), title, fill='#58a6ff', font=font_large)

    # 三个主要模块
    modules = [
        (100, 200, 350, 450, '#161b22', '#30363d', "Claude Code",
         "• browse goto URL\n• click @e3\n• screenshot\n• scroll"),
        (450, 200, 750, 450, '#161b22', '#238636', "gstack CLI",
         "• HTTP Server\n• localhost:rand\n• Bearer token\n• 100-200ms"),
        (850, 200, 1100, 450, '#161b22', '#1f6feb', "Playwright",
         "• Chromium 无头\n• 持久守护进程\n• ariaSnapshot\n• ref 选择器"),
    ]

    # 画模块框
    for x1, y1, x2, y2, bg, border, title_text, content in modules:
        # 背景框
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10,
                               fill=bg, outline=border, width=3)
        # 标题
        draw.text((x1+20, y1+15), title_text, fill='#ffffff', font=font_medium)
        # 内容
        lines = content.split('\n')
        for i, line in enumerate(lines):
            draw.text((x1+20, y1+50+i*25), line, fill='#8b949e', font=font_small)

    # 箭头
    arrow_y = 325
    # 箭头 1: Claude Code -> gstack CLI
    draw.line([(450, arrow_y), (480, arrow_y)], fill='#238636', width=3)
    draw.polygon([(480, arrow_y-8), (480, arrow_y+8), (500, arrow_y)],
                 fill='#238636')
    # 箭头 2: gstack CLI -> Playwright
    draw.line([(750, arrow_y), (850, arrow_y)], fill='#1f6feb', width=3)
    draw.polygon([(850, arrow_y-8), (850, arrow_y+8), (870, arrow_y)],
                 fill='#1f6feb')

    # 底部说明
    footer_y = 520
    draw.text((width//2 - 200, footer_y), "关键优势：0 token 开销，100-200ms 响应",
              fill='#7d8590', font=font_medium)

    # 性能对比表格
    table_y = 570
    table_data = [
        ("工具", "首次调用", "后续调用", "上下文开销"),
        ("Chrome MCP", "~5s", "~2-5s", "~2000 tokens"),
        ("gstack browse", "~3s", "~100-200ms", "0 tokens"),
    ]

    col_widths = [200, 150, 150, 200]
    row_height = 35
    start_x = (width - sum(col_widths)) // 2

    for row_idx, row in enumerate(table_data):
        y = table_y + row_idx * row_height
        is_header = row_idx == 0
        for col_idx, cell in enumerate(row):
            x = start_x + sum(col_widths[:col_idx])
            color = '#58a6ff' if is_header else '#c9d1d9'
            font = font_medium if is_header else font_small
            draw.text((x+10, y+8), cell, fill=color, font=font)
        # 分隔线
        if row_idx > 0:
            draw.line([(start_x, y), (start_x+sum(col_widths), y)],
                     fill='#30363d', width=1)

    # 保存
    output_path = os.path.join(OUTPUT_DIR, "image2.png")
    img.save(output_path)
    print(f"Image 2 saved: {output_path}")
    return output_path

if __name__ == "__main__":
    create_image1()
    create_image2()
    print("Done!")

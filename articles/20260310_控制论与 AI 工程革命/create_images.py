#!/usr/bin/env python3
"""
控制论与 AI 工程革命 - 配图生成脚本
生成三张深色科技风格的配图
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配置
OUTPUT_DIR = "/Users/wp931120/lobsterai/project/wp_work/articles/20260310_控制论与 AI 工程革命"
WIDTH = 1200
HEIGHT = 675  # 16:9 比例
BG_COLOR = (10, 15, 30)  # 深蓝黑色背景

# 配色方案
COLORS = {
    'primary': (0, 188, 255),      # 青色
    'secondary': (255, 0, 128),    # 洋红色
    'accent': (255, 165, 0),       # 橙色
    'text': (255, 255, 255),       # 白色
    'text_dim': (180, 180, 180),   # 浅灰色
    'steam': (100, 100, 120),      # 蒸汽机灰色
    'k8s': (50, 100, 200),         # K8s 蓝色
    'ai': (138, 43, 226),          # AI 紫色
}

def get_font(size=40):
    """获取字体（优先使用系统字体）"""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

def create_base_image():
    """创建基础画布"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    return img, draw

def add_title(draw, title, subtitle, y_offset=80):
    """添加标题"""
    font_large = get_font(56)
    font_medium = get_font(32)

    # 标题
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    x = (WIDTH - title_width) // 2
    draw.text((x, y_offset), title, fill=COLORS['primary'], font=font_large)

    # 副标题
    if subtitle:
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
        sub_width = sub_bbox[2] - sub_bbox[0]
        x = (WIDTH - sub_width) // 2
        draw.text((x, y_offset + 70), subtitle, fill=COLORS['text_dim'], font=font_medium)

def draw_cybernetics_loop(draw, cx, cy, radius=150):
    """绘制控制论反馈回路"""
    # 外环（渐变效果）
    for i in range(8, 0, -1):
        alpha = int(80 * (i / 8))
        color = (*COLORS['primary'][:3], alpha)
        draw.ellipse(
            [cx - radius - i*3, cy - radius - i*3,
             cx + radius + i*3, cy + radius + i*3],
            outline=color,
            width=2
        )

    # 主圆环
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        outline=COLORS['primary'],
        width=4
    )

    # 箭头（表示循环）
    arrow_x = cx + radius * 0.7
    arrow_y = cy - radius * 0.7
    draw.polygon([
        (arrow_x, arrow_y - 15),
        (arrow_x + 20, arrow_y + 10),
        (arrow_x - 10, arrow_y + 5)
    ], fill=COLORS['secondary'])

def image_001():
    """图 001：三次控制论革命 - 蒸汽机/K8s/AI 的演进"""
    img, draw = create_base_image()

    # 标题
    font_title = get_font(48)
    title = "控制论的三次革命"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    x = (WIDTH - title_width) // 2
    draw.text((x, 50), title, fill=COLORS['primary'], font=font_title)

    # 三个时代的图标和说明
    eras = [
        {
            'name': '1780s 蒸汽机',
            'icon': '⚙️',
            'color': COLORS['steam'],
            'desc': '离心调速器\n从手动阀门到自动调节',
            'x': 200
        },
        {
            'name': '2010s Kubernetes',
            'icon': '☸️',
            'color': COLORS['k8s'],
            'desc': '声明式 API\n从重启服务到编写规范',
            'x': 600
        },
        {
            'name': '2020s AI Agent',
            'icon': '🤖',
            'color': COLORS['ai'],
            'desc': 'Harness Engineering\n从手写代码到设计环境',
            'x': 1000
        }
    ]

    # 绘制时间线
    draw.line([(150, 350), (1050, 350)], fill=COLORS['text_dim'], width=3)

    # 绘制每个时代
    font_icon = get_font(80)
    font_name = get_font(28)
    font_desc = get_font(24)

    for era in eras:
        x = era['x']

        # 图标背景圆
        draw.ellipse([x-60, 290, x+60, 350], fill=(*era['color'], 60), outline=era['color'], width=3)

        # 图标
        draw.text((x-30, 305), era['icon'], fill=COLORS['text'], font=font_icon)

        # 名称
        name_bbox = draw.textbbox((0, 0), era['name'], font=font_name)
        name_width = name_bbox[2] - name_bbox[0]
        draw.text((x - name_width//2, 380), era['name'], fill=era['color'], font=font_name)

        # 描述
        desc_lines = era['desc'].split('\n')
        for i, line in enumerate(desc_lines):
            line_bbox = draw.textbbox((0, 0), line, font=font_desc)
            line_width = line_bbox[2] - line_bbox[0]
            draw.text((x - line_width//2, 430 + i*35), line, fill=COLORS['text_dim'], font=font_desc)

    # 底部金句
    quote = "你不再转动阀门 · 你学会掌舵"
    quote_font = get_font(36)
    quote_bbox = draw.textbbox((0, 0), quote, font=quote_font)
    quote_width = quote_bbox[2] - quote_bbox[0]
    draw.text(((WIDTH - quote_width)//2, 580), quote, fill=COLORS['accent'], font=quote_font)

    # 保存
    img.save(os.path.join(OUTPUT_DIR, "001_three_revolutions.png"))
    print("✅ 已生成：001_three_revolutions.png")

def image_002():
    """图 002：反馈回路的层级 - 从底层到架构层"""
    img, draw = create_base_image()

    # 标题
    add_title(draw, "反馈回路的层级", "从机械检查到架构决策", y_offset=60)

    # 四个层级（金字塔结构）
    levels = [
        {
            'name': '架构层',
            'questions': '这个抽象是否正确？',
            'color': COLORS['ai'],
            'y': 180,
            'width': 400,
            'height': 100,
            'agent': '✓ LLM 可操作'
        },
        {
            'name': '设计层',
            'questions': '是否符合架构模式？',
            'color': COLORS['k8s'],
            'y': 300,
            'width': 500,
            'height': 90,
            'agent': '✓ LLM 可操作'
        },
        {
            'name': '行为层',
            'questions': '是否通过测试？',
            'color': COLORS['secondary'],
            'y': 410,
            'width': 600,
            'height': 80,
            'agent': '✓ 测试套件'
        },
        {
            'name': '语法层',
            'questions': '是否能编译？',
            'color': COLORS['primary'],
            'y': 510,
            'width': 700,
            'height': 70,
            'agent': '✓ 编译器/Linter'
        }
    ]

    # 绘制层级
    font_name = get_font(32)
    font_question = get_font(24)
    font_agent = get_font(22)

    for level in levels:
        x = (WIDTH - level['width']) // 2

        # 层级矩形
        draw.rounded_rectangle(
            [x, level['y'], x + level['width'], level['y'] + level['height']],
            radius=10,
            outline=level['color'],
            width=3
        )

        # 渐变填充
        for i in range(5):
            alpha = int(40 * (5-i) / 5)
            inner_y = level['y'] + i*15
            inner_height = level['height'] - i*30
            if inner_height > 0:
                draw.rounded_rectangle(
                    [x + i*15, inner_y, x + level['width'] - i*15, inner_y + inner_height],
                    radius=8,
                    outline=(*level['color'][:3], alpha),
                    width=1
                )

        # 文字
        name_bbox = draw.textbbox((0, 0), level['name'], font=font_name)
        name_width = name_bbox[2] - name_bbox[0]
        draw.text((x + (level['width'] - name_width)//2, level['y'] + 15),
                 level['name'], fill=level['color'], font=font_name)

        q_bbox = draw.textbbox((0, 0), level['questions'], font=font_question)
        q_width = q_bbox[2] - q_bbox[0]
        draw.text((x + (level['width'] - q_width)//2, level['y'] + 55),
                 level['questions'], fill=COLORS['text_dim'], font=font_question)

        # Agent 能力标记
        agent_bbox = draw.textbbox((0, 0), level['agent'], font=font_agent)
        draw.text((x + level['width'] - agent_bbox[2] - 20, level['y'] + 15),
                 level['agent'], fill=COLORS['accent'], font=font_agent)

    # 保存
    img.save(os.path.join(OUTPUT_DIR, "002_feedback_loop_levels.png"))
    print("✅ 已生成：002_feedback_loop_levels.png")

def image_003():
    """图 003：校准前后对比"""
    img, draw = create_base_image()

    # 标题
    add_title(draw, "校准的力量", "让你的判断变成机器可读", y_offset=60)

    # 左右对比
    # 左侧：未校准
    left_x = 150
    draw.rounded_rectangle([left_x, 180, left_x + 400, 500], radius=15,
                          outline=COLORS['secondary'], width=3)

    font_header = get_font(36)
    font_text = get_font(26)
    font_big = get_font(48)

    # 左侧标题
    draw.text((left_x + 50, 200), "❌ 未校准", fill=COLORS['secondary'], font=font_header)

    # 左侧问题列表
    problems = [
        "• Agent 不理解代码库",
        "• 重复犯同样的错误",
        "• 需要人工反复审查",
        "• 质量逐渐下降"
    ]
    for i, problem in enumerate(problems):
        draw.text((left_x + 40, 270 + i*50), problem, fill=COLORS['text_dim'], font=font_text)

    # 右侧：已校准
    right_x = 650
    draw.rounded_rectangle([right_x, 180, right_x + 400, 500], radius=15,
                          outline=COLORS['primary'], width=3)

    draw.text((right_x + 50, 200), "✓ 已校准", fill=COLORS['primary'], font=font_header)

    # 右侧优势列表
    benefits = [
        "• 架构文档机器可读",
        "• 自定义 Linter 编码品味",
        "• 自动反馈快速修复",
        "• 质量持续提升"
    ]
    for i, benefit in enumerate(benefits):
        draw.text((right_x + 40, 270 + i*50), benefit, fill=COLORS['text_dim'], font=font_text)

    # 底部核心观点
    quote_bg = (30, 30, 50)
    draw.rounded_rectangle([100, 540, WIDTH-100, 640], radius=10, fill=quote_bg)

    quote = "实践没有变，忽视它们的代价变得无法承受"
    quote_font = get_font(32)
    quote_bbox = draw.textbbox((0, 0), quote, font=quote_font)
    quote_width = quote_bbox[2] - quote_bbox[0]
    draw.text(((WIDTH - quote_width)//2, 575), quote, fill=COLORS['accent'], font=quote_font)

    # 保存
    img.save(os.path.join(OUTPUT_DIR, "003_calibration_comparison.png"))
    print("✅ 已生成：003_calibration_comparison.png")

def main():
    print("开始生成配图...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    image_001()
    image_002()
    image_003()

    print(f"\n🎉 所有图片已保存到：{OUTPUT_DIR}")

if __name__ == "__main__":
    main()

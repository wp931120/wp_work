#!/usr/bin/env python3
"""
Harrison Chase EPD 文章配图生成脚本
使用 Pillow 绘制，深色科技风格
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 配色方案（深色科技风）
COLORS = {
    'bg': '#0D1117',
    'card': '#161B22',
    'card_light': '#21262D',
    'border': '#30363D',
    'accent_blue': '#58A6FF',
    'accent_green': '#3FB950',
    'accent_purple': '#A371F7',
    'accent_orange': '#F0883E',
    'text_primary': '#F0F6FC',
    'text_secondary': '#8B949E',
    'danger': '#F85149',
    'warning': '#D29922',
}

def get_font(size=24, bold=False):
    """获取字体"""
    # 尝试系统字体
    font_paths = [
        '/System/Library/Fonts/Supplemental/Arial Unicode MS.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/dejavu/DejaVuSans.ttf',
    ]

    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    # 回退到默认字体
    return ImageFont.load_default()

def create_workflow_comparison():
    """图 1：传统 EPD 工作流 vs AI 时代工作流"""
    width, height = 1600, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    font_title = get_font(32, bold=True)
    font_subtitle = get_font(24, bold=True)
    font_text = get_font(20)
    font_small = get_font(16)

    # 标题
    title = "EPD 工作流的范式转移"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) / 2, 40), title, font=font_title, fill=COLORS['text_primary'])

    # ========== 左侧：传统流程 ==========
    left_title = "传统流程（Pre-Claude 时代）"
    draw.text((200, 120), left_title, font=font_subtitle, fill=COLORS['accent_orange'])

    # 传统流程步骤
    steps_old = [
        ('产品想法', COLORS['accent_orange']),
        ('PRD 文档', COLORS['accent_orange']),
        ('设计 Mock', COLORS['accent_purple']),
        ('工程实现', COLORS['accent_blue']),
        ('上线', COLORS['accent_green']),
    ]

    y_start = 200
    y_step = 100

    for i, (label, color) in enumerate(steps_old):
        y = y_start + i * y_step
        x = 100

        # 步骤框
        draw.rectangle([x, y, x + 400, y + 60], outline=color, width=3, fill=COLORS['card'])

        # 文字
        text_bbox = draw.textbbox((0, 0), label, font=font_text)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((x + 200 - text_width/2, y + 15), label, font=font_text, fill=COLORS['text_primary'])

        # 箭头（除了最后一个）
        if i < len(steps_old) - 1:
            arrow_y = y + 70
            draw.line([(200, arrow_y), (200, arrow_y + 20)], fill=COLORS['text_secondary'], width=3)
            # 箭头头部
            draw.polygon([(190, arrow_y + 20), (210, arrow_y + 20), (200, arrow_y + 30)], fill=COLORS['text_secondary'])

    # 时间标注
    draw.text((200, y_start + len(steps_old) * y_step + 20), "周期：2-4 周",
             font=font_subtitle, fill=COLORS['danger'])

    # ========== 右侧：AI 时代流程 ==========
    right_title = "AI 时代工作流"
    draw.text((1100, 120), right_title, font=font_subtitle, fill=COLORS['accent_green'])

    # AI 时代流程步骤
    steps_new = [
        ('产品想法', COLORS['accent_orange']),
        ('Prompt', COLORS['accent_purple']),
        ('Coding Agent', COLORS['accent_blue']),
        ('原型 → 上线', COLORS['accent_green']),
    ]

    y_start_right = 200
    y_step_right = 120

    for i, (label, color) in enumerate(steps_new):
        y = y_start_right + i * y_step_right
        x = 900

        # 步骤框
        draw.rectangle([x, y, x + 400, y + 60], outline=color, width=3, fill=COLORS['card'])

        # 文字
        text_bbox = draw.textbbox((0, 0), label, font=font_text)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((x + 200 - text_width/2, y + 15), label, font=font_text, fill=COLORS['text_primary'])

        # 箭头（除了最后一个）
        if i < len(steps_new) - 1:
            arrow_y = y + 70
            draw.line([(1100, arrow_y), (1100, arrow_y + 40)], fill=COLORS['text_secondary'], width=3)
            # 箭头头部
            draw.polygon([(1090, arrow_y + 40), (1110, arrow_y + 40), (1100, arrow_y + 55)], fill=COLORS['text_secondary'])

    # 时间标注
    draw.text((1100, y_start_right + len(steps_new) * y_step_right), "周期：1-2 天",
             font=font_subtitle, fill=COLORS['accent_green'])

    # 中间对比箭头
    draw.line([(750, 400), (850, 400)], fill=COLORS['accent_blue'], width=3)
    draw.polygon([(840, 390), (850, 400), (840, 410)], fill=COLORS['accent_blue'])
    draw.text((750, 360), "范式转移", font=font_small, fill=COLORS['accent_blue'])

    # 保存
    img.save('workflow-comparison.png')
    print('✓ workflow-comparison.png 已生成')

def create_bottleneck_shift():
    """图 2：瓶颈转移示意图"""
    width, height = 1400, 800
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    font_title = get_font(30, bold=True)
    font_subtitle = get_font(24, bold=True)
    font_text = get_font(22)
    font_small = get_font(18)

    # 标题
    title = "瓶颈转移：从实现到 Review"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) / 2, 40), title, font=font_title, fill=COLORS['text_primary'])

    # ========== 左侧：传统模式 ==========
    draw.text((350, 120), "传统模式", font=font_subtitle, fill=COLORS['accent_orange'])

    # 实现部分（大瓶颈）
    draw.rectangle([150, 200, 550, 450], fill=COLORS['accent_orange'] + '4D', outline=COLORS['accent_orange'], width=2)
    draw.text((350, 280), "实现", font=font_title, fill=COLORS['accent_orange'])
    draw.text((350, 330), "瓶颈", font=font_text, fill=COLORS['text_secondary'])

    # Review 部分（小）
    draw.rectangle([150, 500, 550, 620], fill=COLORS['accent_blue'] + '33', outline=COLORS['accent_blue'], width=2)
    draw.text((350, 540), "Review", font=font_text, fill=COLORS['accent_blue'])

    draw.text((350, 680), "并行项目：少", font=font_small, fill=COLORS['text_secondary'])

    # ========== 右侧：AI 时代模式 ==========
    draw.text((1050, 120), "AI 时代", font=font_subtitle, fill=COLORS['accent_green'])

    # 实现部分（容易）
    draw.rectangle([850, 200, 1250, 300], fill=COLORS['accent_green'] + '33', outline=COLORS['accent_green'], width=2)
    draw.text((1050, 230), "实现", font=font_text, fill=COLORS['accent_green'])
    draw.text((1050, 270), "容易", font=font_small, fill=COLORS['text_secondary'])

    # Review 部分（大瓶颈）
    draw.rectangle([850, 350, 1250, 620], fill=COLORS['danger'] + '66', outline=COLORS['danger'], width=2)
    draw.text((1050, 440), "Review", font=font_title, fill=COLORS['danger'])
    draw.text((1050, 490), "新瓶颈", font=font_text, fill=COLORS['text_secondary'])

    draw.text((1050, 680), "并行项目：爆炸式增长", font=font_small, fill=COLORS['text_secondary'])

    # 中间箭头
    draw.line([(650, 400), (750, 400)], fill=COLORS['accent_blue'], width=3)
    draw.polygon([(740, 390), (750, 400), (740, 410)], fill=COLORS['accent_blue'])
    draw.text((670, 360), "转变", font=font_small, fill=COLORS['accent_blue'])

    # 保存
    img.save('bottleneck-shift.png')
    print('✓ bottleneck-shift.png 已生成')

def create_generalist_value():
    """图 3：通才 vs 专才价值对比"""
    width, height = 1400, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    font_title = get_font(28, bold=True)
    font_subtitle = get_font(22, bold=True)
    font_text = get_font(20)
    font_small = get_font(16)
    font_quote = get_font(18)

    # 标题
    title = "通才的春天：Coding Agent 时代的能力模型"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) / 2, 30), title, font=font_title, fill=COLORS['text_primary'])

    # 副标题/引用
    quote = '"一个通才比三人团队更快——因为消除了沟通开销"'
    draw.text((700, 85), quote, font=font_quote, fill=COLORS['text_secondary'])

    # ========== 左侧：传统团队 ==========
    draw.text((350, 140), "传统团队模式", font=font_subtitle, fill=COLORS['accent_orange'])

    # 三个独立角色
    roles = [
        ('Product', COLORS['accent_orange'], 200),
        ('Design', COLORS['accent_purple'], 320),
        ('Engineering', COLORS['accent_blue'], 440),
    ]

    for label, color, y in roles:
        draw.rectangle([150, y, 550, y + 60], outline=color, width=3, fill=COLORS['card'])
        text_bbox = draw.textbbox((0, 0), label, font=font_text)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((350 - text_width/2, y + 15), label, font=font_text, fill=COLORS['text_primary'])

    # 沟通成本标注（虚线用多段线模拟）
    for i in range(0, 120, 10):
        if i % 20 == 0:
            draw.line([(580, 230+i), (580, 235+i)], fill=COLORS['danger'], width=2)
    draw.text((590, 280), "沟通\n成本", font=font_small, fill=COLORS['danger'])

    draw.text((350, 560), "周期：2-4 周", font=font_text, fill=COLORS['text_secondary'])

    # ========== 右侧：通才 + Agent ==========
    draw.text((1050, 140), "通才 + Coding Agent", font=font_subtitle, fill=COLORS['accent_green'])

    # 通才框
    draw.rectangle([850, 200, 1250, 420], outline=COLORS['accent_green'], width=3, fill=COLORS['card_light'])
    draw.text((1050, 230), "通才 Builder", font=font_subtitle, fill=COLORS['accent_green'])

    # 三个能力徽章
    badges = [
        ('P', COLORS['accent_orange'], 920),
        ('D', COLORS['accent_purple'], 1050),
        ('E', COLORS['accent_blue'], 1180),
    ]

    for label, color, x in badges:
        draw.ellipse([x-30, 280, x+30, 340], fill=color, outline=color)
        draw.text((x, 305), label, font=font_subtitle, fill='white')

    # Coding Agent 框
    draw.rectangle([850, 450, 1250, 520], outline=COLORS['accent_blue'], width=2, fill=COLORS['card'])
    draw.text((1050, 470), "Coding Agent", font=font_text, fill=COLORS['accent_blue'])

    draw.text((1050, 580), "周期：1-2 天", font=font_subtitle, fill=COLORS['accent_green'])
    draw.text((1050, 620), "10 倍速差异", font=font_text, fill=COLORS['accent_green'])

    # 底部关键洞察
    draw.rectangle([200, 700, 1200, 820], outline=COLORS['accent_purple'], width=2, fill=COLORS['card_light'])
    draw.text((700, 720), "核心洞察", font=font_subtitle, fill=COLORS['accent_purple'])
    insight = '"当代码变得极其便宜，真正的壁垒是判断力"'
    draw.text((700, 770), insight, font=font_text, fill=COLORS['text_primary'])

    # 保存
    img.save('generalist-value.png')
    print('✓ generalist-value.png 已生成')

if __name__ == '__main__':
    print('开始生成 Harrison EPD 文章配图...')
    create_workflow_comparison()
    create_bottleneck_shift()
    create_generalist_value()
    print('所有配图已生成完成！')

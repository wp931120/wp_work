#!/usr/bin/env python3
"""
为《Claude Skills 开发指南》文章生成配图
使用 Pillow 绘制深色科技风格图表
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 输出目录
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 配色方案（深色科技风）
COLORS = {
    'bg': '#0f172a',        # 深蓝背景
    'card': '#1e293b',      # 卡片背景
    'primary': '#6366f1',   # 主色（靛蓝）
    'secondary': '#8b5cf6', # 辅色（紫）
    'accent': '#06b6d4',    # 强调色（青）
    'text': '#f1f5f9',      # 主文字
    'text_muted': '#94a3b8', # 次要文字
    'success': '#10b981',   # 成功（绿）
    'warning': '#f59e0b',   # 警告（橙）
}

def get_font(size=24):
    """获取系统字体"""
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    # 回退到默认字体
    return ImageFont.load_default()

def create_skills_mcp_diagram():
    """创建 Skills 与 MCP 关系图"""
    width, height = 800, 500
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    font_title = get_font(32)
    font_text = get_font(20)
    font_small = get_font(16)

    # 标题
    title = "Skills + MCP = 完整解决方案"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 40), title, fill=COLORS['text'], font=font_title)

    # 左侧：MCP（厨房）
    mcp_x, mcp_y = 100, 150
    mcp_width, mcp_height = 250, 200

    # 卡片背景
    draw.rounded_rectangle(
        [mcp_x, mcp_y, mcp_x + mcp_width, mcp_y + mcp_height],
        radius=16,
        fill=COLORS['card'],
        outline=COLORS['primary'],
        width=2
    )

    # MCP 标题
    mcp_title = "MCP（厨房）"
    mcp_title_bbox = draw.textbbox((0, 0), mcp_title, font=font_text)
    mcp_title_width = mcp_title_bbox[2] - mcp_title_bbox[0]
    draw.text(
        ((mcp_x + mcp_width // 2) - mcp_title_width // 2, mcp_y + 20),
        mcp_title, fill=COLORS['primary'], font=font_text
    )

    # MCP 内容
    mcp_items = ["🔧 工具", "📦 数据源", "⚙️ API 服务"]
    for i, item in enumerate(mcp_items):
        y = mcp_y + 70 + i * 40
        draw.text((mcp_x + 30, y), item, fill=COLORS['text_muted'], font=font_small)

    # 右侧：Skills（菜谱）
    skills_x, skills_y = 450, 150
    skills_width, skills_height = 250, 200

    # 卡片背景
    draw.rounded_rectangle(
        [skills_x, skills_y, skills_x + skills_width, skills_y + skills_height],
        radius=16,
        fill=COLORS['card'],
        outline=COLORS['secondary'],
        width=2
    )

    # Skills 标题
    skills_title = "Skills（菜谱）"
    skills_title_bbox = draw.textbbox((0, 0), skills_title, font=font_text)
    skills_title_width = skills_title_bbox[2] - skills_title_bbox[0]
    draw.text(
        ((skills_x + skills_width // 2) - skills_title_width // 2, skills_y + 20),
        skills_title, fill=COLORS['secondary'], font=font_text
    )

    # Skills 内容
    skills_items = ["📝 Instructions", "🎯 最佳实践", "✅ 工作流"]
    for i, item in enumerate(skills_items):
        y = skills_y + 70 + i * 40
        draw.text((skills_x + 30, y), item, fill=COLORS['text_muted'], font=font_small)

    # 中间箭头
    arrow_x = mcp_x + mcp_width + 20
    arrow_y = skills_y + skills_height // 2
    draw.polygon([
        (arrow_x, arrow_y - 10),
        (arrow_x + 30, arrow_y),
        (arrow_x, arrow_y + 10),
    ], fill=COLORS['accent'])

    # 底部文字
    bottom_text = "两者配合 = 用户无需从零摸索"
    bottom_bbox = draw.textbbox((0, 0), bottom_text, font=font_text)
    bottom_width = bottom_bbox[2] - bottom_bbox[0]
    draw.text(
        ((width - bottom_width) // 2, height - 80),
        bottom_text, fill=COLORS['accent'], font=font_text
    )

    # 保存
    img.save(os.path.join(OUTPUT_DIR, "001_skills_mcp_relationship.png"))
    print(f"✅ 已生成：001_skills_mcp_relationship.png")

def create_three_layer_diagram():
    """创建三层渐进式披露图"""
    width, height = 800, 500
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    font_title = get_font(32)
    font_text = get_font(20)
    font_small = get_font(16)

    # 标题
    title = "三层渐进式披露架构"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 40), title, fill=COLORS['text'], font=font_title)

    # 三层结构
    layers = [
        {
            'title': '第一层：YAML Frontmatter',
            'desc': '总是加载 · 触发判断',
            'color': COLORS['primary'],
            'y': 120,
            'height': 100,
        },
        {
            'title': '第二层：SKILL.md 正文',
            'desc': '需要时加载 · 完整指令',
            'color': COLORS['secondary'],
            'y': 240,
            'height': 100,
        },
        {
            'title': '第三层：references/ 等',
            'desc': '按需探索 · 深度文档',
            'color': COLORS['accent'],
            'y': 360,
            'height': 100,
        },
    ]

    padding_x = 100
    layer_width = width - 2 * padding_x

    for layer in layers:
        # 卡片背景
        draw.rounded_rectangle(
            [padding_x, layer['y'], padding_x + layer_width, layer['y'] + layer['height']],
            radius=12,
            fill=COLORS['card'],
            outline=layer['color'],
            width=3
        )

        # 标题
        title_bbox = draw.textbbox((0, 0), layer['title'], font=font_text)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(
            ((width - title_width) // 2, layer['y'] + 25),
            layer['title'], fill=layer['color'], font=font_text
        )

        # 描述
        desc_bbox = draw.textbbox((0, 0), layer['desc'], font=font_small)
        desc_width = desc_bbox[2] - desc_bbox[0]
        draw.text(
            ((width - desc_width) // 2, layer['y'] + 60),
            layer['desc'], fill=COLORS['text_muted'], font=font_small
        )

    # 右侧箭头
    arrow_x = width - 60
    draw.polygon([
        (arrow_x, 200),
        (arrow_x + 20, 250),
        (arrow_x, 300),
    ], fill=COLORS['accent'])

    # 箭头旁文字
    draw.text((width - 180, 240), "按需加载\n节省 Token", fill=COLORS['text_muted'], font=font_small)

    # 保存
    img.save(os.path.join(OUTPUT_DIR, "002_three_layer_architecture.png"))
    print(f"✅ 已生成：002_three_layer_architecture.png")

def create_comparison_chart():
    """创建 Before/After 对比图"""
    width, height = 800, 500
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    font_title = get_font(32)
    font_text = get_font(20)
    font_small = get_font(16)
    font_big = get_font(28)

    # 标题
    title = "使用 Skills 效果对比"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 40), title, fill=COLORS['text'], font=font_title)

    # 左侧：Before
    before_x, before_y = 50, 100
    before_width, before_height = 320, 350

    draw.rounded_rectangle(
        [before_x, before_y, before_x + before_width, before_y + before_height],
        radius=16,
        fill=COLORS['card'],
        outline=COLORS['warning'],
        width=3
    )

    draw.text((before_x + 30, before_y + 25), "❌ Before（不用 Skill）", fill=COLORS['warning'], font=font_text)

    before_items = [
        "对话轮次：15 轮",
        "Token 消耗：12,000",
        "API 错误：3 次",
        "用户需要逐项说明",
        "每次从头解释"
    ]
    for i, item in enumerate(before_items):
        draw.text((before_x + 30, before_y + 80 + i * 45), item, fill=COLORS['text_muted'], font=font_small)

    # 右侧：After
    after_x, after_y = 430, 100
    after_width, after_height = 320, 350

    draw.rounded_rectangle(
        [after_x, after_y, after_x + after_width, after_y + after_height],
        radius=16,
        fill=COLORS['card'],
        outline=COLORS['success'],
        width=3
    )

    draw.text((after_x + 30, after_y + 25), "✅ After（用 Skill）", fill=COLORS['success'], font=font_text)

    after_items = [
        "对话轮次：2 轮",
        "Token 消耗：6,000",
        "API 错误：0 次",
        "自动执行工作流",
        "最佳实践固化"
    ]
    for i, item in enumerate(after_items):
        draw.text((after_x + 30, after_y + 80 + i * 45), item, fill=COLORS['text_muted'], font=font_small)

    # 中间箭头
    arrow_x = before_x + before_width + 10
    arrow_y = before_y + before_height // 2
    draw.polygon([
        (arrow_x, arrow_y - 15),
        (arrow_x + 40, arrow_y),
        (arrow_x, arrow_y + 15),
    ], fill=COLORS['success'])

    # 底部提升百分比
    improvements = [
        ("对话轮次", "87% ↓"),
        ("Token 消耗", "50% ↓"),
        ("API 错误", "100% ↓"),
    ]

    y = before_y + before_height + 40
    for label, value in improvements:
        label_bbox = draw.textbbox((0, 0), label, font=font_small)
        label_width = label_bbox[2] - label_bbox[0]
        draw.text((width // 2 - label_width - 20, y), label, fill=COLORS['text_muted'], font=font_small)

        value_bbox = draw.textbbox((0, 0), value, font=font_big)
        draw.text((width // 2 + 20, y - 5), value, fill=COLORS['success'], font=font_big)
        y += 35

    # 保存
    img.save(os.path.join(OUTPUT_DIR, "003_before_after_comparison.png"))
    print(f"✅ 已生成：003_before_after_comparison.png")

if __name__ == "__main__":
    print("开始生成配图...")
    create_skills_mcp_diagram()
    create_three_layer_diagram()
    create_comparison_chart()
    print(f"\n🎉 所有图片已保存到：{OUTPUT_DIR}")

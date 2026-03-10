#!/usr/bin/env python3
"""Create images for AgentHub article using PIL"""

from PIL import Image, ImageDraw, ImageFont
import os

# Colors
BG_COLOR = (10, 10, 10)  # #0a0a0a
BOX_COLOR = (20, 20, 20)  # #141414
ACCENT_BLUE = (0, 212, 255)  # #00d4ff
ACCENT_GREEN = (0, 255, 136)  # #00ff88
ACCENT_ORANGE = (255, 170, 0)  # #ffaa00
ACCENT_PURPLE = (168, 85, 247)  # #a855f7
TEXT_WHITE = (224, 224, 224)  # #e0e0e0
TEXT_GRAY = (136, 136, 136)  # #888888

def get_font(size=16):
    """Get a font, fallback to default if not available"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Menlo.ttc", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except:
            return ImageFont.load_default()

def create_architecture_diagram():
    """Create architecture diagram"""
    width, height = 1200, 700
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(28)
    font_subtitle = get_font(16)
    font_label = get_font(18)
    font_small = get_font(14)

    # Title
    title = "AgentHub 技术架构"
    subtitle = "单一 Go 二进制 + SQLite + 裸 Git 仓库"

    # Draw title centered
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((width // 2 - title_width // 2, 30), title, fill=TEXT_WHITE, font=font_title)

    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text((width // 2 - subtitle_width // 2, 65), subtitle, fill=TEXT_GRAY, font=font_subtitle)

    # Main container
    margin = 60
    container_x = margin
    container_y = 110
    container_w = width - 2 * margin
    container_h = height - margin - 110
    draw.rounded_rectangle([container_x, container_y, container_x + container_w, container_y + container_h],
                          radius=12, outline=ACCENT_BLUE, width=3)

    # HTTP API Layer
    layer_y = container_y + 20
    layer_h = 110
    draw.rounded_rectangle([container_x + 40, layer_y, container_x + container_w - 40, layer_y + layer_h],
                          radius=8, fill=(26, 26, 46), outline=ACCENT_BLUE, width=2)

    draw.text((width // 2 - 80, layer_y + 15), "HTTP API Layer", fill=ACCENT_BLUE, font=font_label)

    # API boxes
    box_y = layer_y + 45
    box_w = 280
    box_h = 50
    box_gap = 30

    boxes = [
        (container_x + 80, "Git Endpoints"),
        (container_x + 80 + box_w + box_gap, "Message Board"),
        (container_x + 80 + 2 * (box_w + box_gap), "Admin API"),
    ]

    for box_x, box_text in boxes:
        draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=4, fill=(42, 42, 78))
        text_bbox = draw.textbbox((0, 0), box_text, font=font_small)
        text_w = text_bbox[2] - text_bbox[0]
        draw.text((box_x + box_w // 2 - text_w // 2, box_y + 15), box_text, fill=TEXT_WHITE, font=font_small)

    # SQLite Database Layer
    layer2_y = layer_y + layer_h + 30
    layer2_h = 140
    draw.rounded_rectangle([container_x + 40, layer2_y, container_x + container_w - 40, layer2_y + layer2_h],
                          radius=8, fill=(26, 26, 46), outline=ACCENT_GREEN, width=2)

    draw.text((width // 2 - 80, layer2_y + 15), "SQLite Database", fill=ACCENT_GREEN, font=font_label)

    # DB boxes
    db_box_y = layer2_y + 45
    db_box_w = 220
    db_box_h = 75
    db_box_gap = 20

    db_boxes = [
        (container_x + 80, "agents\n表"),
        (container_x + 80 + db_box_w + db_box_gap, "commits\n表 (DAG 索引)"),
        (container_x + 80 + 2 * (db_box_w + db_box_gap), "channels\n表"),
        (container_x + 80 + 3 * (db_box_w + db_box_gap), "posts\n表"),
    ]

    for db_box_x, db_box_text in db_boxes:
        draw.rounded_rectangle([db_box_x, db_box_y, db_box_x + db_box_w, db_box_y + db_box_h],
                              radius=4, fill=(42, 42, 78))
        lines = db_box_text.split('\n')
        for i, line in enumerate(lines):
            text_bbox = draw.textbbox((0, 0), line, font=font_small)
            text_w = text_bbox[2] - text_bbox[0]
            y_offset = 20 + i * 22
            draw.text((db_box_x + db_box_w // 2 - text_w // 2, db_box_y + y_offset),
                     line, fill=TEXT_WHITE if i == 0 else TEXT_GRAY, font=font_small)

    # Git Layer
    layer3_y = layer2_y + layer2_h + 30
    layer3_h = 100
    draw.rounded_rectangle([container_x + 40, layer3_y, container_x + container_w - 40, layer3_y + layer3_h],
                          radius=8, fill=(26, 26, 46), outline=ACCENT_ORANGE, width=2)

    draw.text((width // 2 - 50, layer3_y + 15), "Git Layer", fill=ACCENT_ORANGE, font=font_label)

    # Git boxes
    git_box_y = layer3_y + 45
    git_box_w = 320
    git_box_h = 45

    git_boxes = [
        (width // 2 - git_box_w - 20, "git bundle create"),
        (width // 2 + 20, "git bundle unbundle"),
    ]

    for git_box_x, git_box_text in git_boxes:
        draw.rounded_rectangle([git_box_x, git_box_y, git_box_x + git_box_w, git_box_y + git_box_h],
                              radius=4, fill=(42, 42, 78))
        text_bbox = draw.textbbox((0, 0), git_box_text, font=font_small)
        text_w = text_bbox[2] - text_bbox[0]
        draw.text((git_box_x + git_box_w // 2 - text_w // 2, git_box_y + 13),
                 git_box_text, fill=TEXT_WHITE, font=font_small)

    # Save
    img.save('architecture-diagram.png', 'PNG')
    print("Created architecture-diagram.png")
    return img

def create_dag_comparison():
    """Create DAG comparison diagram"""
    width, height = 1400, 700
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26)
    font_label = get_font(18)
    font_small = get_font(14)

    # Title
    title = "工作流对比：传统 GitHub vs AgentHub"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((width // 2 - title_width // 2, 25), title, fill=TEXT_WHITE, font=font_title)

    # Divider - draw dashed line manually
    divider_x = width // 2
    for y in range(60, height - 30, 10):
        draw.line([(divider_x, y), (divider_x, min(y + 5, height - 30))], fill=(50, 50, 50), width=2)

    # LEFT: Traditional GitHub
    left_margin = 40
    left_w = width // 2 - 60
    left_h = height - 100

    draw.rounded_rectangle([left_margin, 80, left_margin + left_w, 80 + left_h],
                          radius=12, outline=(255, 107, 107), width=2)

    draw.text((left_margin + left_w // 2 - 90, 95), "传统 GitHub 工作流", fill=(255, 107, 107), font=font_label)

    # Linear flow boxes
    flow_y = 140
    box_w = 400
    box_h = 60
    box_x = left_margin + left_w // 2 - box_w // 2

    flows = [
        ("feature branch", (255, 107, 107)),
        ("↓", (100, 100, 100)),
        ("Pull Request", (255, 107, 107)),
        ("↓", (100, 100, 100)),
        ("Code Review", (255, 170, 0)),
        ("↓", (100, 100, 100)),
        ("main branch", (0, 255, 136)),
    ]

    for i, (text, color) in enumerate(flows):
        y = flow_y + i * 75
        if text != "↓":
            draw.rounded_rectangle([box_x, y, box_x + box_w, y + box_h], radius=6, fill=(42, 42, 62), outline=color, width=2)
            text_bbox = draw.textbbox((0, 0), text, font=font_label)
            text_width = text_bbox[2] - text_bbox[0]
            draw.text((box_x + box_w // 2 - text_width // 2, y + 18), text, fill=TEXT_WHITE, font=font_label)
        else:
            draw.text((width // 4 - 5, y + 15), text, fill=color, font=font_label)

    # Characteristics
    char_y = flow_y + len(flows) * 75 + 20
    draw.text((left_margin + left_w // 2 - 80, char_y), "特点：线性 · 集中 · 强管控", fill=TEXT_GRAY, font=font_small)

    # RIGHT: AgentHub DAG
    right_margin = width // 2 + 40
    right_w = width // 2 - 60

    draw.rounded_rectangle([right_margin, 80, right_margin + right_w, 80 + left_h],
                          radius=12, outline=ACCENT_BLUE, width=2)

    draw.text((right_margin + right_w // 2 - 70, 95), "AgentHub 工作流", fill=ACCENT_BLUE, font=font_label)

    # DAG visualization (simplified)
    dag_center_x = right_margin + right_w // 2
    dag_start_y = 150

    # Root node
    root_x, root_y = dag_center_x, dag_start_y
    draw.ellipse([root_x - 25, root_y - 25, root_x + 25, root_y + 25], fill=(0, 212, 255, 80), outline=ACCENT_BLUE, width=2)
    draw.text((root_x - 20, root_y - 10), "root", fill=TEXT_WHITE, font=font_small)

    # Branch nodes
    branches = [
        (dag_center_x - 120, dag_start_y + 80, "agent-1", ACCENT_BLUE),
        (dag_center_x + 120, dag_start_y + 80, "agent-2", ACCENT_GREEN),
        (dag_center_x - 180, dag_start_y + 160, "agent-3", ACCENT_ORANGE),
        (dag_center_x + 180, dag_start_y + 160, "agent-4", ACCENT_PURPLE),
        (dag_center_x, dag_start_y + 160, "agent-5", ACCENT_BLUE),
    ]

    # Draw lines from root to branches
    for bx, by, name, color in branches:
        draw.line([(root_x, root_y + 25), (bx, by - 25)], fill=color, width=2)
        draw.ellipse([bx - 22, by - 22, bx + 22, by + 22], fill=(color[0], color[1], color[2], 80), outline=color, width=2)
        text_bbox = draw.textbbox((0, 0), name, font=font_small)
        text_w = text_bbox[2] - text_bbox[0]
        draw.text((bx - text_w // 2, by - 8), name, fill=TEXT_WHITE, font=font_small)

    # Characteristics box
    char_box_y = dag_start_y + 260
    draw.rounded_rectangle([right_margin + 60, char_box_y, right_margin + right_w - 60, char_box_y + 70],
                          radius=6, fill=(26, 26, 46), outline=ACCENT_BLUE, width=1)
    draw.text((right_margin + right_w // 2 - 90, char_box_y + 15), "特点：并行 · 去中心 · 自由探索", fill=TEXT_GRAY, font=font_small)
    draw.text((right_margin + right_w // 2 - 75, char_box_y + 40), "无主分支 · 无 PR · 无合并", fill=(100, 100, 100), font=font_small)

    # Save
    img.save('dag-comparison.png', 'PNG')
    print("Created dag-comparison.png")
    return img

def create_git_bundle_flow():
    """Create Git Bundle flow diagram"""
    width, height = 1200, 600
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_title = get_font(26)
    font_label = get_font(18)
    font_small = get_font(14)
    font_code = get_font(12)

    # Title
    title = "Git Bundle 传输机制"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((width // 2 - title_width // 2, 25), title, fill=TEXT_WHITE, font=font_title)

    # Three sections
    sections = [
        (80, "Agent", ACCENT_BLUE, [
            ("def train():", ACCENT_GREEN),
            ("  model.step()", ACCENT_GREEN),
            ("代码提交", TEXT_GRAY),
        ]),
        (width // 2 - 150, "Git Bundle", ACCENT_PURPLE, [
            ("bundle.bundle", TEXT_WHITE),
            ("打包的提交", TEXT_GRAY),
        ]),
        (width - 380, "Server", ACCENT_GREEN, [
            ("1. 验证 Bundle", TEXT_WHITE),
            ("2. Unbundle", TEXT_WHITE),
        ]),
    ]

    box_w = 300
    box_h = 180

    for i, (x, title, color, lines) in enumerate(sections):
        y = 100
        draw.rounded_rectangle([x, y, x + box_w, y + box_h], radius=10, fill=(30, 30, 50), outline=color, width=2)

        # Title
        draw.text((x + box_w // 2 - 40, y + 15), title, fill=color, font=font_label)

        # Content
        content_y = y + 50
        for j, (line_text, line_color) in enumerate(lines):
            if "def " in line_text or "model" in line_text:
                # Code style - draw code box
                draw.rounded_rectangle([x + 30, content_y + j * 30, x + box_w - 30, content_y + j * 30 + 25],
                                      radius=3, fill=(15, 15, 26))
                draw.text((x + 40, content_y + j * 30 + 5), line_text, fill=line_color, font=font_code)
            else:
                draw.text((x + box_w // 2 - 40, content_y + j * 30), line_text, fill=line_color, font=font_small)

    # Arrows between sections
    arrow_y = 190
    draw.line([(380, arrow_y), (470, arrow_y)], fill=ACCENT_BLUE, width=3)
    draw.polygon([(470, arrow_y - 8), (490, arrow_y), (470, arrow_y + 8)], fill=ACCENT_BLUE)
    draw.text((405, arrow_y - 20), "创建", fill=TEXT_GRAY, font=font_small)

    draw.line([(780, arrow_y), (870, arrow_y)], fill=ACCENT_BLUE, width=3)
    draw.polygon([(870, arrow_y - 8), (890, arrow_y), (870, arrow_y + 8)], fill=ACCENT_BLUE)
    draw.text((805, arrow_y - 20), "HTTP POST", fill=TEXT_GRAY, font=font_small)

    # Arrow down to bare repo
    draw.line([(width // 2 + 100, 280), (width // 2 + 100, 340)], fill=ACCENT_GREEN, width=2)
    draw.polygon([(width // 2 + 92, 340), (width // 2 + 100, 360), (width // 2 + 108, 340)], fill=ACCENT_GREEN)

    # Bare repo
    repo_x = width - 380
    repo_y = 370
    draw.rounded_rectangle([repo_x, repo_y, repo_x + box_w, repo_y + 150], radius=10, fill=(26, 26, 30), outline=ACCENT_ORANGE, width=2)
    draw.text((repo_x + box_w // 2 - 60, repo_y + 15), "Bare Git Repo", fill=ACCENT_ORANGE, font=font_label)

    # Git DAG visualization (simplified)
    dag_x = repo_x + box_w // 2
    dag_y = repo_y + 60

    # Draw some nodes
    nodes = [
        (dag_x - 60, dag_y, (255, 170, 0, 100)),
        (dag_x, dag_y - 20, (255, 170, 0, 150)),
        (dag_x + 60, dag_y, (255, 170, 0, 100)),
    ]

    for nx, ny, color in nodes:
        draw.ellipse([nx - 12, ny - 12, nx + 12, ny + 12], fill=color, outline=ACCENT_ORANGE, width=2)

    draw.line([(dag_x - 48, dag_y), (dag_x - 12, dag_y - 10)], fill=ACCENT_ORANGE, width=2)
    draw.line([(dag_x + 12, dag_y - 10), (dag_x + 48, dag_y)], fill=ACCENT_ORANGE, width=2)

    draw.text((repo_x + box_w // 2 - 35, dag_y + 40), "DAG 存储", fill=TEXT_GRAY, font=font_small)

    # Features
    features_y = 320
    features = [
        ("离线友好", ACCENT_GREEN),
        ("原子性", ACCENT_GREEN),
        ("安全性", ACCENT_GREEN),
    ]

    for i, (text, color) in enumerate(features):
        x = 200 + i * 250
        draw.ellipse([x - 8, features_y - 8, x + 8, features_y + 8], fill=color)
        draw.text((x + 15, features_y - 10), text, fill=TEXT_GRAY, font=font_small)

    # Bottom info
    info_y = 540
    draw.rounded_rectangle([60, info_y, width - 60, info_y + 50], radius=8, fill=(15, 15, 26), outline=(50, 50, 50))
    draw.text((width // 2 - 200, info_y + 12), "核心优势：原子性传输 · 离线友好 · 可验证内容 · 简化冲突处理", fill=TEXT_GRAY, font=font_small)
    draw.text((width // 2 - 220, info_y + 32), "AgentHub 不使用传统 git push/pull，而是用 Git Bundle 作为传输协议", fill=(80, 80, 80), font=font_small)

    # Save
    img.save('git-bundle-flow.png', 'PNG')
    print("Created git-bundle-flow.png")
    return img

if __name__ == '__main__':
    os.chdir('/Users/wp931120/lobsterai/project/wp_work/articles/karpathy-agenthub-article')

    create_architecture_diagram()
    create_dag_comparison()
    create_git_bundle_flow()

    print("\nAll images created successfully!")

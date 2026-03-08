#!/usr/bin/env python3
"""
Mermaid 图表渲染脚本
将 Markdown 文件中的 Mermaid 代码块渲染为 PNG 图片
"""

import re
import os
from playwright.sync_api import sync_playwright

def extract_mermaid_blocks(markdown_content):
    """提取所有 Mermaid 代码块"""
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    return matches

def render_mermaid_to_png(mermaid_code, output_path, timeout=30000):
    """使用 Playwright 渲染 Mermaid 图表为 PNG"""

    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; display: flex; justify-content: center; }}
        .mermaid {{ display: flex; justify-content: center; }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
        }});

        // 等待渲染完成
        setTimeout(() => {{
            window.renderComplete = true;
        }}, 2000);
    </script>
</body>
</html>
"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 设置更大的视口
        page.set_viewport_size({"width": 1200, "height": 800})

        # 加载 HTML
        page.set_content(html_template, wait_until='networkidle')

        # 等待渲染完成
        page.wait_for_function("window.renderComplete", timeout=timeout)

        # 截图
        page.screenshot(path=output_path, full_page=True, clip={"x": 0, "y": 0, "width": 1200, "height": 800})

        browser.close()

    return True

def main():
    # 读取文章
    md_path = os.path.join(os.path.dirname(__file__), 'turix-cua-desktop-agent.md')
    output_dir = os.path.join(os.path.dirname(__file__), 'turix-cua-desktop-agent_images')

    os.makedirs(output_dir, exist_ok=True)

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 Mermaid 图表
    mermaid_blocks = extract_mermaid_blocks(content)

    print(f"找到 {len(mermaid_blocks)} 个 Mermaid 图表")

    # 渲染每个图表
    for i, mermaid_code in enumerate(mermaid_blocks, 1):
        output_path = os.path.join(output_dir, f'diagram_{i}_mermaid.png')
        print(f"渲染图表 {i}/{len(mermaid_blocks)}...")

        try:
            render_mermaid_to_png(mermaid_code, output_path)
            print(f"✅ 已保存：{output_path}")
        except Exception as e:
            print(f"❌ 渲染失败：{e}")
            # 保存原始 Mermaid 代码用于调试
            error_path = os.path.join(output_dir, f'diagram_{i}_error.mmd')
            with open(error_path, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)
            print(f"   已保存错误文件：{error_path}")

if __name__ == '__main__':
    main()

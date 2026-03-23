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
        body {{ margin: 0; padding: 20px; display: flex; justify-content: center; background: white; }}
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
        page.set_viewport_size({"width": 1400, "height": 1000})

        # 加载 HTML
        page.set_content(html_template, wait_until='networkidle')

        # 等待渲染完成
        page.wait_for_function("window.renderComplete", timeout=timeout)

        # 找到 mermaid 元素并获取其尺寸
        mermaid_element = page.query_selector('.mermaid')
        if mermaid_element:
            box = mermaid_element.bounding_box()
            if box:
                clip_rect = {
                    'x': max(0, box['x'] - 20),
                    'y': max(0, box['y'] - 20),
                    'width': box['width'] + 40,
                    'height': box['height'] + 40
                }
                page.screenshot(path=output_path, clip=clip_rect)
            else:
                page.screenshot(path=output_path, full_page=True)
        else:
            page.screenshot(path=output_path, full_page=True)

        browser.close()

    return True

def main():
    # 文章路径
    article_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(article_dir, 'article.md')
    images_dir = os.path.join(article_dir, 'images')

    os.makedirs(images_dir, exist_ok=True)

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 Mermaid 图表
    mermaid_blocks = extract_mermaid_blocks(content)

    print(f"找到 {len(mermaid_blocks)} 个 Mermaid 图表")

    if not mermaid_blocks:
        print("没有找到需要渲染的 Mermaid 图表")
        return

    # 渲染每个图表
    for i, mermaid_code in enumerate(mermaid_blocks, 1):
        output_path = os.path.join(images_dir, f'diagram_{i}.png')
        print(f"渲染图表 {i}/{len(mermaid_blocks)}...")

        try:
            render_mermaid_to_png(mermaid_code, output_path)
            print(f"✅ 已保存：{output_path}")
        except Exception as e:
            print(f"❌ 渲染失败：{e}")

    # 创建 article_with_images.md
    new_content = content
    for i in range(len(mermaid_blocks), 0, -1):
        # 从后往前替换，避免索引问题
        pattern = r'```mermaid\n.*?\n```'
        matches = list(re.finditer(pattern, new_content, re.DOTALL))
        if matches:
            match = matches[i-1]
            new_content = new_content[:match.start()] + f'![图{i}](images/diagram_{i}.png)' + new_content[match.end():]

    output_article = os.path.join(article_dir, 'article_with_images.md')
    with open(output_article, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n✅ 创建了渲染后的文章：{output_article}")

if __name__ == '__main__':
    main()
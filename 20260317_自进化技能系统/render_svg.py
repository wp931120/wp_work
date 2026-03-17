#!/usr/bin/env python3
"""Render SVG images to PNG using Playwright."""

import os
import re
import subprocess
import sys

def extract_svgs(markdown_file):
    """Extract all SVG blocks from markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <svg>...</svg> blocks
    svg_pattern = re.compile(r'(<svg[^>]*>.*?</svg>)', re.DOTALL)
    svgs = svg_pattern.findall(content)
    return svgs, content

def render_svg_to_png(svg_content, output_path, width=1400, scale=2):
    """Render SVG to PNG using Playwright."""
    html = f'''<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; padding: 20px; background: transparent; }}
    </style>
</head>
<body>
{svg_content}
</body>
</html>'''

    # Write temp HTML with absolute path
    output_abs = os.path.abspath(output_path)
    temp_html = output_abs.replace('.png', '.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html)

    # Use playwright to screenshot
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': 1000})
        page.goto(f'file://{temp_html}')  # temp_html is already absolute path

        # Find svg and get its dimensions
        svg_element = page.query_selector('svg')
        clip_rect = None
        if svg_element:
            box = svg_element.bounding_box()
            if box:
                # Clip to SVG bounds with padding
                clip_rect = {
                    'x': max(0, box['x'] - 10),
                    'y': max(0, box['y'] - 10),
                    'width': box['width'] + 20,
                    'height': box['height'] + 20
                }

        page.screenshot(path=output_abs, clip=clip_rect)
        browser.close()

    # Clean up temp HTML
    os.remove(temp_html)
    print(f"Rendered: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python render_svg.py <article.md>")
        sys.exit(1)

    article_path = sys.argv[1]
    article_dir = os.path.dirname(article_path)
    images_dir = os.path.join(article_dir, 'images')

    # Create images directory
    os.makedirs(images_dir, exist_ok=True)

    # Extract SVGs
    svgs, content = extract_svgs(article_path)

    if not svgs:
        print("No SVG blocks found in the article.")
        return

    print(f"Found {len(svgs)} SVG blocks")

    # Render each SVG
    for i, svg in enumerate(svgs, 1):
        output_path = os.path.join(images_dir, f'diagram_{i}.png')
        render_svg_to_png(svg, output_path)

    # Create article_with_images.md
    new_content = content
    for i, svg in enumerate(svgs, 1):
        # Replace SVG block with image reference
        new_content = new_content.replace(
            svg,
            f'![图{i}](images/diagram_{i}.png)',
            1
        )

    output_article = article_path.replace('article.md', 'article_with_images.md')
    with open(output_article, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nCreated: {output_article}")

if __name__ == '__main__':
    main()
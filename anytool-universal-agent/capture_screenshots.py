#!/usr/bin/env python3
"""
Capture screenshots from AnyTool website and GitHub page
"""

from playwright.sync_api import sync_playwright
import os

OUTPUT_DIR = "/Users/wp931120/lobsterai/project/wp_work/anytool-universal-agent/"

def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        screenshots = []

        # 1. Capture AnyTool official website
        print("Visiting https://anytool.ai...")
        try:
            page.goto("https://anytool.ai", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000)

            # Full page screenshot
            full_path = os.path.join(OUTPUT_DIR, "anytool-official-website.png")
            page.screenshot(path=full_path, full_page=True)
            screenshots.append((full_path, "AnyTool 官方网站完整截图"))

            # Logo area (typically top left)
            logo_path = os.path.join(OUTPUT_DIR, "anytool-logo.png")
            page.screenshot(path=logo_path, clip={"x": 0, "y": 0, "width": 400, "height": 100})
            screenshots.append((logo_path, "AnyTool Logo 区域"))

            # Hero section
            hero_path = os.path.join(OUTPUT_DIR, "anytool-hero-section.png")
            page.screenshot(path=hero_path, clip={"x": 0, "y": 0, "width": 1920, "height": 800})
            screenshots.append((hero_path, "AnyTool 主页横幅区域"))

            print(f"  Captured: {full_path}")
        except Exception as e:
            print(f"  Error capturing anytool.ai: {e}")

        # 2. Capture GitHub page
        print("Visiting https://github.com/HKUDS/AnyTool...")
        try:
            page.goto("https://github.com/HKUDS/AnyTool", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(2000)

            # Full page screenshot
            github_full_path = os.path.join(OUTPUT_DIR, "anytool-github-page.png")
            page.screenshot(path=github_full_path, full_page=True)
            screenshots.append((github_full_path, "AnyTool GitHub 页面完整截图"))

            # README area (architecture diagrams, etc.)
            readme_path = os.path.join(OUTPUT_DIR, "anytool-github-readme.png")
            page.screenshot(path=readme_path, clip={"x": 0, "y": 150, "width": 1920, "height": 1200})
            screenshots.append((readme_path, "AnyTool GitHub README 区域（可能包含架构图）"))

            print(f"  Captured: {github_full_path}")
        except Exception as e:
            print(f"  Error capturing github page: {e}")

        browser.close()

        return screenshots

if __name__ == "__main__":
    screenshots = capture_screenshots()
    print("\n" + "="*60)
    print("截图完成！保存的文件:")
    print("="*60)
    for path, description in screenshots:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"\n{path}")
            print(f"  说明：{description}")
            print(f"  大小：{size/1024:.1f} KB")

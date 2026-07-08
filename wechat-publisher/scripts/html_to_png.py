#!/usr/bin/env python3
"""
HTML 转 PNG 截图工具
使用 Playwright 将 HTML 文件渲染为高质量 PNG 图片，适合手机阅读。

用法：
  python html_to_png.py <input.html> <output.png> [--width 420] [--scale 2]
"""

import argparse
import asyncio
import sys
from pathlib import Path


async def html_to_png(html_path: str, output_path: str, width: int = 420, scale: int = 2):
    """将 HTML 文件渲染为 PNG 截图"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("[错误] 需要安装 playwright: pip install playwright && playwright install chromium")
        sys.exit(1)

    html_file = Path(html_path).resolve()
    if not html_file.exists():
        print(f"[错误] HTML 文件不存在: {html_path}")
        sys.exit(1)

    file_url = f"file:///{str(html_file).replace(chr(92), '/')}"

    print(f"[渲染] {html_path} -> {output_path}")
    print(f"[参数] width={width}, device_scale_factor={scale}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": width, "height": 800},
            device_scale_factor=scale,
        )
        page = await context.new_page()
        await page.goto(file_url, wait_until="networkidle")
        # 等待页面完全渲染（含字体加载）
        await page.wait_for_timeout(1500)
        # 截取完整页面
        png_bytes = await page.screenshot(
            full_page=True,
            type="png",
        )
        output = Path(output_path)
        output.write_bytes(png_bytes)
        print(f"[完成] 截图已保存: {output_path} ({len(png_bytes)} bytes)")
        await browser.close()


def main():
    parser = argparse.ArgumentParser(description="HTML 转 PNG 截图工具（Playwright）")
    parser.add_argument("input", help="输入 HTML 文件路径")
    parser.add_argument("output", help="输出 PNG 文件路径")
    parser.add_argument("--width", type=int, default=420, help="渲染宽度（默认 420，手机友好）")
    parser.add_argument("--scale", type=int, default=2, help="设备像素比（默认 2，高清）")
    args = parser.parse_args()

    asyncio.run(html_to_png(args.input, args.output, args.width, args.scale))


if __name__ == "__main__":
    main()

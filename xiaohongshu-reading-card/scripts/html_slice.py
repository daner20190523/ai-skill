#!/usr/bin/env python3
"""
HTML 多卡片切片工具
将包含多张卡片（每张1080×1440竖排堆叠）的HTML渲染为全页截图，然后按高度竖向切分。

用法：
  python html_slice.py <cards.html> --card-height 1440 [--width 1080] [--scale 2]
  
输出：
  card_01.png, card_02.png, ... + full_page.png（完整长图）到 HTML 同级目录
"""

import argparse
import asyncio
import sys
from pathlib import Path


async def render_full_page(html_path: str, output_png: str, width: int, scale: int):
    """用 Playwright 渲染HTML为全页截图"""
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

    print(f"[Render] {html_path}")
    print(f"[Params] width={width}, device_scale_factor={scale}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": width, "height": 1440},
            device_scale_factor=scale,
        )
        page = await context.new_page()
        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_timeout(2000)

        png_bytes = await page.screenshot(full_page=True, type="png")
        output = Path(output_png)
        output.write_bytes(png_bytes)
        
        await browser.close()
        
        return len(png_bytes)


def slice_png(full_png: str, output_dir: str, card_height: int, scale: int):
    """用 Pillow 竖向切分 PNG"""
    try:
        from PIL import Image
    except ImportError:
        print("[错误] 需要安装 Pillow: pip install Pillow")
        sys.exit(1)

    img = Image.open(full_png)
    w, h = img.size
    sliced_height = card_height * scale  # 实际像素高度（含 scale）
    
    print(f"[Slice] Original: {w}x{h}, card height: {sliced_height}px")
    
    card_count = h // sliced_height
    remainder = h % sliced_height
    
    if remainder > 0:
        print(f"[Warn] Height {h} not divisible by {sliced_height}, {remainder}px remainder discarded")
    
    output_dir_path = Path(output_dir)
    for i in range(card_count):
        top = i * sliced_height
        bottom = top + sliced_height
        card = img.crop((0, top, w, bottom))
        card_name = f"card_{i+1:02d}.png"
        card_path = output_dir_path / card_name
        card.save(card_path, "PNG")
        print(f"  [{i+1}/{card_count}] {card_name} ({card.size[0]}×{card.size[1]})")
    
    # 保留完整长图为产物
    full_page_path = output_dir_path / "full_page.png"
    Path(full_png).rename(full_page_path)
    print(f"[FullPage] Saved: {full_page_path}")
    
    return card_count


async def main():
    parser = argparse.ArgumentParser(description="HTML 多卡片切片工具")
    parser.add_argument("html", help="输入 HTML 文件路径（含多张堆叠卡片）")
    parser.add_argument("--card-height", type=int, default=1440, help="每张卡片 CSS 高度（默认 1440）")
    parser.add_argument("--width", type=int, default=1080, help="渲染宽度（默认 1080）")
    parser.add_argument("--scale", type=int, default=2, help="设备像素比（默认 2，输出 2160×2880）")
    args = parser.parse_args()

    html_path = Path(args.html).resolve()
    output_dir = html_path.parent
    
    # 临时全页截图（渲染后重命名为 full_page.png 保留）
    temp_png = output_dir / "_temp_render.png"

    print("=" * 50)
    print("HTML Multi-Card Slice")
    print("=" * 50)

    # Step 1: 渲染全页截图
    byte_count = await render_full_page(
        str(html_path), str(temp_png), args.width, args.scale
    )
    print(f"[Render OK] {byte_count} bytes")

    # Step 2: 切片
    card_count = slice_png(str(temp_png), str(output_dir), args.card_height, args.scale)

    print("=" * 50)
    print(f"[Done] {card_count} cards generated -> {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

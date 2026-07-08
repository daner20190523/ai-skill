#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长图切割工具

将生成长图切割成多张适合微信公众号的图片（每张高度约 1500px）

用法：
  python split_image.py <input.png> [--output-dir <dir>] [--height 1500]
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("[错误] 需要安装 Pillow: pip install Pillow")
    sys.exit(1)


def split_image(image_path: str, output_dir: str = None, slice_height: int = 1500) -> list:
    """
    将长图切割成多张图片

    参数：
        image_path: 输入图片路径
        output_dir: 输出目录（默认与输入图片同目录）
        slice_height: 每张图片的高度（像素）

    返回：
        切割后的图片路径列表
    """
    img_path = Path(image_path)
    if not img_path.exists():
        print(f"[错误] 图片不存在: {image_path}")
        sys.exit(1)

    # 打开图片
    img = Image.open(img_path)
    width, height = img.size
    print(f"[信息] 图片尺寸: {width}x{height}")

    # 确定输出目录
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = img_path.parent / img_path.stem
    out_dir.mkdir(exist_ok=True)

    # 切割图片
    slices = []
    num_slices = (height + slice_height - 1) // slice_height  # 向上取整
    print(f"[信息] 将切割成 {num_slices} 张图片")

    for i in range(num_slices):
        # 计算切割区域
        top = i * slice_height
        bottom = min((i + 1) * slice_height, height)

        # 切割
        slice_img = img.crop((0, top, width, bottom))

        # 保存
        slice_path = out_dir / f"{img_path.stem}_{i+1:02d}.png"
        slice_img.save(slice_path, "PNG")
        slices.append(str(slice_path))
        print(f"[完成] 已保存: {slice_path} ({width}x{bottom-top})")

    print(f"\n[完成] 共切割 {len(slices)} 张图片")
    return slices


def main():
    parser = argparse.ArgumentParser(description="长图切割工具")
    parser.add_argument("input", help="输入图片路径（PNG/JPG）")
    parser.add_argument("--output-dir", "-o", help="输出目录（默认在同目录下创建子文件夹）")
    parser.add_argument("--height", type=int, default=1500, help="每张图片的高度（默认 1500px）")
    args = parser.parse_args()

    slices = split_image(args.input, args.output_dir, args.height)

    # 输出切割后的图片路径（供其他脚本使用）
    print("\n--- 切割结果 ---")
    for i, path in enumerate(slices, start=1):
        print(f"{i}. {path}")


if __name__ == "__main__":
    main()

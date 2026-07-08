#!/usr/bin/env python3
"""
微信公众号封面图生成器

使用 AI 生成极简风格封面图，严格符合公众号头条封面规格。

功能：
  1. 根据技术名词生成 AI 绘图 prompt（极简风格，公众号封面适配）
  2. 后处理：将生成的图片裁剪/缩放到严格 900×383 像素
  3. 支持从已有图片直接裁剪

公众号封面规格：
  - 头条封面（大图）：900×383 像素，比例 2.35:1
  - 次条封面（小图）：200×200 像素
  - 本脚本默认生成头条封面大图

用法：
  # 从 AI 生成的原始图片裁剪到封面尺寸
  python generate_cover_image.py -i raw_image.png -o cover.png

  # 同时生成 AI prompt（仅打印，不生成图片）
  python generate_cover_image.py --prompt "Docker 容器技术" --style minimalist

  # 批量处理：从已有图片生成 900x383 + 200x200 两版
  python generate_cover_image.py -i input.png -o output --both-sizes
"""

import argparse
import sys
from pathlib import Path


# ============================================================
# 公众号封面尺寸规格
# ============================================================

COVER_SIZES = {
    "headline": (900, 383),   # 头条封面（大图，比例 2.35:1）
    "subheadline": (200, 200),  # 次条封面（小图，1:1）
}

# 艺术风格配色方案（用于 prompt 生成）
ARTISTIC_PALETTES = {
    "tech":     "深海蓝 #0f172a 渐变到极光青 #06b6d4，搭配霓虹光晕 #00d2ff，科技感中带着神秘氛围",
    "warm":     "暖米白 #fef7f0 为底，焦糖棕 #d97706 做视觉锚点，炭灰 #1e293b 压住重心，温暖而有质感",
    "dark":     "纯黑 #000000 为底，香槟金 #fbbf24 勾出轮廓光，珍珠白 #fefefe 提亮高光，奢华暗调",
    "clean":    "素雪白 #f8fafc 为底，雾松绿 #64748b 做层次，薄荷绿 #10b981 做点睛，清新通透",
    "cyber":    "深空紫 #1e1b4b 为底，霓虹粉 #ec4899 和电光青 #06b6d4 交织，赛博霓虹氛围",
    "art":      "莫兰迪灰粉 #fecdd3 + 雾霾蓝 #a5b4fc + 奶油白 #fef3c7，低饱和度艺术感，温柔高级",
    "nature":   "森林绿 #064e3b + 琥珀金 #f59e0b + 象牙白 #fefce8，自然光影，有机质感",
    "sunset":   "暮色紫 #581c87 + 落日橙 #ea580c + 云朵白 #fff7ed，温暖渐变，电影感",
}


# ============================================================
# AI Prompt 生成
# ============================================================

def build_cover_prompt(
    tech_name: str,
    style: str = "artistic",
    palette: str = "tech",
    extra: str = "",
) -> str:
    """根据技术名词构建 AI 绘图 prompt。

    生成具有艺术美感的封面图，适配公众号 900×383 横向布局。
    强调视觉冲击力、光影效果和材质质感。
    """
    palette_desc = ARTISTIC_PALETTES.get(palette, ARTISTIC_PALETTES["tech"])
    
    # 风格模板库
    style_templates = {
        "minimalist": (
            "Ultra-minimalist design, extreme negative space, "
            "single focal point, Japanese wabi-sabi aesthetic, "
            "subtle texture like rice paper or matte finish"
        ),
        "artistic": (
            "Artistic composition with depth and layers, "
            "cinematic lighting with soft shadows, "
            "material textures: frosted glass, brushed metal, or smooth stone, "
            "Bauhaus-inspired geometry, elegant and sophisticated"
        ),
        "geometric": (
            "Bold geometric shapes with perfect proportions, "
            "sacred geometry patterns, golden ratio composition, "
            "clean lines with subtle glow effects, "
            "architectural aesthetic, structural beauty"
        ),
        "abstract": (
            "Abstract expressionist style, fluid shapes like ink in water, "
            "dreamy atmosphere with soft focus edges, "
            "ethereal lighting, otherworldly beauty, "
            "poetic visual metaphor for technology"
        ),
        "gradient": (
            "Smooth gradient transitions like aurora borealis, "
            "iridescent sheen, pearlescent finish, "
            "soft focus with bokeh effects, "
            "dreamy pastel tones, gentle and inviting"
        ),
        "editorial": (
            "Magazine editorial layout style, "
            "high-end fashion photography lighting, "
            "sophisticated color grading, "
            "art direction quality, Vogue or Kinfolk aesthetic"
        ),
    }
    
    style_desc = style_templates.get(style, style_templates["artistic"])

    base = (
        f"WeChat official account cover image, wide landscape format 2.35:1, "
        f"topic concept: {tech_name}, "
        f"color palette: {palette_desc}, "
        f"{style_desc}, "
        f"no text or typography (will be added later), "
        f"composition: rule of thirds or golden ratio, "
        f"lighting: dramatic side lighting or soft backlight, "
        f"depth of field: shallow focus on subject, blurred background, "
        f"mood: sophisticated, intriguing, premium quality, "
        f"inspired by works in Vogue, Kinfolk, or high-end tech editorials, "
        f"4K resolution, photorealistic rendering, ray tracing lighting effects"
    )

    if extra:
        base += f", {extra}"

    return base


def print_prompt_info(tech_name: str, style: str, palette: str):
    """打印 prompt 生成信息，供 AI 调用 image_gen 工具。"""
    prompt = build_cover_prompt(tech_name, style, palette)
    print(f"\n{'='*60}")
    print(f"[封面图 Prompt] — {tech_name}")
    print(f"{'='*60}")
    print(f"风格: {style} | 配色: {palette}")
    print(f"输出尺寸: {COVER_SIZES['headline'][0]}×{COVER_SIZES['headline'][1]} px")
    print(f"\n--- AI 绘图 Prompt ---")
    print(prompt)
    print(f"--- 结束 ---\n")
    print("[提示] 用此 prompt 调用 image_gen 工具生成图片，")
    print(f"   然后用本脚本裁剪: python generate_cover_image.py -i output.png -o cover.png")


# ============================================================
# 图片裁剪/缩放
# ============================================================

def smart_crop_resize(
    input_path: str,
    output_path: str,
    target_size: tuple = (900, 383),
    focus: str = "center",
) -> str:
    """智能裁剪 + 缩放图片到目标尺寸。

    策略：先按目标比例居中裁剪，再缩放到精确尺寸。
    保持画面主体不丢失。

    参数：
      - input_path: 输入图片路径
      - output_path: 输出图片路径
      - target_size: (宽, 高) 像素
      - focus: 裁剪焦点 ('center', 'top', 'bottom', 'face')

    返回输出路径。
    """
    try:
        from PIL import Image
    except ImportError:
        print("❌ 缺少 Pillow，请运行: pip install Pillow", file=sys.stderr)
        sys.exit(1)

    img = Image.open(input_path).convert("RGB")
    orig_w, orig_h = img.size
    target_w, target_h = target_size
    target_ratio = target_w / target_h  # ≈ 2.35

    print(f"\n🖼 原始尺寸: {orig_w}×{orig_h} px")
    print(f"🎯 目标尺寸: {target_w}×{target_h} px (比例 {target_ratio:.2f}:1)")

    # 步骤 1：按目标比例裁剪
    orig_ratio = orig_w / orig_h

    if abs(orig_ratio - target_ratio) < 0.01:
        # 比例基本一致，直接缩放
        crop = img
        print("   → 比例匹配，直接缩放")
    elif orig_ratio > target_ratio:
        # 原图太宽：裁左右
        new_w = int(orig_h * target_ratio)
        offset = (orig_w - new_w) // 2
        if focus == "top":
            offset = 0
        elif focus == "bottom":
            offset = orig_w - new_w
        crop = img.crop((offset, 0, offset + new_w, orig_h))
        print(f"   → 裁左右：裁掉 {(orig_w - new_w)}px 宽度")
    else:
        # 原图太高：裁上下
        new_h = int(orig_w / target_ratio)
        offset = (orig_h - new_h) // 2
        if focus == "top":
            offset = 0
        elif focus == "bottom":
            offset = orig_h - new_h
        crop = img.crop((0, offset, orig_w, offset + new_h))
        print(f"   → 裁上下：裁掉 {(orig_h - new_h)}px 高度")

    # 步骤 2：缩放到精确尺寸
    resized = crop.resize(target_size, Image.LANCZOS)
    print(f"   → 缩放至 {target_w}×{target_h} px")

    # 保存
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    resized.save(out, quality=95, optimize=True)
    file_size_kb = out.stat().st_size / 1024

    print(f"✅ 封面图已生成: {out}")
    print(f"   尺寸: {target_w}×{target_h} px | 大小: {file_size_kb:.1f} KB")
    return str(out)


def batch_generate_cover(input_path: str, output_base: str):
    """批量生成头条封面 + 次条封面两版。"""
    # 大图 900×383
    headline_path = f"{output_base}_headline.png"
    smart_crop_resize(input_path, headline_path, COVER_SIZES["headline"])

    # 小图 200×200
    sub_path = f"{output_base}_sub.png"
    smart_crop_resize(input_path, sub_path, COVER_SIZES["subheadline"], focus="center")

    print(f"\n📦 批量完成，输出文件：")
    print(f"   头条封面: {headline_path}")
    print(f"   次条封面: {sub_path}")


# ============================================================
# 二维码叠加（可选）
# ============================================================

def add_qrcode_watermark(
    cover_path: str,
    qr_path: str,
    output_path: str,
    position: str = "bottom-right",
    margin: int = 20,
    size: int = 80,
):
    """在封面图上叠加公众号二维码水印。

    参数：
      - cover_path: 封面图路径
      - qr_path: 二维码图片路径
      - output_path: 输出路径
      - position: 位置 ('bottom-right', 'bottom-left', 'top-right')
      - margin: 边距
      - size: 二维码显示尺寸（等比缩放后最大边）
    """
    try:
        from PIL import Image
    except ImportError:
        print("❌ 缺少 Pillow", file=sys.stderr)
        sys.exit(1)

    cover = Image.open(cover_path).convert("RGBA")
    qr = Image.open(qr_path).convert("RGBA")

    # 缩放二维码
    qr.thumbnail((size, size), Image.LANCZOS)
    qr_w, qr_h = qr.size

    # 定位
    cw, ch = cover.size
    positions = {
        "bottom-right": (cw - qr_w - margin, ch - qr_h - margin),
        "bottom-left": (margin, ch - qr_h - margin),
        "top-right": (cw - qr_w - margin, margin),
    }
    pos = positions.get(position, positions["bottom-right"])

    # 叠加（二维码带透明通道）
    cover.paste(qr, pos, qr)
    out = Path(output_path)
    cover.convert("RGB").save(out, quality=95, optimize=True)
    print(f"✅ 已叠加二维码 → {out}")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="微信公众号封面图生成器 — AI 生图 + 智能裁剪到 900×383"
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    # ---- crop ----
    crop_parser = sub.add_parser("crop", help="裁剪/缩放已有图片到封面尺寸")
    crop_parser.add_argument("-i", "--input", required=True, help="输入图片路径")
    crop_parser.add_argument("-o", "--output", required=True, help="输出图片路径")
    crop_parser.add_argument(
        "--width", type=int, default=900, help="目标宽度（默认 900）"
    )
    crop_parser.add_argument(
        "--height", type=int, default=383, help="目标高度（默认 383）"
    )
    crop_parser.add_argument(
        "--focus", default="center",
        choices=["center", "top", "bottom"],
        help="裁剪焦点（默认 center）",
    )
    crop_parser.add_argument(
        "--both-sizes", action="store_true",
        help="同时输出 900×383 头条 + 200×200 次条",
    )

    # ---- prompt ----
    prompt_parser = sub.add_parser("prompt", help="生成 AI 绘图 prompt")
    prompt_parser.add_argument("name", help="技术名词")
    prompt_parser.add_argument(
        "--style", default="artistic",
        choices=["minimalist", "artistic", "geometric", "abstract", "gradient", "editorial"],
        help="艺术风格（默认 artistic）",
    )
    prompt_parser.add_argument(
        "--palette", default="tech",
        choices=list(ARTISTIC_PALETTES.keys()),
        help="配色方案（默认 tech）",
    )

    # ---- watermark ----
    wm_parser = sub.add_parser("watermark", help="叠加二维码水印")
    wm_parser.add_argument("-i", "--input", required=True, help="封面图路径")
    wm_parser.add_argument("-q", "--qr", required=True, help="二维码图片路径")
    wm_parser.add_argument("-o", "--output", required=True, help="输出路径")
    wm_parser.add_argument(
        "--position", default="bottom-right",
        choices=["bottom-right", "bottom-left", "top-right"],
    )
    wm_parser.add_argument("--margin", type=int, default=20, help="水印边距")
    wm_parser.add_argument("--size", type=int, default=80, help="水印尺寸")

    args = parser.parse_args()

    if args.command == "crop":
        if args.both_sizes:
            # 输出基名：output 去掉扩展名
            base = Path(args.output).with_suffix("")
            batch_generate_cover(args.input, str(base))
        else:
            smart_crop_resize(
                args.input, args.output,
                target_size=(args.width, args.height),
                focus=args.focus,
            )

    elif args.command == "prompt":
        print_prompt_info(args.name, args.style, args.palette)

    elif args.command == "watermark":
        add_qrcode_watermark(
            args.input, args.qr, args.output,
            position=args.position,
            margin=args.margin,
            size=args.size,
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

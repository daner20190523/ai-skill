#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agnes AI 图像生成脚本 — 支持文生图 (txt2img) 和 图生图 (img2img)。

API Key 优先从同目录下的 agnes_config.yaml 读取，命令行传参会覆盖配置文件。

文生图 (txt2img):
  echo "prompt" | python agnes_image.py <OUTPUT_PATH>
  printf "p1\\np2\\np3\\np4" | python agnes_image.py <OUTPUT_DIR> --batch --count 4

图生图 (img2img):
  echo "prompt" | python agnes_image.py <OUTPUT_PATH> --image <REFERENCE_IMAGE>
  printf "p1\\np2" | python agnes_image.py <OUTPUT_DIR> --image <REF_IMG> --batch --count 2

参数说明:
  --image PATH    参考图路径 (启用图生图模式)
  --strength 0.7  图生图重绘强度 0.0-1.0 (默认 0.65)
  --api-key KEY   手动指定 API Key
  --size WxH      输出尺寸 (默认 768x1024)
  --model NAME    模型名 (默认 agnes-image-2.1-flash)
  --batch         批量模式
  --count N       批量数量 (默认 4)
"""

import sys
import os
import json
import time
import base64
import urllib.request
import urllib.error
from pathlib import Path

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

# ---- 常量 ----
API_BASE = "https://apihub.agnes-ai.com/v1"
IMAGE_ENDPOINT = f"{API_BASE}/images/generations"
DEFAULT_MODEL = "agnes-image-2.1-flash"
DEFAULT_SIZE = "768x1024"  # 3:4 portrait

# ---- 配置文件路径 ----
# 优先级: 1) 同目录 agnes_config.yaml  2) 项目根 config/agnes_config.yaml
_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent  # ai-prompt-master/

_CFG_CANDIDATES = [
    _SCRIPT_DIR / "agnes_config.yaml",                              # 技能 scripts/ 目录
    _SKILL_ROOT.parent.parent.parent / "tech-knowledge-card" / "config" / "agnes_config.yaml",  # 项目根
]
_CONFIG_PATH = next((p for p in _CFG_CANDIDATES if p.exists()), _CFG_CANDIDATES[0])


# ============================================================
# 配置加载
# ============================================================
def load_config() -> dict:
    """从 YAML 加载 Agnes 配置。失败返回空字典。"""
    if not _CONFIG_PATH.exists():
        print(f"  [WARN] Config not found: {_CONFIG_PATH}", file=sys.stderr)
        return {}

    if not _HAS_YAML:
        print("  [WARN] PyYAML not installed. Install: pip install pyyaml", file=sys.stderr)
        return {}

    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        agnes_cfg = cfg.get("agnes", {}) or {}
        api_key = agnes_cfg.get("api_key", "")
        if api_key and api_key != "YOUR_API_KEY_HERE":
            print(f"  [OK] Loaded API key from {_CONFIG_PATH}")
            return agnes_cfg
        else:
            print(f"  [WARN] API key not configured in {_CONFIG_PATH}", file=sys.stderr)
            return {}
    except Exception as e:
        print(f"  [WARN] Config parse error: {e}", file=sys.stderr)
        return {}


# ============================================================
# 图片编码 (用于 img2img)
# ============================================================
def encode_image_base64(image_path: str) -> str | None:
    """将图片编码为 base64 data URI。"""
    path = Path(image_path)
    if not path.exists():
        print(f"  [FAIL] Reference image not found: {image_path}", file=sys.stderr)
        return None

    ext = path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    mime = mime_map.get(ext, "image/png")

    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{data}"
    except Exception as e:
        print(f"  [FAIL] Failed to encode image: {e}", file=sys.stderr)
        return None


# ============================================================
# API 调用
# ============================================================
def call_image_api(
    api_key: str,
    prompt: str,
    size: str = DEFAULT_SIZE,
    model: str = DEFAULT_MODEL,
    image_path: str | None = None,
    strength: float = 0.65,
    timeout: int = 120,
) -> str | None:
    """
    调用 Agnes AI 图像生成 API。
    - 若提供 image_path → img2img 模式
    - 否则 → txt2img 模式

    返回生成的图片 URL，失败返回 None。
    """
    payload: dict = {
        "model": model,
        "prompt": prompt,
        "size": size,
    }

    # 图生图模式
    if image_path:
        encoded = encode_image_base64(image_path)
        if not encoded:
            return None
        payload["image"] = encoded
        payload["strength"] = strength
        mode_label = f"img2img (ref={Path(image_path).name}, strength={strength})"
    else:
        mode_label = "txt2img"

    print(f"  [{mode_label}] Sending request...")

    req = urllib.request.Request(
        IMAGE_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  [FAIL] API error {e.code}: {body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [FAIL] Request failed: {e}", file=sys.stderr)
        return None

    if "data" in result and len(result["data"]) > 0:
        url = result["data"][0].get("url")
        if url:
            return url

    print(f"  [FAIL] Unexpected response: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
    return None


# ============================================================
# 图片下载
# ============================================================
def download_image(url: str, output_path: str, timeout: int = 120) -> bool:
    """下载图片并保存到本地。"""
    try:
        urllib.request.urlretrieve(url, output_path)
        size_kb = os.path.getsize(output_path) / 1024
        print(f"  [OK] Saved: {output_path} ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"  [FAIL] Download failed: {e}", file=sys.stderr)
        return False


# ============================================================
# 单图模式
# ============================================================
def single_mode(
    api_key: str,
    output_path: str,
    image_path: str | None = None,
    strength: float = 0.65,
    size: str = DEFAULT_SIZE,
    model: str = DEFAULT_MODEL,
) -> None:
    """生成一张图片（从 stdin 读取 prompt）。"""
    prompt = sys.stdin.read().strip()
    if not prompt:
        print("Error: no prompt provided on stdin", file=sys.stderr)
        sys.exit(1)

    print(f"Prompt:  {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    url = call_image_api(api_key, prompt, size=size, model=model, image_path=image_path, strength=strength)

    if url:
        time.sleep(1)
        download_image(url, output_path)
    else:
        print("  [FAIL] Generation failed", file=sys.stderr)
        sys.exit(1)


# ============================================================
# 批量模式
# ============================================================
def batch_mode(
    api_key: str,
    output_dir: str,
    count: int = 4,
    image_path: str | None = None,
    strength: float = 0.65,
    size: str = DEFAULT_SIZE,
    model: str = DEFAULT_MODEL,
) -> None:
    """批量生成 N 张图片。从 stdin 读取 prompt（每行一个）。仅 1 个 prompt 则重复。"""
    prompts = [line.strip() for line in sys.stdin if line.strip()]
    if not prompts:
        print("Error: no prompts provided on stdin", file=sys.stderr)
        sys.exit(1)

    if len(prompts) == 1 and count > 1:
        prompts = prompts * count

    if len(prompts) != count:
        print(
            f"Error: expected {count} prompts, got {len(prompts)}. "
            "Each prompt on its own line, or provide 1 prompt to repeat.",
            file=sys.stderr,
        )
        sys.exit(1)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for i, prompt in enumerate(prompts, 1):
        filename = f"ai-prompt_{i:02d}.png"
        filepath = out / filename

        if filepath.exists():
            print(f"\n[{i}/{count}] {filename} already exists → skip")
            continue

        print(f"\n[{i}/{count}] {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
        url = call_image_api(api_key, prompt, size=size, model=model, image_path=image_path, strength=strength)

        if url:
            time.sleep(2)
            download_image(url, str(filepath))
        else:
            print(f"  [FAIL] [{i}/{count}] Generation failed, continuing...", file=sys.stderr)

        if i < count:
            time.sleep(2)

    mode_str = "img2img" if image_path else "txt2img"
    print(f"\n[OK] Batch {mode_str} complete ({count} images). Output:", out)


# ============================================================
# CLI 入口
# ============================================================
def main() -> None:
    args = sys.argv[1:]

    # 可解析参数
    cli_api_key = None
    cli_image = None
    cli_strength = 0.65
    cli_size = DEFAULT_SIZE
    cli_model = DEFAULT_MODEL
    count = 4
    batch = False

    def pop_kv(flag: str) -> str | None:
        """弹出 --flag value 形式的参数值。"""
        nonlocal args
        try:
            idx = args.index(flag)
        except ValueError:
            return None
        if idx + 1 >= len(args):
            print(f"Error: {flag} requires a value", file=sys.stderr)
            sys.exit(1)
        val = args[idx + 1]
        del args[idx : idx + 2]
        return val

    # --api-key
    v = pop_kv("--api-key")
    if v:
        cli_api_key = v

    # --image (图生图参考图)
    v = pop_kv("--image")
    if v:
        cli_image = v

    # --strength (图生图强度)
    v = pop_kv("--strength")
    if v:
        try:
            cli_strength = float(v)
        except ValueError:
            print("Error: --strength requires a float 0.0-1.0", file=sys.stderr)
            sys.exit(1)

    # --size
    v = pop_kv("--size")
    if v:
        cli_size = v

    # --model
    v = pop_kv("--model")
    if v:
        cli_model = v

    # --count
    v = pop_kv("--count")
    if v:
        try:
            count = int(v)
        except ValueError:
            print("Error: --count requires an integer", file=sys.stderr)
            sys.exit(1)

    # --batch
    if "--batch" in args:
        batch = True
        args.remove("--batch")

    # --- 获取 API Key ---
    if cli_api_key:
        api_key = cli_api_key
        print("  [OK] Using API key from command line")
    else:
        cfg = load_config()
        api_key = cfg.get("api_key", "")
        if not api_key:
            print(
                "Error: No API key provided. Either:\n"
                f"  1. Set api_key in {_CONFIG_PATH}\n"
                "  2. Pass --api-key <KEY> on the command line\n"
                "Get your free key at: https://platform.agnes-ai.com/settings/apiKeys",
                file=sys.stderr,
            )
            sys.exit(1)

    # --- 路由 ---
    if batch:
        if len(args) != 1:
            print(
                "Usage (batch): printf 'p1\\np2\\n...' | python agnes_image.py <OUTPUT_DIR> --batch [--count N] [--image REF]",
                file=sys.stderr,
            )
            sys.exit(1)
        output_dir = args[0]
        batch_mode(api_key, output_dir, count=count, image_path=cli_image, strength=cli_strength, size=cli_size, model=cli_model)
    else:
        if len(args) != 1:
            print(
                "Usage (single): echo 'prompt' | python agnes_image.py <OUTPUT_PATH> [--image REF] [--strength 0.7]",
                file=sys.stderr,
            )
            sys.exit(1)
        output_path = args[0]
        single_mode(api_key, output_path, image_path=cli_image, strength=cli_strength, size=cli_size, model=cli_model)


if __name__ == "__main__":
    main()

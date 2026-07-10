#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送 HTML 内容到微信公众号草稿箱

功能：
  1. 读取微信公众号配置（appid/appsecret）
  2. 获取 access_token（自动缓存、过期刷新）
  3. 上传文中图片到微信素材库，替换 URL
  4. 上传封面图到永久素材库，获取 thumb_media_id
  5. 将 HTML 内容 + 封面推送到草稿箱

用法：
  # 模式 1：推送 HTML 正文（传统模式）
  python push_to_wechat_draft.py <input.html> --title "文章标题" [--cover-image cover.png]

  # 模式 2：自动检测切割图片（需 HTML 文件在同目录）
  python push_to_wechat_draft.py <input.html> --use-split-images --title "标题" [--cover-image cover.png]

  # 模式 3：直接指定已有截图上传（不依赖 HTML 文件）
  python push_to_wechat_draft.py --image-files "output/wuxia/*_0*.png" --title "标题" [--cover-image cover.png]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib import request, parse
from urllib.error import HTTPError, URLError

# Windows 控制台 UTF-8 编码支持
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


# ============================================================
# 配置加载
# ============================================================

def load_config(config_path: str = None) -> dict:
    """加载 YAML 配置文件。优先 wechat_config.secret.yaml，fallback wechat_config.yaml。"""
    search_paths = []
    skill_dir = Path(__file__).resolve().parent.parent

    if config_path:
        search_paths.append(Path(config_path))
    else:
        search_paths = [
            skill_dir / "config" / "wechat_config.secret.yaml",
            skill_dir / "config" / "wechat_config.yaml",
            skill_dir / "config" / "wechat_config.template.yaml",
        ]

    cfg = {}
    for p in search_paths:
        if p.exists():
            try:
                import yaml
                with open(p, "r", encoding="utf-8") as f:
                    loaded = yaml.safe_load(f)
                if loaded:
                    cfg = loaded
                    print(f"[OK] 配置已加载: {p}")
                    break
            except ImportError:
                print("[ERROR] 缺少 PyYAML，请运行: pip install pyyaml", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"[WARN] 配置加载失败: {e}", file=sys.stderr)

    if not cfg:
        print("[ERROR] 未找到配置文件！请复制 config/wechat_config.template.yaml -> wechat_config.secret.yaml 并填入真实密钥",
              file=sys.stderr)
        sys.exit(1)

    return cfg


def get_wechat_creds(cfg: dict) -> tuple:
    """从配置提取微信凭据。"""
    wc = cfg.get("wechat", {})
    appid = wc.get("appid", "")
    appsecret = wc.get("appsecret", "")
    use_test = wc.get("use_test_account", 0)

    if not appid or appid == "wx_your_appid_here":
        print("[ERROR] 请在配置文件中填入真实的微信公众号 AppID", file=sys.stderr)
        sys.exit(1)
    if not appsecret or appsecret == "your_appsecret_here":
        print("[ERROR] 请在配置文件中填入真实的微信公众号 AppSecret", file=sys.stderr)
        sys.exit(1)

    return appid, appsecret, use_test


# ============================================================
# Access Token 管理
# ============================================================

TOKEN_CACHE_FILE = Path(__file__).resolve().parent.parent / "config" / ".token_cache.json"


def load_token_cache() -> dict:
    """加载本地 token 缓存。"""
    if TOKEN_CACHE_FILE.exists():
        try:
            return json.loads(TOKEN_CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_token_cache(data: dict):
    """保存 token 缓存到本地。"""
    TOKEN_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_CACHE_FILE.write_text(json.dumps(data), encoding="utf-8")


def get_access_token(appid: str, appsecret: str, use_test: bool = False) -> str:
    """获取微信公众号 access_token，优先从缓存读取。"""
    cache = load_token_cache()
    cache_key = f"{appid}:token"
    now = time.time()

    # 检查缓存是否有效（提前 5 分钟刷新）
    if cache_key in cache:
        entry = cache[cache_key]
        if entry.get("expires_at", 0) > now + 300:
            return entry["token"]

    # 请求新 token
    if use_test:
        # 测试号接口
        url = (
            f"https://api.weixin.qq.com/cgi-bin/token"
            f"?grant_type=client_credential&appid={appid}&secret={appsecret}"
        )
    else:
        url = (
            f"https://api.weixin.qq.com/cgi-bin/token"
            f"?grant_type=client_credential&appid={appid}&secret={appsecret}"
        )

    try:
        resp = _api_get(url)
        data = json.loads(resp)
        if "access_token" in data:
            token = data["access_token"]
            expires_in = data.get("expires_in", 7200)
            cache[cache_key] = {
                "token": token,
                "expires_at": now + expires_in,
            }
            save_token_cache(cache)
            print(f"🔑 Access Token 已获取，有效期 {expires_in}s")
            return token
        else:
            errcode = data.get("errcode", "unknown")
            errmsg = data.get("errmsg", "unknown error")
            print(f"❌ 获取 access_token 失败: [{errcode}] {errmsg}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ 网络请求失败: {e}", file=sys.stderr)
        sys.exit(1)


# ============================================================
# 微信 API 调用封装
# ============================================================

def _api_get(url: str) -> str:
    """GET 请求。"""
    req = request.Request(url, method="GET")
    with request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _api_post(url: str, data: dict) -> dict:
    """POST 请求，返回解析后的 JSON。"""
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return json.loads(err_body)
        except Exception:
            return {"errcode": e.code, "errmsg": err_body}


# ============================================================
# 图片上传
# ============================================================

def upload_image_to_wechat(
    image_path: str, access_token: str
) -> str:
    """上传图片到微信「图文消息内的图片」素材，返回微信 URL。

    注意：这是临时素材接口，返回的 URL 可直接用于 draft content，
    不会被过滤。
    """
    if image_path.startswith(("http://", "https://")):
        # 已是远程 URL，无需上传
        print(f"   ⏭ 跳过远程图片: {image_path}")
        return image_path

    local_path = Path(image_path)
    if not local_path.exists():
        print(f"   ⚠ 图片不存在，跳过: {image_path}")
        return image_path

    url = (
        f"https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        f"?access_token={access_token}"
    )

    boundary = "----WeChatUploadBoundary"
    with open(local_path, "rb") as f:
        img_data = f.read()

    # 构造 multipart/form-data
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{local_path.name}"\r\n'
        f"Content-Type: image/{local_path.suffix.lstrip('.') or 'png'}\r\n\r\n"
    ).encode("utf-8") + img_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "url" in result:
                print(f"   ✅ 上传成功: {result['url']}")
                return result["url"]
            else:
                print(f"   ❌ 上传失败: {result.get('errmsg', 'unknown')}")
                return image_path
    except Exception as e:
        print(f"   ❌ 上传异常: {e}")
        return image_path


def process_images_in_html(html: str, access_token: str) -> str:
    """扫描 HTML 中的本地图片并上传到微信素材。"""
    import re

    def replacer(m):
        src = m.group(1)
        alt = m.group(2)
        if src.startswith(("http://", "https://")):
            return m.group(0)
        new_url = upload_image_to_wechat(src, access_token)
        return f'<img src="{new_url}" alt="{alt}" style="max-width:100%;height:auto;display:block;margin:12px auto;border-radius:4px;">'

    pattern = r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>'
    return re.sub(pattern, replacer, html)


# ============================================================
# 封面图→永久素材上传
# ============================================================

def upload_permanent_cover(
    image_path: str, access_token: str
) -> str:
    """上传封面图到微信「永久素材」库，返回 media_id。

    封面图必须作为永久素材上传（media/uploadimg 的临时 URL 不可用作
    thumb_media_id），使用 material/add_material 接口。

    图片要求：
      - 格式：jpg / png / gif
      - 大小：≤ 2MB（微信限制，500px 以内 ≤ 1MB）
      - 推荐尺寸：900×383 px（头条封面，2.35:1 比例）

    返回 media_id（字符串）。
    """
    local_path = Path(image_path)

    if not local_path.exists():
        print(f"❌ 封面图不存在: {image_path}", file=sys.stderr)
        sys.exit(1)

    # 检查格式
    ext = local_path.suffix.lower().lstrip(".")
    if ext not in ("jpg", "jpeg", "png", "gif"):
        print(f"⚠ 封面图格式建议为 jpg/png/gif，当前为 .{ext}，尝试继续...")

    # 检查大小
    file_size_mb = local_path.stat().st_size / (1024 * 1024)
    if file_size_mb > 2:
        print(f"⚠ 封面图过大 ({file_size_mb:.1f}MB)，微信限制 ≤ 2MB", file=sys.stderr)

    url = (
        f"https://api.weixin.qq.com/cgi-bin/material/add_material"
        f"?access_token={access_token}&type=image"
    )

    boundary = "----WxCoverUploadBoundary"
    with open(local_path, "rb") as f:
        img_data = f.read()

    # 构造 multipart/form-data（material/add_material 的 media 字段）
    mime_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
    }.get(ext, "image/png")

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{local_path.name}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8") + img_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )

    print(f"\n🖼 上传封面图到永久素材库...")
    print(f"   文件: {local_path.name} ({file_size_mb:.2f}MB)")

    try:
        with request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "media_id" in result:
                media_id = result["media_id"]
                print(f"   ✅ 封面已上传，media_id: {media_id}")
                # 同时打印 URL（如果有，便于确认）
                if "url" in result:
                    print(f"   🔗 URL: {result['url']}")
                return media_id
            else:
                errcode = result.get("errcode", "unknown")
                errmsg = result.get("errmsg", "unknown error")
                print(f"   ❌ 封面上传失败: [{errcode}] {errmsg}")
                if errcode == 40001:
                    print("   → access_token 无效，请检查配置")
                elif errcode == 40007:
                    print("   → 图片格式不支持，请转换为 jpg/png")
                elif errcode == 40009:
                    print("   → 图片过大，请压缩至 ≤ 2MB")
                return ""
    except Exception as e:
        print(f"   ❌ 上传异常: {e}")
        return ""


# ============================================================
# 切割图片检测与上传
# ============================================================

def find_split_images(html_path: Path) -> list:
    """根据 HTML 文件名自动查找对应的切割图片。

    命名规则：{html_stem}_01.png, {html_stem}_02.png, ...
    在同一目录下按序号排序。

    返回按序号排序的 Path 列表。
    """
    html_name = html_path.stem
    parent = html_path.parent

    # 匹配模式: {html_stem}_数字.png
    pattern = f"{html_name}_*.png"

    candidates = sorted(
        parent.glob(pattern),
        key=lambda p: p.stem  # 按文件名排序（含编号）
    )

    if not candidates:
        # 尝试在 output 子目录搜索
        candidates = sorted(
            parent.glob(f"**/{html_name}_*.png"),
            key=lambda p: p.stem
        )

    return candidates


def expand_image_files(pattern: str) -> list:
    """展开 glob 模式或逗号分隔的路径列表，返回排序后的 Path 列表。

    支持：
      - glob 模式："output/wuxia/*_0?.png"
      - 逗号分隔："a.png,b.png,c.png"
    """
    import glob

    paths = []
    if "," in pattern and not any(c in pattern for c in ["*", "?", "[", "]"]):
        # 逗号分隔的显式路径列表
        for part in pattern.split(","):
            part = part.strip()
            if part:
                paths.append(part)
    else:
        # glob 模式
        paths = glob.glob(pattern, recursive=True)

    # 去重、只保留存在的文件、按文件名排序
    seen = set()
    result = []
    for p in sorted(paths, key=lambda x: Path(x).name):
        pp = Path(p)
        if str(pp) not in seen and pp.exists() and pp.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif"):
            seen.add(str(pp))
            result.append(pp)

    return result


def build_images_html(image_urls: list) -> str:
    """将已上传的图片 URL 列表拼成微信图文正文 HTML。

    每张图片全宽显示，图片间无多余间距。
    """
    if not image_urls:
        return ""

    img_tags = "\n".join(
        f'<img src="{url}" style="max-width:100%;height:auto;display:block;margin:0;padding:0;border:0;">'
        for url in image_urls
    )

    html = f"""<section style="margin:0;padding:0;line-height:0;">{img_tags}</section>"""
    return html


def upload_images_and_build_html(
    image_paths: list, access_token: str
) -> str:
    """上传一组本地图片到微信素材库，返回拼接好的图片正文 HTML。

    参数：
      image_paths: Path 对象列表
      access_token: 微信 access_token

    返回：拼接好的纯图片 HTML 字符串
    """
    if not image_paths:
        print("\n❌ 未找到有效图片文件")
        return ""

    print(f"\n🔍 共 {len(image_paths)} 张图片：")
    for p in image_paths:
        print(f"   {p.name}")

    print(f"\n🖼 上传图片到微信素材库...")
    urls = []
    for p in image_paths:
        url = upload_image_to_wechat(str(p), access_token)
        urls.append(url)

    html = build_images_html(urls)
    print(f"   ✅ 正文图片 HTML 已生成，共 {len(urls)} 张")
    return html


def upload_and_replace_split_images(
    html_path: Path, access_token: str
) -> str:
    """检测并上传切割图片，返回拼接好的图片正文 HTML。

    流程：
      1. 根据 HTML 文件名查找同目录下 _01.png ~ _0N.png 切割图片
      2. 逐张上传到微信「图文消息内的图片」素材库
      3. 拼成全宽 <img> 序列 HTML
    """
    split_imgs = find_split_images(html_path)

    if not split_imgs:
        print(f"\n⚠ 未找到切割图片（匹配模式: {html_path.stem}_*.png），退回使用原始 HTML")  # 不会走到这里，仅在手动调用时提示
        return None

    print(f"\n🔍 检测到 {len(split_imgs)} 张切割图片：")
    for img in split_imgs:
        print(f"   {img.name}")

    print(f"\n🖼 上传切割图片到微信素材库...")
    urls = []
    for img in split_imgs:
        url = upload_image_to_wechat(str(img), access_token)
        urls.append(url)

    content_html = build_images_html(urls)
    print(f"   ✅ 正文图片 HTML 已生成，共 {len(urls)} 张")
    return content_html


# ============================================================
# 草稿箱推送
# ============================================================

def push_draft(
    access_token: str,
    title: str,
    content_html: str,
    author: str = "daner",
    digest: str = "",
    thumb_media_id: str = "",
    need_open_comment: int = 0,
    only_fans_can_comment: int = 0,
    content_source_url: str = "",
) -> dict:
    """推送图文到公众号草稿箱。

    参数：
      - title: 标题（≤32字）
      - content_html: 正文 HTML（≤2万字符，<1MB）
      - author: 作者（≤16字）
      - digest: 摘要（≤128字）
      - thumb_media_id: 封面图素材永久 MediaID
      - need_open_comment: 是否打开评论
      - only_fans_can_comment: 是否仅粉丝可评论
      - content_source_url: 阅读原文链接

    返回 API 响应 dict。
    """
    url = (
        f"https://api.weixin.qq.com/cgi-bin/draft/add"
        f"?access_token={access_token}"
    )

    article = {
        "article_type": "news",
        "title": title[:32],
        "author": author[:16],
        "content": content_html,
        "need_open_comment": need_open_comment,
        "only_fans_can_comment": only_fans_can_comment,
    }

    if digest:
        article["digest"] = digest[:128]
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
    if content_source_url:
        article["content_source_url"] = content_source_url[:1024]

    payload = {"articles": [article]}

    print(f"\n📤 正在推送到草稿箱...")
    print(f"   标题: {title}")
    print(f"   作者: {author}")
    print(f"   正文长度: {len(content_html)} 字符")

    result = _api_post(url, payload)
    return result


def auto_generate_digest(html: str, max_len: int = 54) -> str:
    """从 HTML 正文中自动提取摘要（前 54 个字）。"""
    import re
    # 去除 HTML 标签
    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"\s+", "", text)
    return text[:max_len]


# ============================================================
# CLI 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="推送内容到微信公众号草稿箱。支持三种模式：① HTML 正文模式 ② --use-split-images 自动检测切割图片 ③ --image-files 指定已有图片"
    )
    parser.add_argument("input", nargs="?", default=None, help="输入的 .html 文件路径（--image-files 模式下可选）")
    parser.add_argument("--config", "-c", default=None, help="微信配置文件路径")
    parser.add_argument("--title", "-t", default=None, help="文章标题（必填，≤32字）")
    parser.add_argument("--author", "-a", default=None, help="作者名（默认从配置读取）")
    parser.add_argument("--digest", "-d", default=None, help="摘要（不填则自动提取前54字）")
    parser.add_argument(
        "--cover-image", "-v",
        default=None,
        help="封面图路径（推荐 900×383 px），将上传到永久素材库并设置为封面",
    )
    parser.add_argument(
        "--upload-images",
        action="store_true",
        help="上传 HTML 中的本地图片到微信素材库并替换 URL（HTML 模式）",
    )
    parser.add_argument(
        "--use-split-images",
        action="store_true",
        help="自动检测切割后的截图（{html_stem}_01.png ...）作为正文，上传到微信素材库",
    )
    parser.add_argument(
        "--image-files", "-f",
        default=None,
        help="直接指定已有截图作为正文。支持 glob 模式（如 'output/wuxia/*_0?.png'）或逗号分隔路径列表。此模式下 --title 必填。",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="上传成功后立即发布（默认仅存入草稿箱）",
    )
    args = parser.parse_args()

    # 0) 校验参数
    if not args.image_files and not args.input:
        print("❌ 请提供输入文件或使用 --image-files 指定图片", file=sys.stderr)
        sys.exit(1)
    if not args.title:
        print("❌ 必须提供文章标题（--title）", file=sys.stderr)
        sys.exit(1)

    # 1) 加载配置
    cfg = load_config(args.config)
    appid, appsecret, use_test = get_wechat_creds(cfg)
    upload_cfg = cfg.get("upload", {})

    # 2) 确定内容来源
    title = args.title
    content_html = ""
    digest = args.digest or ""
    html_path = None

    if args.image_files:
        # ========== 模式 A：直接指定已有图片 ==========
        print(f"\n📸 图片直传模式：{args.image_files}")
        image_paths = expand_image_files(args.image_files)
        if not image_paths:
            print(f"❌ 未匹配到任何图片文件: {args.image_files}", file=sys.stderr)
            sys.exit(1)
        # 此模式下 digest 自动生成
        if not digest:
            digest = f"一张图搞懂 {title}"
    else:
        # ========== 模式 B：HTML 正文 / --use-split-images ==========
        html_path = Path(args.input)
        if not html_path.exists():
            print(f"❌ 文件不存在: {html_path}", file=sys.stderr)
            sys.exit(1)
        content_html = html_path.read_text(encoding="utf-8")

        # 尝试从 HTML 提取标题
        if not title:
            import re
            m = re.search(r"<title>(.+?)</title>", content_html)
            if m:
                title = m.group(1)
            if not title:
                m = re.search(r"<h1[^>]*>(.+?)</h1>", content_html)
                if m:
                    title = re.sub(r"<[^>]+>", "", m.group(1))
            if not title:
                print("❌ 无法自动检测标题，请用 --title 指定", file=sys.stderr)
                sys.exit(1)

        if not digest:
            digest = auto_generate_digest(content_html)

    author = args.author or upload_cfg.get("default_author", "daner")
    need_open_comment = upload_cfg.get("need_open_comment", 0)
    only_fans_can_comment = upload_cfg.get("only_fans_can_comment", 0)

    # 4) 获取 access_token
    token = get_access_token(appid, appsecret, use_test)

    # 5) 上传封面图（可选）
    thumb_media_id = ""
    if args.cover_image:
        thumb_media_id = upload_permanent_cover(args.cover_image, token)
        if not thumb_media_id:
            print("⚠ 封面图上传失败，将在不设置封面的情况下继续推送...")

    # 6) 构建正文内容
    if args.image_files:
        # 模式 A：上传已有图片 → 构建纯图片 HTML
        content_html = upload_images_and_build_html(image_paths, token)
        if not content_html:
            print("❌ 图片上传后无法构建正文 HTML", file=sys.stderr)
            sys.exit(1)
    elif args.use_split_images and html_path:
        # 模式 B-2：自动检测切割图片
        split_html = upload_and_replace_split_images(html_path, token)
        if split_html:
            content_html = split_html

    # 7) 上传 HTML 中内嵌的本地图片（仅 HTML 模式，--upload-images）
    if args.upload_images and content_html:
        print("\n🖼 上传本地图片到微信素材库...")
        content_html = process_images_in_html(content_html, token)

    # 8) 推送到草稿箱
    result = push_draft(
        access_token=token,
        title=title,
        content_html=content_html,
        author=author,
        digest=digest,
        thumb_media_id=thumb_media_id,
        need_open_comment=need_open_comment,
        only_fans_can_comment=only_fans_can_comment,
    )

    if "media_id" in result:
        media_id = result["media_id"]
        print(f"\n✅ 草稿创建成功！")
        print(f"   Media ID: {media_id}")
        if thumb_media_id:
            print(f"   封面: ✅ 已设置（media_id: {thumb_media_id}）")
        else:
            print(f"   封面: ⚠ 未设置，请在后台手动上传")
        print(f"   可在公众号后台「草稿箱」中查看和编辑。")
    else:
        errcode = result.get("errcode", "unknown")
        errmsg = result.get("errmsg", "unknown error")
        print(f"\n❌ 草稿创建失败: [{errcode}] {errmsg}")
        if errcode == 40001:
            print("   → access_token 无效，尝试清除缓存后重试")
            TOKEN_CACHE_FILE.unlink(missing_ok=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

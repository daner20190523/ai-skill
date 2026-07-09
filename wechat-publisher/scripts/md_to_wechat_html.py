#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown → 微信公众号兼容 HTML 转换器

功能：
- 将 Markdown 渲染为 HTML
- 所有样式转为内联 style（微信不支持 <style> 标签和外部 CSS）
- 代码块高亮
- 表格自动美化

用法：
  python md_to_wechat_html.py <input.md> [--output <output.html>] [--config <config.yaml>]
"""

import argparse
import re
import sys
from pathlib import Path

# ============================================================
# 微信兼容内联样式定义（优化版 - 兼容微信公众号）
# ============================================================

WECHAT_STYLES = {
    # 正文段落
    "p": "font-size:16px;color:#333333;line-height:2;margin:0 0 20px 0;word-break:break-all;",
    # 标题
    "h1": "font-size:24px;font-weight:bold;color:#ffffff;line-height:1.5;margin:30px 0 20px 0;text-align:center;padding:18px 20px;background-color:#1a73e8;border-radius:6px;",
    "h2": "font-size:20px;font-weight:bold;color:#1a73e8;line-height:1.5;margin:28px 0 16px 0;padding:10px 16px;background-color:#e8f0fe;border-left:6px solid #1a73e8;",
    "h3": "font-size:18px;font-weight:bold;color:#333333;line-height:1.5;margin:24px 0 14px 0;padding:8px 12px;background-color:#f8f9fa;border-left:4px solid #4285f4;",
    "h4": "font-size:16px;font-weight:bold;color:#555555;line-height:1.5;margin:20px 0 12px 0;padding-left:10px;",
    # 引用块
    "blockquote": "font-size:15px;color:#666666;line-height:1.8;margin:20px 0;padding:16px 20px;background-color:#f8f9fa;border-left:4px solid #4285f4;",
    # 代码块
    "code_block": "font-size:14px;font-family:Menlo,Monaco,Consolas,'Courier New',monospace;line-height:1.6;color:#f8f8f2;background-color:#282c34;padding:16px 20px;margin:20px 0;border-radius:4px;border:1px solid #44475a;",
    # 行内代码
    "inline_code": "font-size:14px;font-family:Menlo,Monaco,Consolas,'Courier New',monospace;color:#e06c75;background-color:#f0f0f0;padding:2px 6px;border-radius:3px;",
    # 列表
    "ul": "font-size:16px;color:#333333;line-height:2;margin:16px 0;padding-left:24px;",
    "ol": "font-size:16px;color:#333333;line-height:2;margin:16px 0;padding-left:24px;",
    "li": "margin:6px 0;",
    # 表格
    "table": "width:100%;border-collapse:collapse;margin:24px 0;font-size:15px;color:#333333;line-height:1.6;",
    "th": "background-color:#4285f4;font-weight:bold;text-align:left;padding:12px 14px;border:1px solid #3367d6;color:#ffffff;",
    "td": "padding:10px 14px;border:1px solid #dddddd;background-color:#ffffff;",
    # 分隔线
    "hr": "border:none;border-top:2px solid #4285f4;margin:32px 0;",
    # 链接
    "a": "color:#4285f4;text-decoration:none;",
    # 加粗/强调
    "strong": "font-weight:bold;color:#333333;",
    "em": "font-style:italic;color:#666666;",
    # 图片
    "img": "max-width:100%;height:auto;display:block;margin:20px auto;",
    # 删除线
    "del": "text-decoration:line-through;color:#999999;",
}


def html_inline_style(tag: str, styles: dict) -> str:
    """给 HTML 标签注入内联样式。"""
    if tag in styles:
        return f'style="{styles[tag]}"'
    return ""


def escape_html(text: str) -> str:
    """HTML 转义。"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def markdown_to_wechat_html(md_text: str, styles: dict = None) -> dict:
    """将 Markdown 文本转换为微信公众号兼容的 HTML。"""
    if styles is None:
        styles = WECHAT_STYLES

    lines = md_text.split("\n")
    result = []
    in_code_block = False
    code_lines = []
    code_lang = ""
    title = ""

    def parse_inline(text: str) -> str:
        """解析行内 Markdown 语法。"""
        text = escape_html(text)
        # 图片
        text = re.sub(
            r"!\[([^\]]*)\]\(([^)\s]+)\)",
            lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" style="{styles["img"]}">',
            text,
        )
        # 链接
        text = re.sub(
            r"\[([^\]]+)\]\(([^)\s]+)\)",
            lambda m: f'<a href="{m.group(2)}" style="{styles["a"]}">{m.group(1)}</a>',
            text,
        )
        # 粗体
        text = re.sub(
            r"\*\*(.+?)\*\*",
            lambda m: f'<strong style="{styles["strong"]}">{m.group(1)}</strong>',
            text,
        )
        # 行内代码
        text = re.sub(
            r"`([^`]+)`",
            lambda m: f'<code style="{styles["inline_code"]}">{m.group(1)}</code>',
            text,
        )
        return text

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 代码块
        if stripped.startswith("```"):
            if in_code_block:
                # 结束代码块
                code = "\n".join(code_lines)
                escaped_code = escape_html(code)
                result.append(
                    f'<section style="{styles["code_block"]}"><pre>{escaped_code}</pre></section>'
                )
                code_lines = []
                code_lang = ""
                in_code_block = False
            else:
                # 开始代码块
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # 空行
        if not stripped:
            i += 1
            continue

        # 标题
        h_match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if h_match:
            level = len(h_match.group(1))
            content = parse_inline(h_match.group(2))
            tag = f"h{level}"
            if tag in styles:
                result.append(f"<{tag} {html_inline_style(tag, styles)}>{content}</{tag}>")
            if title == "" and level == 1:
                title = h_match.group(2)
            i += 1
            continue

        # 引用
        if stripped.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = "<br>".join(parse_inline(l) for l in quote_lines)
            result.append(f'<blockquote style="{styles["blockquote"]}">{quote_text}</blockquote>')
            continue

        # 列表
        ul_match = re.match(r"^[\-\*\+]\s+(.+)$", stripped)
        ol_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ul_match or ol_match:
            list_lines = []
            list_tag = "ul" if ul_match else "ol"
            while i < len(lines):
                l_stripped = lines[i].strip()
                if re.match(r"^[\-\*\+]\s+(.+)$", l_stripped) or re.match(r"^\d+\.\s+(.+)$", l_stripped):
                    content = re.sub(r"^[\-\*\+\d\.]+\s+", "", l_stripped)
                    list_lines.append(parse_inline(content))
                    i += 1
                else:
                    break
            result.append(f'<{list_tag} style="{styles[list_tag]}">')
            for item in list_lines:
                result.append(f'<li style="{styles["li"]}">{item}</li>')
            result.append(f"</{list_tag}>")
            continue

        # 表格
        if "|" in stripped and stripped.startswith("|"):
            table_rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                row_stripped = lines[i].strip()
                # 跳过分隔行
                if re.match(r"^\|[\s\-:]*\|", row_stripped):
                    i += 1
                    continue
                cells = [c.strip() for c in row_stripped.strip("|").split("|")]
                parsed_cells = [parse_inline(c) for c in cells]
                table_rows.append(parsed_cells)
                i += 1
            if table_rows:
                result.append(f'<table style="{styles["table"]}">')
                # 表头
                result.append("<tr>")
                for cell in table_rows[0]:
                    result.append(f'<th style="{styles["th"]}">{cell}</th>')
                result.append("</tr>")
                # 表身
                for idx, row in enumerate(table_rows[1:], start=0):
                    bg = "#ffffff" if idx % 2 == 0 else "#f8f9fa"
                    result.append(f'<tr style="background-color:{bg};">')
                    for cell in row:
                        result.append(f'<td style="{styles["td"]}">{cell}</td>')
                    result.append("</tr>")
                result.append("</table>")
            continue

        # 分隔线
        if re.match(r"^(\*{3,}|-{3,}|_{3,})\s*$", stripped):
            result.append(f'<hr style="{styles["hr"]}">')
            i += 1
            continue

        # 普通段落
        result.append(f'<p style="{styles["p"]}">{parse_inline(stripped)}</p>')
        i += 1

    return {
        "html": "\n".join(result),
        "title": title,
    }


def main():
    parser = argparse.ArgumentParser(description="Markdown → 微信公众号兼容 HTML 转换器")
    parser.add_argument("input", help="输入的 .md 文件路径")
    parser.add_argument("--output", "-o", help="输出的 .html 文件路径")
    parser.add_argument("--wrap", action="store_true", help="包裹完整的 HTML 文档（含 <html><head><body>）")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[错误] 文件不存在: {input_path}")
        sys.exit(1)

    md_text = input_path.read_text(encoding="utf-8")
    result = markdown_to_wechat_html(md_text)
    html_body = result["html"]
    title = result["title"]

    # 添加上下文包裹
    if args.wrap:
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>{title}</title>
</head>
<body style="margin:0;padding:0;background-color:#f7fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;">
<div style="max-width:680px;margin:20px auto;padding:32px 28px;background-color:#ffffff;border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
{html_body}
</div>
</body>
</html>"""
    else:
        html = html_body

    # 输出
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(html, encoding="utf-8")
        print(f"[完成] 已生成 HTML: {out_path}")
    else:
        print(html)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
save_analysis.py — 底层逻辑洞察专家 · 增长学习沉淀助手

功能：
  1. 将完整分析产物（markdown 文本或文件）写入当前工作区：
       底层逻辑_{topic}_{YYYYMMDD}.md
  2. 向技能 references/knowledge_base.md 追加一条索引条目（在 ENTRY_START/ENTRY_END 标记之间），
     实现"每次分析自动沉淀，下次复用"的增长学习闭环。

用法：
  # 直接传入完整 markdown 内容
  python save_analysis.py --topic "短视频算法" --domain "industry" \
      --frameworks "供需,激励,系统动力学" --judgment "算法优化停留→广告库存↑→收入↑，但内容劣化负反馈积累" \
      --tags "内容平台,算法,注意力经济" --content-file "analysis.md" \
      --workspace "d:/IdeaProjects/ai-skill-2" \
      --kb "d:/.../references/knowledge_base.md"

  # 仅做知识库沉淀（完整 md 已由调用者用 write_to_file 写入工作区）
  python save_analysis.py --topic "..." --domain "industry" --frameworks "..." \
      --judgment "..." --tags "..." --kb ".../knowledge_base.md"

参数：
  --topic        主题（用于文件名与索引标题），必填
  --domain       领域：verbal | industry | codebase，必填
  --frameworks   使用的透镜，逗号分隔，必填
  --judgment     一句话核心判断，必填
  --tags         标签，逗号分隔，可选
  --content-file 完整分析 md 路径；若提供则复制到工作区产物文件，可选
  --workspace    工作区绝对路径；省略则取当前目录，可选
  --kb           knowledge_base.md 绝对路径；省略则取脚本旁 references/knowledge_base.md，可选
  --date         自定义日期 YYYYMMDD；省略则用今天，可选
"""

import argparse
import datetime
import os
import sys


def parse_args():
    p = argparse.ArgumentParser(description="底层逻辑分析沉淀助手")
    p.add_argument("--topic", required=True)
    p.add_argument("--domain", required=True, choices=["verbal", "industry", "codebase"])
    p.add_argument("--frameworks", required=True)
    p.add_argument("--judgment", required=True)
    p.add_argument("--tags", default="")
    p.add_argument("--content-file", default="")
    p.add_argument("--workspace", default=os.getcwd())
    p.add_argument("--kb", default="")
    p.add_argument("--date", default="")
    return p.parse_args()


def main():
    args = parse_args()

    # 日期
    if args.date:
        ymd = args.date
    else:
        ymd = datetime.date.today().strftime("%Y%m%d")

    # 知识库路径
    if args.kb:
        kb_path = os.path.abspath(args.kb)
    else:
        kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "references", "knowledge_base.md")
    kb_path = os.path.abspath(kb_path)

    # 1) 写入工作区产物
    if args.content_file and os.path.isfile(args.content_file):
        ws = os.path.abspath(args.workspace)
        os.makedirs(ws, exist_ok=True)
        dest = os.path.join(ws, "底层逻辑_{}_{}.md".format(args.topic, ymd))
        with open(args.content_file, "r", encoding="utf-8") as f:
            data = f.read()
        with open(dest, "w", encoding="utf-8") as f:
            f.write(data)
        print("[save_analysis] 产物已写入: {}".format(dest))
    else:
        print("[save_analysis] 未提供 --content-file，跳过工作区产物写入（假设已由调用者写入）。")

    # 2) 追加知识库索引
    if not os.path.isfile(kb_path):
        print("[save_analysis] 警告：知识库文件不存在: {}".format(kb_path))
        return

    with open(kb_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 统计已有条目数量（以 "### " 开头且位于 ENTRY 区之后）
    entry_count = 0
    in_entries = False
    for ln in lines:
        if "ENTRY_START" in ln:
            in_entries = True
            continue
        if "ENTRY_END" in ln:
            in_entries = False
            continue
        if in_entries and ln.startswith("### "):
            entry_count += 1

    new_idx = entry_count + 1
    today = datetime.date.today().strftime("%Y-%m-%d")
    tags_str = args.tags if args.tags else "未分类"
    entry = (
        "### {}. {}\n".format(new_idx, args.topic)
        + "- 领域：`{}`\n".format(args.domain)
        + "- 日期：{}\n".format(today)
        + "- 透镜：`{}`\n".format(args.frameworks)
        + "- 核心判断：{}\n".format(args.judgment)
        + "- 标签：`{}`\n\n".format(tags_str)
    )

    # 插入到 ENTRY_END 之前
    out = []
    inserted = False
    for ln in lines:
        if "ENTRY_END" in ln and not inserted:
            out.append(entry)
            inserted = True
        out.append(ln)

    with open(kb_path, "w", encoding="utf-8") as f:
        f.writelines(out)

    print("[save_analysis] 知识库已追加第 {} 条: {}".format(new_idx, args.topic))
    print("[save_analysis] 知识库路径: {}".format(kb_path))


if __name__ == "__main__":
    main()

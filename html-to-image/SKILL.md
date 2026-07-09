---
name: html-to-image
description: HTML 知识卡片截图管线。将 HTML 渲染为 PNG 长图 → 切割为适合公众号的多段图片。上游技能 @skill://tech-knowledge-card 生成 HTML，本技能负责截图+切割，下游 @skill://wechat-publisher 负责推送到公众号草稿箱。触发词："截图""切割""html转png""生成图片""切图"。
---

# HTML to Image — 知识卡片截图管线

## 定位

本技能是 **tech-knowledge-card 的截图管线技能**，负责将已生成的 HTML 知识卡片渲染为 PNG 长图并切割分段。**不负责内容生成和公众号推送**，只负责截图+切割。上游内容由 `@skill://tech-knowledge-card` 生成，下游推送由 `@skill://wechat-publisher` 负责。

## 是什么

将技术知识卡片 HTML 转换为适合公众号分享的 PNG 图片。包含三步：HTML 渲染截图 → 长图切割分段 → CSS 提取/内联辅助。

## 核心流程

```
HTML 知识卡片
     │
     ├─→ [extract_css.py]     ← CSS 提取/内联（可选预处理）
     │
     └─→ [html_to_png.py]     ← HTML → PNG 长图（Playwright, 420px宽度, 2x scale）
              │
              └─→ [split_image.py]   ← 长图切割（每段 ~1500px）
                       │
                       └─→ 切割完成 → 交给 @skill://wechat-publisher 推送
```

---

## 脚本详解

### 1. `html_to_png.py` — HTML → PNG 长图截图

使用 **Playwright** 将 HTML 文件渲染为高质量 PNG 长图。

```bash
python scripts/html_to_png.py input.html output.png --width 420 --scale 2
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input.html` | 必填 | 输入的 HTML 文件路径 |
| `output.png` | 必填 | 输出的 PNG 文件路径 |
| `--width` | `420` | 截图固定宽度（px），匹配移动端卡片设计 |
| `--scale` | `2` | 设备像素比（1x / 2x），2x 输出 840px 保清晰度 |

**依赖**：
```bash
pip install playwright && playwright install chromium
```

**关键规则**：
- HTML 的 CSS 必须已内联（`<style>` 块中），脚本不会自动提取外部 CSS
- 生成前用 `extract_css.py` 将外部 `<link>` 替换为内联 `<style>`
- 输出 PNG 为全页长图，高度由 HTML 内容自动决定

---

### 2. `split_image.py` — 长图切割

将 `html_to_png.py` 生成的 PNG 长图切割成多段，适配微信公众号上传。

```bash
python scripts/split_image.py input.png
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input.png` | 必填 | 输入的长图 PNG 文件 |
| `--height` | `1500` | 每段高度（px），微信公众号单图推荐 ≤ 1500px |
| `--output-dir` | 同目录 | 切割图输出目录（默认同输入目录） |

**输出命名**：`原文件名_00.png`, `原文件名_01.png`, `原文件名_02.png` ...

**依赖**：
```bash
pip install Pillow
```

---

### 3. `extract_css.py` — CSS 提取/内联工具

CSS 与 HTML 模板分离和合并的辅助工具。两种模式：

**模式 A：提取（分离）**
```bash
python scripts/extract_css.py extract card_template.html css/editorial.css
```
从 HTML 中提取 `<style>` 块 → 保存为独立 `.css` 文件，原位置替换为 `<link rel="stylesheet" href="...">`。

**模式 B：内联（合并）**
```bash
python scripts/extract_css.py inline card_template.html
```
将 `<link rel="stylesheet" href="...">` 替换为 `<style>/* CSS 内容 */</style>`，保证截图自包含。

**模板与 CSS 映射**：

| HTML 模板 | CSS 样式文件 |
|-----------|-------------|
| `card_template_wuxia.html` | `wuxia.css` |
| `card_template_wuxia_conquest.html` | `wuxia_conquest.css` |
| `card_template_wuxia_pipeline.html` | `wuxia_pipeline.css` |
| `card_template_newspaper.html` | `newspaper.css` |

---

## 文件结构

```
html-to-image/
├── SKILL.md                    ← 本文件（主入口）
└── scripts/
    ├── html_to_png.py          ← HTML → PNG 长图截图（Playwright, 固定宽度 420px）
    ├── split_image.py          ← 长图切割（每段 ~1500px, 适配公众号上传）
    └── extract_css.py          ← CSS 提取/内联工具（分离或内联样式块）
```

## 依赖

```bash
pip install Pillow playwright
playwright install chromium
```

## 上下游协作

```
@skill://tech-knowledge-card  → 生成 HTML 知识卡片
        │
        └─→ @skill://html-to-image  → 截图 PNG + 切割
                 │
                 └─→ @skill://wechat-publisher  → 推送到公众号草稿箱
```

> 本技能不依赖 wechat-publisher，可独立使用。切割产物的推送由 `@skill://wechat-publisher` 的 `--image-files` 模式完成。

## 常见问题

**Q: 截图中文乱码/缺字？**
A: 确保系统中已安装所需中文字体。Playwright 使用系统字体渲染。

**Q: 截图宽度选择？**
A: 默认 420px 匹配微信公众号移动端阅读宽度。`--scale 2` 输出实际 840px 保证 Retina 清晰度。不要修改宽度，否则切割和推送效果不一致。

**Q: 图片太大超出微信限制？**
A: 微信要求单图 ≤ 10MB，格式 jpg/png/gif。长图切割为 1500px 段已保证合规。

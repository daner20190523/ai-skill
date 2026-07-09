---
name: wechat-publisher
description: 微信公众号图文发布技能。将卡片图片/HTML 推送到公众号草稿箱。支持两种模式：① 切割图片直传（--image-files，推荐，保留完整视觉效果）② HTML 纯内联样式直推（微信兼容，文字可选中代码可复制）。含 AI 封面图生成（极简风 900×383）、草稿箱推送全流程。上游：@skill://tech-knowledge-card 生成 HTML → @skill://html-to-image 截图切割 → 本技能推送到公众号。触发词："上传公众号""发布到微信""推送到草稿箱""直接发公众号图文""公众号封面""生成封面图"。
---

# WeChat Publisher — 微信公众号图文发布技能

## 定位

本技能是 **tech-knowledge-card 的下游发布技能**，负责将截图/HTML 推送到微信公众号草稿箱。**不负责内容撰写和截图切割**，只负责推送+封面图生成。上游内容由 `@skill://tech-knowledge-card` 生成，截图切割由 `@skill://html-to-image` 负责。

## 是什么

将技术知识卡片内容发布到微信公众号草稿箱。上游截图管线 `@skill://html-to-image` 产出切割图片后，由本技能负责推送到公众号。

## 两种发布模式

| 模式 | 触发词 | 原理 | 视觉效果 | 文字可复制 |
|------|--------|------|----------|-----------|
| **图片直传**（推荐） | "上传公众号""发布到微信" | 切割 PNG → 微信 CDN → 图片 HTML | ✅ 完整保留 | ❌ |
| **HTML 直推** | "直接发公众号图文""可复制文字" | 纯内联样式 HTML → 草稿箱 | ✅ 基本保留 | ✅ |

> **核心原则**：图片直传完整保留所有设计细节（宣纸纹理、CSS 变量、特殊字体），微信不裁剪；HTML 直推所有样式写在 `style=""` 属性里，不用 `<style>` 块，绕过微信过滤。

## 模式 A：切割图片直传（`--image-files`）

**无需 HTML 文件，不重新生成，直接上传已有截图。**

```bash
python scripts/push_to_wechat_draft.py \
  --image-files "output/wuxia/Redis_*_0*.png" \
  --title "Redis 武林秘籍：内存为丹田、单线程为心法" \
  --author "daner" \
  --cover-image output/wuxia/Redis_cover.png
```

| 参数 | 说明 |
|------|------|
| `--image-files` / `-f` | 切割图片的 glob 模式或逗号分隔路径列表 |
| `--title` / `-t` | 文章标题（≤32 字，营销标题） |
| `--author` / `-a` | 作者名（默认从配置读取） |
| `--digest` / `-d` | 摘要（不填则自动生成） |
| `--cover-image` / `-v` | 封面图路径（900×383 px） |
| `--config` / `-c` | 配置文件路径 |

## 模式 B：HTML 纯内联样式直推

**适用于武侠风公众号图文，文字可选中、代码可复制。**

### 微信安全清单（必须遵守）

| 禁用项 | 原因 | 替代方案 |
|--------|------|----------|
| `<style>` 块 | 微信可能直接删除 | 所有样式写 `style=""` |
| `position: absolute/relative` | 被过滤 | 用 `table` / 流式布局 / 负 margin |
| `::before` / `::after` | 伪元素直接消失 | 用真实 `<span>` / `<div>` |
| `float: left/right` | 微信中不可靠 | 用 `<table>` 做网格布局 |
| `display: flex` | 部分场景失效 | 小范围可试，复杂布局用 `<table>` |

### 模板变量

基于 `assets/card_template_wx_article_wuxia.html` 模板：

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ARTICLE_TITLE}}` | `<title>` 标签标题 | `Transformer 武林秘籍` |
| `{{KICKER}}` | 卷首封印文字 | `武林秘籍` |
| `{{TITLE}}` | 正标题 | `Transformer：从逐字苦修到一眼万里` |
| `{{DECK}}` | 副标题 | `八位谷歌大侠...` |
| `{{AUTHOR_NAME}}` | 作者署名 | `daner技术栈` |
| `{{QR_CODE_IMAGE}}` | 页脚二维码路径 | `../assets/qrcode_wechat.jpg` |
| `{{TECH_JIANGHU_LINK}}` | "我的技术江湖"博客链接 | `https://daner20190523.github.io/blog/` |
| `{{SEAL_TEXT}}` | 印章文字（2-4字） | `关注` |
| `{{STORYTELLER_INTRO}}` | 说书人开场白 | 古风开场段落 |
| `{{CHAPTER_WHAT/WHY/HOW/PROBLEMS_HEADER}}` | 四回标题区域 HTML | |
| `{{CHAPTER_WHAT_BODY}}` 等 | 四回正文 | |
| `{{ILLO_WHAT/WHY/HOW/PROBLEMS}}` | 墨小颠配图 HTML | `<img>` + caption |
| `{{ANALOGY}}` / `{{TIMELINE_ITEMS}}` / `{{FEATURE_CARDS}}` 等 | 内容组件 | 见模板 |

### 推送命令

```bash
python scripts/push_to_wechat_draft.py \
  "output/wuxia/{技术名词}_{时间戳}_wx_article_wuxia.html" \
  --upload-images \
  --title "{营销标题}" \
  --author "daner" \
  --cover-image "output/wuxia/{技术名词}_{时间戳}_cover.png"
```

`--upload-images` 自动：扫描 HTML 中 `<img src="…">` → 本地路径上传到微信 CDN → 替换为微信 URL。

### 我的技术江湖（博客引流板块）

```html
<div style="margin:0;padding:32px 24px;background-color:#faf5ed;border-top:2px dashed #e0d6c0;border-bottom:2px dashed #e0d6c0;text-align:center;">
  <span style="display:block;font-size:10px;letter-spacing:14px;color:#b8943e;opacity:0.6;margin-bottom:18px;">◆ ◇ ◆</span>
  <span style="display:inline-block;padding:3px 18px;font-size:10px;font-weight:700;letter-spacing:4px;color:#c43a31;border:1px solid rgba(196,58,49,0.3);margin-bottom:14px;">归 隐 之 地</span>
  <div style="font-family:'Noto Serif SC','STSong','Songti SC',serif;font-size:24px;font-weight:800;color:#1a1410;margin-bottom:8px;letter-spacing:3px;">我的技术江湖</div>
  <p style="font-size:13px;color:#8a8070;margin:0 0 20px;line-height:1.8;">更多武林秘籍、独门绝技，尽在江湖客栈</p>
  <a href="{{TECH_JIANGHU_LINK}}" style="display:inline-block;padding:12px 36px;font-family:'KaiTi','STKaiti','楷体',serif;font-size:16px;font-weight:600;color:#ffffff;background-color:#c43a31;border-radius:4px;text-decoration:none;letter-spacing:3px;box-shadow:0 2px 8px rgba(196,58,49,0.25);">踏入江湖 →</a>
  <span style="display:block;font-size:10px;color:#b5aea0;margin-top:14px;letter-spacing:0.3px;word-break:break-all;">{{TECH_JIANGHU_LINK}}</span>
</div>
```

## AI 封面图生成

### 规格

| 类型 | 尺寸 | 比例 |
|------|------|------|
| 头条封面 | 900×383 px | 2.35:1 |
| 次条封面 | 200×200 px | 1:1 |

### 生成流程（3 步）

**步骤 1**：构建 AI Prompt

```bash
python scripts/generate_cover_image.py prompt "{技术名词}" --style minimalist --palette tech
```

**8 套配色方案**：

| 配色 ID | 描述 | 适用场景 |
|---------|------|----------|
| `tech` | 深海蓝→极光青 + 霓虹光晕 | 技术深度文 |
| `warm` | 暖米白 + 焦糖棕 + 炭灰 | 经验分享 |
| `dark` | 纯黑 + 香槟金 + 珍珠白 | 架构设计 |
| `clean` | 素雪白 + 雾松绿 + 薄荷绿 | 入门教程 |
| `cyber` | 深空紫 + 霓虹粉 + 电光青 | AI 相关 |
| `art` | 莫兰迪灰粉 + 雾霾蓝 + 奶油白 | 设计/创意 |
| `nature` | 森林绿 + 琥珀金 + 象牙白 | 区块链/分布式 |
| `sunset` | 暮色紫 + 落日橙 + 云朵白 | 前端/UI |

**步骤 2**：AI 生图（调用 `image_gen` 生成 1024×1024）

**步骤 3**：裁剪到 900×383

```bash
python scripts/generate_cover_image.py crop -i raw.png -o cover.png
python scripts/generate_cover_image.py crop -i raw.png -o cover --both-sizes  # 头条+次条
```

## 配置

复制 `config/wechat_config.template.yaml` 为 `wechat_config.secret.yaml`，填入真实密钥：

```yaml
wechat:
  appid: "你的 AppID"
  appsecret: "你的 AppSecret"
  use_test_account: 0

upload:
  auto_publish: 0
  default_author: "daner技术栈"
```

## 上下游协作

```
@skill://tech-knowledge-card  → 生成 HTML 知识卡片
        │
        └─→ @skill://html-to-image  → 截图 PNG + 切割
                 │
                 └─→ @skill://wechat-publisher  → 推送到公众号草稿箱
```

> 截图切割（html_to_png.py / split_image.py / extract_css.py）已拆分至独立技能 `@skill://html-to-image`。

## 依赖

```bash
pip install pyyaml Pillow
# HTML 直推模式额外需要：
pip install pygments
```

## 文件结构

```
wechat-publisher/
├── SKILL.md                           ← 本文件（主入口）
├── scripts/
│   ├── push_to_wechat_draft.py        ← 草稿箱推送（图片直传 + HTML 直推 + 封面上传）
│   ├── generate_cover_image.py        ← AI 封面图 prompt 生成 + 裁剪（900×383）
│   └── md_to_wechat_html.py           ← Markdown → 微信兼容 HTML（Pygments 代码高亮）
├── config/
│   └── wechat_config.template.yaml    ← 微信配置模板（需复制并填入真实密钥）
└── assets/
    ├── card_template_wx_article_wuxia.html  ← 武侠风纯内联样式 HTML 模板
    └── qrcode_wechat.jpg                    ← 页脚公众号二维码
```

## 常见问题

**Q: 只有切割图片，没有 HTML 文件怎么办？**
A: 使用 `--image-files` 模式，不需要 HTML 文件。只需提供 `--title`。

**Q: access_token 失效怎么办？**
A: 脚本自动缓存 token，提前 5 分钟刷新。遇 `40001` 错误自动清除缓存重试。

**Q: 图片上传失败？**
A: 微信要求格式 jpg/png/gif，大小 ≤ 10MB。确认配置中 appid/appsecret 正确。

**Q: 封面图需要什么规格？**
A: 头条封面推荐 900×383 px（2.35:1）。使用 `generate_cover_image.py` 自动裁剪。

**Q: 想重新上传之前的文章？**
A: 直接使用 `--image-files` 指定之前的切割图片路径，几秒完成上传。

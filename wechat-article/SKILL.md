---
name: wechat-article
description: 武侠风微信公众号图文直传模式（非截图）——将风格化 HTML 内容直接推送到公众号草稿箱作为图文消息，保留武侠秘籍排版、朱砂金玉配色、墨小颠配图等全部视觉元素，读者可在公众号内直接阅读排版精美的长文，文字可选中、代码可复制。
---

# 武侠风 · 公众号图文直传（非截图模式）

## 是什么

传统知识卡片流程是"HTML → 截图 → 切割 → 图片文章推送"，读者看到的是截图瀑布流。本技能换一种推送方式：**将武侠风排版的 HTML 直接作为公众号图文内容推送**，读者看到的是真正的文字 + 图片混排长文，可选中文字、点击复制代码，阅读体验远胜截图模式。

> **核心优势**：文字可选中、代码可复制、排版自适应手机宽度、墨小颠配图嵌入文中，整体更像一篇精心排版的公众号文章而非长图拼接。

## 触发场景

以下任一表述出现时触发：

- "直接发公众号图文"
- "推送到公众号作为文章"
- "不用截图，直接发排版文章"
- "发成可以复制文字的图文"
- "推图文消息到草稿箱"
- "HTML 直推公众号"
- "用 HTML 模式推送" / "Mode 1 推送"
- "公众号长文"

> **与现有截图模式的区分**：
> - "上传公众号"、"发布到微信" 等无修饰关键词 → 默认仍走截图模式（`--image-files`）
> - 明确提到"图文"、"HTML 模式"、"不要截图"、"可复制文字" → 触发本技能

## 前置条件

1. 已完成「技术名词知识卡片」的**内容生成**（四回内容：是什么 / 为什么用 / 怎么用 / 有什么问题）
2. 墨小颠配图已生成（`generated-images/xiaodian_*.png`）
3. 微信配置已就绪（`config/wechat_config.yaml` 中的 AppID/AppSecret 非占位值）
4. `@skill://wechat-publisher` 中的 `push_to_wechat_draft.py` 脚本可用

## 模板变量

基于 `assets/card_template_wx_article_wuxia.html` 模板，所有变量如下：

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{ARTICLE_TITLE}}` | `<title>` 标签中的标题（浏览器标签页用） | `LLM 武林秘籍` |
| `{{KICKER}}` | 卷首封印文字 | `武林秘籍` |
| `{{TITLE}}` | 正标题（秘籍封面大标题） | `LLM：大语言模型武林通关秘籍` |
| `{{DECK}}` | 副标题 / 一句话定位 | `从文弱书生到一代宗师，只差这一本心法` |
| `{{AUTHOR_NAME}}` | 作者署名 | `daner技术栈` |
| `{{QR_CODE_IMAGE}}` | 页脚二维码路径 | `../../assets/qrcode_wechat.jpg` |
| `{{STORYTELLER_INTRO}}` | 说书人开场白 | `列位看官，今日要说的是……` |
| `{{SEAL_TEXT}}` | 印章文字（2-4字） | `武林` |
| `{{CHAPTER_WHAT_HEADER}}` | 第一回标题区域 HTML | 含回目编号 + 标题的完整 `<div>` |
| `{{CHAPTER_WHAT_BODY}}` | 第一回正文 | 是什么的定义、背景等段落 |
| `{{CHAPTER_WHY_HEADER}}` | 第二回标题区域 HTML | 同上 |
| `{{CHAPTER_WHY_INTRO}}` | 第二回导语 | 为什么用这技术的总起段落 |
| `{{CHAPTER_WHY_BODY}}` | 第二回正文 | — |
| `{{CHAPTER_HOW_HEADER}}` | 第三回标题区域 HTML | 同上 |
| `{{CHAPTER_HOW_INTRO}}` | 第三回导语 | — |
| `{{CHAPTER_PROBLEMS_HEADER}}` | 第四回标题区域 HTML | 同上 |
| `{{CHAPTER_PROBLEMS_INTRO}}` | 第四回导语 | — |
| `{{ILLO_WHAT}}` | 第一回墨小颠配图 HTML | `<div class="illo-wrap">...` |
| `{{ILLO_WHY}}` | 第二回墨小颠配图 HTML | 同上 |
| `{{ILLO_HOW}}` | 第三回墨小颠配图 HTML | 同上 |
| `{{ILLO_PROBLEMS}}` | 第四回墨小颠配图 HTML | 同上 |
| `{{ANALOGY}}` | 核心类比段落 | 用生活场景类比技术本质 |
| `{{TIMELINE_ITEMS}}` | 时间线条目 | 3-4 条 `<li class="timeline-item">` |
| `{{FEATURE_CARDS}}` | 独门绝技卡片 | 4 个 `<div class="feature-card">` |
| `{{COMPARE_LABEL_A}}` | 对比表左列标签 | `TECH A` |
| `{{COMPARE_LABEL_B}}` | 对比表右列标签 | `TECH B` |
| `{{COMPARE_ROWS}}` | 对比表行内容 | 若干 `<tr>...</tr>` |
| `{{DIAGRAM_ROWS}}` | 架构图行 | 若干 `<div class="diagram-row">` |
| `{{MANTRA}}` | 心法口诀（一句话核心命令） | `docker run -d -p 80:80 nginx` |
| `{{CODE_BLOCK}}` | 代码块内容 | 带 `<span class="comment/cmd/flag/str">` 的高亮代码 |
| `{{ASIDE_TIP}}` | 说书人插话 | 一句话实用小贴士 |
| `{{ALERT_BLOCKS}}` | 警告框列表 | 2-3 个 `<div class="alert danger/info">` |
| `{{REFERENCES}}` | 参考文献列表 | 3-5 条 `<li>来源 · URL</li>` |
| `{{TECH_JIANGHU_LINK}}` | 技术江湖链接 | 博客或公众号主页 URL |

## 输出目录结构

```
output/wuxia/{技术名词}/
├── {技术名词}_{YYYYMMDD_HHMMSS}_wx_article_wuxia.html   ← 公众号图文 HTML
└── {技术名词}_{YYYYMMDD_HHMMSS}_cover.png               ← 封面图（900×383）
```

## 生成与推送流程

### 步骤 1：生成内容

由主技能 `@skill://tech-knowledge-card` 完成四回武侠叙事内容构建：

- 秘籍封面（标题 + 封印 + 一句话定位）
- 说书人开场（古风说书人口吻引入技术）
- 第一回：这是什么？（定义 + 类比 + 时间线）
- 第二回：为什么用？（5 个独门绝技 + 武林对决对比表）
- 第三回：怎么用？（架构图 + 心法口诀 + 代码 + 说书人插话）
- 第四回：有什么坑？（2-3 个走火入魔警告 + 1 个专家忠告）

### 步骤 2：填充模板

读取 `assets/card_template_wx_article_wuxia.html` 模板（CSS 已内联，无需外部样式文件），逐一替换上述 `{{VARIABLE}}`：

- **路径规则**：模板中的 `{{QR_CODE_IMAGE}}` 填入 `../../assets/qrcode_wechat.jpg`，`{{ILLO_*}}` 中的图片路径使用 `../../../generated-images/xiaodian_X_desc.png`
- **HTML 安全**：所有用户内容中的 `<` `>` `&` 转义或确认无注入风险
- **文件写入路径**：`output/wuxia/{技术名词}/{技术名词}_{YYYYMMDD_HHMMSS}_wx_article_wuxia.html`

### 步骤 3：生成封面图

调用 `@skill://wechat-publisher` 中的封面图生成流程 → `image_gen` 生成 → 裁剪到 900×383：

```bash
python ../wechat-publisher/scripts/generate_cover_image.py crop \
  -i output/wuxia/{技术名词}/raw.png \
  -o output/wuxia/{技术名词}/{技术名词}_{时间戳}_cover.png
```

### 步骤 4：HTML 直推公众号草稿箱

**[CRITICAL] 核心命令**：调用 `@skill://wechat-publisher` 的 HTML 直推模式：

```bash
python ../wechat-publisher/scripts/push_to_wechat_draft.py \
  "output/wuxia/{技术名词}/{技术名词}_{时间戳}_wx_article_wuxia.html" \
  --upload-images \
  --title "{营销标题}" \
  --author "daner" \
  --cover-image "output/wuxia/{技术名词}/{技术名词}_{时间戳}_cover.png"
```

**与原截图模式的关键区别**：

| 维度 | 截图模式（`--image-files`） | 图文模式（HTML + `--upload-images`） |
|------|--------------------------|--------------------------------------|
| 第一个参数 | 无需 HTML 文件 | **必须提供 HTML 文件路径** |
| `--image-files` | 必填，指定切割 PNG | **不用** |
| `--upload-images` | 不用 | **必填**，自动上传文中本地图片到微信 CDN |
| 正文内容 | 纯 `<img>` 图序列 | 完整的风格化 HTML 长文 |
| 读者体验 | 看截图 | 看排版文章，文字可选/代码可复制 |
| 腾讯云图片审核 | 不触发（图片已上传素材库） | 可能触发（HTML 正文经 filter 扫描） |

**`--upload-images` 自动处理**：
1. 扫描 HTML 中所有 `<img src="…">` 标签
2. 本地路径（`../../../generated-images/xiaodian_*.png`、`../../assets/qrcode_wechat.jpg`）→ 上传到 `media/uploadimg` → 获取微信 CDN URL → 替换 `src`
3. 远程 URL（`http://` / `https://`）→ 跳过
4. 不存在的文件 → 跳过并警告

### 步骤 5：确认结果

推送完成后告知用户：

- ✅ 草稿已创建，Media ID
- 📷 文中 X 张图片已上传到微信 CDN
- 🖼 封面图状态
- 🔗 在公众号后台「草稿箱」可预览和编辑

## 标题规则

与截图模式**完全一致**：

**[WARNING] 标题必须是营销标题**：禁止直接用技术名词 + 风格后缀。必须从**焦虑感 / 好奇心 / 获得感 / 社交货币 / 紧迫感**中选题，≤32 字。

- Redis → [NO] "Redis 武林秘籍" [OK] "被Redis虐哭后，我悟了这本武功心法"
- Docker → [NO] "Docker 武侠" [OK] "面试官问Docker，我掏出这张旧报纸"

### 标题公式速查（实战胜率高的模板）

| 编号 | 公式模板 | 结构拆解 | 已验证案例 | 适合场景 |
|---|---|---|---|---|
| **F1** | 搞懂`{X}`，`{领域}`你就横着走 | 获得感 → 狂妄结果 | "搞懂AQS，Java并发包你就横着走" | 单个核心技术 |
| **F2** | 被`{X}`虐哭后，我悟了这套`{比喻}` | 焦虑共鸣 → 解法承诺 | "被Redis虐哭后，我悟了这本武功心法" | 学习曲线陡峭的技术 |
| **F3** | 面试官问`{X}`，我掏出`{独家武器}` | 社交货币 → 反杀场景 | "面试官问Docker，我掏出这张旧报纸" | 面试高频考点 |
| **F4** | 没用过`{X}`的`{岗位}`，`{严重后果}` | 紧迫感 → 身份威胁 | "没用过K8s的后端，简历直接被筛掉" | 行业趋势技术 |
| **F5** | 把`{X}`画成`{画面}`，`{对象}`一看就懂 | 好奇心 → 认知降维 | "把Raft画成连环画，实习生一看就懂" | 复杂概念可视化 |
| **F6** | 花了`{N}`小时搞懂`{X}`，现在`{N}分钟`讲给你听 | 时间投入 → 读者占便宜 | "花了80小时搞懂Transformer，现在8分钟讲给你" | 高复杂度技术 |
| **F7** | `{N}`个问题，带你彻底搞懂`{X}` | 结构清晰 → 获得感可量化 | "3个问题，带你彻底搞懂HTTPS" | 问题驱动结构 |

**生成标题时的铁律**：
1. **禁止说明书式标题**：如"Redis 武林秘籍""Docker 知识卡片"→ 这等于主动放弃点击
2. **禁止空洞情绪词**：不要写"惊天揭秘""99%的人不知道"这种脱离内容的标题党
3. **必须对位读者身份**：标题里的人设必须是目标读者（后端/前端/面试者/小白），不是作者
4. **≤ 32 字**，含标点。超出就删修饰词，留核心钩子
5. **每个标题提供 3 个候选**，按预估点击率排序，第1个是最优解

## 与现有工作流的配合

本技能**不是替代**现有截图模式，而是**新增选择**：

| 场景 | 推荐模式 |
|------|---------|
| 追求视觉还原（纹理/印章/渐变） | 截图模式 |
| 需要文字可选中、代码可复制 | **图文模式** |
| 多图配合密集排版 | 截图模式 |
| 想二次编辑文字内容 | **图文模式** |
| 规避腾讯图片审核 | 截图模式 |
| 纯技术教程、代码为主 | **图文模式** |

## 已知限制

1. **微信 WebView 渲染差异**：部分 CSS3 特性（`clamp()`、复杂 `box-shadow` 叠加）在微信内置浏览器中可能降级。模板已做兼容处理（去掉 `clamp()`、简化阴影）。
2. **HTML 长度限制**：微信 `draft/add` API 限制 content 字段 ≤ 1MB（约 2 万字符）。一篇完整四回武侠文章通常在 15,000-20,000 字符，接近但一般不会超出。
3. **图片审核**：HTML 正文经过微信后台 filter 扫描，使用腾讯云图片审核。如遇误杀，退回截图模式。
4. **字体依赖**：`KaiTi` / `STKaiti` / `楷体` 仅在 iOS/macOS 系统默认可用，Android 和 Windows 微信阅读时可能退化到系统默认衬线字体，视觉效果略有差异。

## 博客同步

与现有流程一致：将 `_wx_article_wuxia.html` 复制到 blog 站点时，图片路径需替换：

| 原文路径 | blog 路径 |
|---------|----------|
| `../../../generated-images/xxx.png` | `../images/xxx.png` |
| `../../assets/qrcode_wechat.jpg` | `../qrcode_wechat.jpg` |

## 依赖技能

| 技能 | 用途 |
|------|------|
| `@skill://tech-knowledge-card` | 内容生成（四回武侠叙事 + 墨小颠配图） |
| `@skill://wechat-publisher` | 推送脚本（`push_to_wechat_draft.py` + `generate_cover_image.py`） |

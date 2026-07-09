---
name: tech-knowledge-card
agent_created: true
description: 当用户要求以脱口秀级骨灰级专家视角，用类比方式讲解某个技术名词，并输出知识卡片 HTML（移动端截图用 + 网页版浏览器阅读）时触发。覆盖是什么、为什么用、怎么用、有什么问题四个维度，末尾署名 {{AUTHOR_NAME}}（默认"daner技术栈"）、列出参考文献。根据用户意图自动分发到多个子风格。网页版 HTML 为响应式布局，直接浏览器阅读。推送公众号由下游技能 @skill://html-to-image（截图切割）+ @skill://wechat-publisher（推送到草稿箱）组成完整流水线。
---

# Tech Knowledge Card — 技术名词知识卡片生成（总入口）

## 变量约定

以下变量由入口统一指定，所有子技能和模板均使用此变量，生成时替换为实际值：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `{{AUTHOR_NAME}}` | `daner技术栈` | 作者署名，出现在所有模板的署名/印章/byline 位置 |
| `{{QR_CODE_IMAGE}}` | `../../assets/qrcode_wechat.jpg` | 公众号二维码图片路径（相对 output/{style}/{技术名词}/ 的路径，上两级回到根目录），出现在所有模板页脚 |

> 用户在请求中指定了作者名（如"署名 XXX"），则覆盖默认值。

## 触发场景

以下任一表述出现时触发：
- "把 XXX 技术讲成知识卡片"
- "用类比解释 XXX 技术"
- "扮演脱口秀级专家讲 XXX 技术"
- "用武侠秘籍/漫画风讲解 XXX"
- "输出 HTML/PNG 知识卡片"
- "方便手机阅读的图片"
- 类似意图：给定技术名词，要求生成类比化、脱口秀级化、结构化的知识卡片

## 如何使用

### 基本用法

直接说出以下任一指令即可：

```
把 Docker 讲成知识卡片
用类比解释 Redis 技术
生成 WebSocket 知识卡片，要报纸风
输出 GraphQL 的 HTML 和 PNG 卡片
```

### 风格分发

根据用户输入中的关键词，自动加载对应子 Skill：

| 关键词 | 分发到 | 子 Skill 文件 |
|---|---|---|
| 无修饰词（默认） | Editorial 编辑杂志风 | `SKILL_editorial.md` |
| "武侠""秘籍""漫画""江湖""武功""夸张""刺激" | → 转发到 `@skill://wuxia-card` | — |
| "攻克""征服""拿下""啃掉""硬骨头""从恐惧到精通""从零开始学""学习路线""怎么学会""练成""入门到精通" | → 转发到 `@skill://wuxia-conquest-card` | — |
| "流程""步骤""从0到1""一步步""过程""路线""攻略""图解流程""武侠流程图""怎么完成""上手路线" | → 转发到 `@skill://wuxia-pipeline-card` | — |
| "直接发公众号图文""推送到公众号作为文章""不用截图，直接发排版文章""发成可以复制文字的图文""推图文消息到草稿箱""HTML 直推公众号""用 HTML 模式推送""公众号长文" | → 转发到 `@skill://wechat-article` | — |
| "上传到公众号""发布到微信""推送到草稿""生成封面""公众号封面""封面图""配个封面" | → 转发到 `@skill://wechat-publisher` | — |

```
把 Kubernetes 讲成报纸风格的知识卡片    → Newspaper
用旧报纸排版解释 Docker 技术            → Newspaper
把 Redis 讲成武侠秘籍风格                → Wuxia
用夸张漫画风讲解 WebSocket              → Wuxia
给我一个 Docker 的征服学习路线            → Wuxia 攻克式·征服者之路
把 Docker 讲成知识卡片                   → Editorial（默认）
把搭建 CI/CD 的完整步骤画成武侠流程图       → Wuxia 流程卡·从0到1
一步一步教我怎么部署 K8s 集群               → Wuxia 流程卡·从0到1
把 Docker 直接推送成公众号排版长文           → Wuxia 图文直推
```

> **分发流程**：检测到关键词后，用 `read_file` 读取对应子 Skill 文件获取该风格的专属模板和内容规则，然后执行生成流程。

### 交付物

每次生成输出两类 HTML + 长图 + 切割图，按风格和主题分目录存储。详见 **[FILES.md §二·输出目录结构](./FILES.md#二输出目录结构)** 和 **[FILES.md §三·文件命名规则](./FILES.md#三文件命名规则)**。

核心要点：
- **固定输出根目录**：`D:\workspace\tech-knowledge-card\`（不受 IDE 工作区时间戳影响，所有路径相对于此根目录）
- **移动端 HTML**（420px 固定宽度）→ 下游技能 `@skill://html-to-image` 负责截图、切割 → `@skill://wechat-publisher` 推送到公众号草稿箱
- **网页版 HTML**（响应式 max 820px）→ 浏览器直接阅读，不走截图管线
- **一个主题一个文件夹**：`output/{style}/{技术名词}/`，产物全部在该主题目录下
- 文件命名：`{技术名词}_{YYYYMMDD_HHMMSS}_{style}.{ext}`，每次生成带时间戳不覆盖

> 模板和脚本的完整清单见 **[FILES.md](./FILES.md)**。

### 前置依赖

本技能仅负责**内容生成**（HTML + 配图），截图/切割由 `@skill://html-to-image` 负责，推送由 `@skill://wechat-publisher` 负责。

```bash
# 封面图生成依赖
pip install Pillow
```

> 截图管线依赖（Playwright）请在 `@skill://html-to-image` 侧安装。推送依赖（PyYAML / Pygments）请在 `@skill://wechat-publisher` 侧安装。

## 生成流程

按以下顺序执行：

1. **选择技术名词**：如果用户没指定，主动挑选一个常见、有趣、适合类比的技术名词（如 Docker、Redis、WebSocket、Kubernetes、GraphQL）。
2. **资料校验**：通过 WebSearch / WebFetch 至少 2 个权威来源，确认核心概念、技术细节、对比关系，避免胡说八道。
3. **内容构建**：以「脱口秀级骨灰级专家」口吻，围绕以下四方面撰写：
   - **是什么？**：用一句话定义 + 一个生动类比 + 历史/背景补充。
   - **为什么用？**：列出 3-5 个核心优势，必要时用对比表格（如 vs VM）。
   - **怎么用？**：给出最小可运行示例（如 Dockerfile、命令行、代码片段），配合架构图说明。
   - **有什么问题？**：列出 2-4 个常见坑点，用警告样式突出安全/持久化/网络/性能问题。
4. **选择模板风格**：默认 Editorial，根据关键词分发到子 Skill（见上方风格分发表）。
5. **生成墨小颠配图**：为卡片生成手绘线稿风格的墨小颠配图，嵌入 HTML 丰富视觉。分三步：
   
   **5a. 观文 → 配图策略**：读完步骤 3 构建的内容后，提炼核心认知锚点，每张卡片 2-3 张配图：
   - **图1 · 概念类比图**：把技术核心类比画出来（借物喻理/一语点穴）→ 放在「是什么」章节
   - **图2 · 招式/流程图**：画技术的关键动作或架构（行云流水/管中窥豹）→ 放在「怎么用」章节
   - **图3 · 陷阱图**（可选）：画最典型的坑（借物喻理/浮生三帧）→ 放在「有什么问题」章节
   
   **5b. 落笔 → 生图**：用 `image_gen` 逐张生成，参数：`size: "1024x1024"`，`style: "vivid"`，`output_dir: "generated-images/"`，文件名 `xiaodian_{序号}_{desc}.png`。
   
   必检要素（每张生成前确认）：
   - 乱毛 bun + 朱砂红葫芦（角色锚点到位）
   - 墨小颠在干技术相关的活（不是站桩看客）
   - prompt 首行写 `Chinese text ONLY. All text characters must be Chinese.`
   - 批注 2-5 个词，汉字清晰可读、笔画完整
   
   **5c. 验稿**：生成后逐字默念批注汉字，确认无缺笔画/假名/英文/粘连。不合格→重生成（对症下药：补 prompt 约束，砍批注数，调间距）。
   
   **5d. HTML 嵌入**：在 HTML 模板中对应章节用 `<img src="../../generated-images/xiaodian_X_desc.png" class="illo-img" />` 嵌入配图。样式：max-width 匹配卡片宽度，居中，四周留白。
   
6. **生成移动端 HTML**：根据选中的子 Skill 模板，生成对应风格的完整 HTML 卡片。

   **模板与样式对应关系（符合前端工程化规范，CSS 已从模板中分离到 `assets/css/` 目录）：**

   | 风格 | HTML 模板 | CSS 样式文件 |
   |------|----------|-------------|
   | Editorial | `assets/card_template.html` | `assets/css/editorial.css` |
   | Wuxia | `assets/card_template_wuxia.html` | `assets/css/wuxia.css` |
   | Wuxia 攻克式 | `assets/card_template_wuxia_conquest.html` | `assets/css/wuxia_conquest.css` |
   | Wuxia 流程卡 | `assets/card_template_wuxia_pipeline.html` | `assets/css/wuxia_pipeline.css` |
   | Newspaper | `assets/card_template_newspaper.html` | `assets/css/newspaper.css` |
   

   **模板结构规范（前端工程化分离）：**
   - HTML 模板仅包含结构（`<body>` 中的 HTML 元素）
   - CSS 样式独立存放在 `assets/css/{style}.css` 文件
   - 模板通过 `<link rel="stylesheet" href="css/{style}.css">` 引用样式
   - 无 JavaScript 依赖（纯静态展示型页面）
   - 静态资源（图片、二维码）存放在 `assets/` 根目录

   **移动端 HTML 生成步骤（供 `@skill://html-to-image` 截图使用）：**
   - 读取对应模板 HTML 和 `assets/css/{style}.css` 样式文件
   - 将 `<link rel="stylesheet" href="css/{style}.css">` 替换为 `<style>/* {style}.css 内容 */</style>`（内联 CSS）
   - 替换内容占位变量，写入输出文件
   - **文件写入路径**：`output/{style}/{技术名词}/{技术名词}_{时间戳}_{style}.html`
   - **注意**：此 HTML 宽度固定 420px，专为截图生成 PNG 设计，CSS 已内联以保证截图自包含渲染。

7. **生成网页版 HTML**：基于 `assets/card_template_web.html` 模板，引用 `assets/css/web.css` 样式文件，用同一份内容填充生成**响应式网页版** HTML。

   **网页版样式引用**（保留外部 CSS 链接，符合前端工程化规范）：模板中已包含 `<link rel="stylesheet" href="css/web.css">`，生成时**不内联 CSS**，保持样式与结构分离。

   核心特性：
   - 用 `<html data-theme="wuxia|editorial|newspaper">` 设置风格主题
   - 用 `<body>` 包裹内容，响应式布局（`max-width: 820px`）
   - 顶部带导航栏 + 锚点目录（TOC），`<section id="what|why|how|problems">` 锚点链接
   - 优势列表用 `.feature-grid`（CSS Grid 自适应 `repeat(auto-fit, minmax(280px, 1fr))`）
   - 对比表格用 `<table>` + `.compare-table`，支持横向滚动
   - `@media (max-width: 900px)` 和 `480px` 两级响应式断点
   - Print 样式优化（隐藏导航栏）
   - 底部签名 + 二维码分列布局
   - **文件写入路径**：`output/{style}/{技术名词}/{技术名词}_{时间戳}_{style}_web.html`
   - **此 HTML 不进入截图管线**，直接在浏览器打开即可阅读

8. **（已移至 html-to-image）截图管线**：移动端 HTML → PNG 长图 → 切割，由下游技能 `@skill://html-to-image` 负责。详见 [html-to-image SKILL.md](html-to-image/SKILL.md)。

   > **标题规则**：推公众号时仍需生成营销标题（参见下方「标题公式速查」），传递给 `@skill://wechat-publisher` 的 `--title` 参数。

9. **输出交付**：提供所有生成文件（移动端 HTML + 网页版 HTML + 墨小颠配图），并简要说明参考了哪些权威来源。

10. **记录到文章目录**：生成完成后，自动追加文章记录到 `output/article_catalog.txt`（格式见 [FILES.md §十·共享资源](./FILES.md#十共享资源)）。

    ```python
    catalog_line = f"{timestamp}|{tech_name}|{style}|{article_title}|{html_path}|{png_path}|{cover_path}\n"
    with open('output/article_catalog.txt', 'a', encoding='utf-8') as f:
        f.write(catalog_line)
    ```

11. **推送公众号**（可选）：如果用户要求推送，分两步：
    1. 调用 `@skill://html-to-image` 截图+切割
    2. 调用 `@skill://wechat-publisher` 推送到草稿箱

    - **图片直传模式**（所有风格默认推荐）：
      ```bash
      # Step 1: @skill://html-to-image 截图+切割
      python scripts/html_to_png.py output/{style}/{技术名词}/{文件}.html output/{style}/{技术名词}/{文件}.png --width 420 --scale 2
      python scripts/split_image.py output/{style}/{技术名词}/{文件}.png
      # Step 2: @skill://wechat-publisher 推送
      python scripts/push_to_wechat_draft.py \
        --image-files "output/{style}/{技术名词}/splits/{技术名词}_*_0*.png" \
        --title "{营销标题}" \
        --author "daner" \
        --cover-image output/{style}/{技术名词}/{技术名词}_cover.png
      ```

    - **HTML 图文直推模式**（武侠风，文字可复制）：
      先生成 `card_template_wx_article_wuxia.html`，再转发给 `@skill://wechat-article` 走 HTML 图文直推流程。

    > 完整流程、参数说明、封面图生成见 `@skill://wechat-publisher` 的 SKILL.md。

12. **同步到 Blog 静态站点**：生成完成后，将网页版 HTML 和配图同步到 `D:\IdeaProjects\daner20190523.github.io\blog`（GitHub Pages 部署的静态博客）。详见 [FILES.md §五·Blog 静态站点](./FILES.md#五blog-静态站点dideaprojectsdaner20190523githubioblog)。

   **12a. 复制网页版 HTML 到 blog**：将步骤 7 生成的网页版 HTML 复制到 `blog/wuxia/`，并**重命名去掉 `_web` 后缀**。

   > **注入共享顶部导航**：找到 HTML 中的 `<!-- BLOG_NAV -->` 注释，读取 `blog/_includes/nav_article.html` 内容替换。

   **12b. 替换图片路径 + 注入共享页脚**：
   | 原路径（扁平化后） | blog 路径 |
   |---|---|
   | `../../generated-images/xxx.png` | `../images/xxx.png` |
   | `../../assets/qrcode_wechat.jpg` | `../qrcode_wechat.jpg` |

   **12c. 复制配图到 blog/images/**。

   **12d. 更新 images.json**：
   ```json
   { "file": "xiaodian_X_desc.png", "label": "中文字描述" }
   ```
  
   **12e. 更新 articles.html**：在 `blog/wuxia/articles.html` 开头新增文章卡片（缩进对齐已有格式）。

   **12f. 更新 blog/index.html**：首页新增 `.article-card`（插入「更多文章」按钮之前）。

> **关键规则**：每次生成都必须执行步骤 12a-12f，确保 blog 静态站点五点全部同步。

13. **重新上传已有产物**（不重新生成）：如果用户已有生成好的产物，调用 `@skill://wechat-publisher` 用 `--image-files` 模式直接上传。标题仍需从下方「标题公式速查」生成营销标题。

## 公共资源（所有风格共用）

模板、样式、脚本、子技能、配置文件的完整清单见 **[FILES.md](./FILES.md)**，包括但不限于：

- **HTML 模板**（仅结构，样式已分离）：`assets/card_template.html`（Editorial）、`assets/card_template_wuxia.html`（Wuxia）、`assets/card_template_wuxia_conquest.html`（攻克式）、`assets/card_template_wuxia_pipeline.html`（流程卡）、`assets/card_template_newspaper.html`（Newspaper）、`assets/card_template_web.html`（网页版通用）
- **CSS 样式**（独立文件）：`assets/css/editorial.css`、`assets/css/wuxia.css`、`assets/css/wuxia_conquest.css`、`assets/css/wuxia_pipeline.css`、`assets/css/newspaper.css`、`assets/css/web.css`
- **内容生成脚本**：`scripts/inject_shared_footer.py`（页脚注入）、`scripts/html_slice.py`（小红书卡片切片）
- **独立技能**：`@skill://wuxia-card`（武侠漫画风·标准版）、`@skill://wuxia-pipeline-card`（武侠流程卡）、`@skill://wuxia-conquest-card`（攻克式手札）、`@skill://wechat-article`（公众号图文直传）、`@skill://html-to-image`（截图管线·HTML→PNG→切割）、`@skill://wechat-publisher`（推送公众号草稿箱）、以上均已从本技能拆分独立
- **墨小颠配图**：调用 `@skill://wuxia-avatar` skill 生成手绘线稿

> **截图管线**（截图/切割）由独立技能 `@skill://html-to-image` 负责，包括 `html_to_png.py`、`split_image.py`、`extract_css.py` 等脚本。发布管线由 `@skill://wechat-publisher` 负责。本技能不再携带管线脚本。

## 内容风格指南（所有风格通用）

- 用第一人称「我」口吻，像脱口秀演员在讲段子。
- 每个类比要具体、可触摸，避免抽象术语堆叠。
- 技术术语必须准确，错误处应及时纠正。
- 代码片段必须可执行真实命令，不要写伪代码。
- 警告框必须标注具体风险，不能泛泛而谈。

## 示例输出结构（所有风格通用骨架）

1. 标题 + 技术标签
2. 专家徽章
3. 是什么？（定义 + 类比 + 历史时间线）
4. 为什么用？（优势列表 + 对比表格）
5. 怎么用？（架构图 + 代码示例 + 命令速查）
6. 有什么问题？（警告框 + 专家忠告）
7. 参考文献
8. 署名：{{AUTHOR_NAME}}（默认"daner技术栈"）



## 运营策略（涨粉导向）

### 核心目标
以**涨粉**为初期运营目标，通过内容设计调动用户情绪，提升分享率和关注转化率。

### 情绪调动策略

#### 1. 标题情绪设计
标题是涨粉的第一道门，必须触发用户情绪。不要机械套用情绪类型，而是从**内容本身**里提炼最有杀伤力的那个认知钩子。

| 情绪类型 | 触发词 | 示例标题 | 预期效果 |
|---|---|---|---|
| **焦虑感** | "坑""踩坑""血泪""崩溃""千万不要" | "Docker 这些坑，我替你踩过了" | 引发共鸣，降低防御 |
| **好奇心** | "揭秘""真相""为什么""原来""背后的" | "Redis 为什么这么快？真相在这里" | 激发点击欲望 |
| **获得感** | "搞懂""一文搞懂""彻底弄懂""从入门到精通""手把手" | "一文彻底搞懂 Kubernetes" | 承诺价值，降低门槛 |
| **社交货币** | "面试官问""大厂""阿里""腾讯""字节" | "面试官：Docker 和网络有什么关系？" | 提升分享意愿 |
| **紧迫感** | "必须""一定要""再不学就晚了""2026 年" | "2026 年还不会 Docker？涨薪无望" | 促进行动 |

#### 1½. 标题公式速查（实战胜率高的模板）

不要凭空起标题，从下面已经验证过的公式里选，填入技术名词和领域关键词即可。

| 编号 | 公式模板 | 结构拆解 | 已验证案例 | 适合场景 |
|---|---|---|---|---|
| **F1** | 搞懂`{X}`，`{领域}`你就横着走 | 获得感 → 狂妄结果 | "搞懂AQS，Java并发包你就横着走" | 单个核心技术，它是整个领域的基石 |
| **F2** | 被`{X}`虐哭后，我悟了这套`{比喻}` | 焦虑共鸣 → 解法承诺 | "被Redis虐哭后，我悟了这本武功心法" | 有一定学习曲线的技术 |
| **F3** | 面试官问`{X}`，我掏出`{独家武器}` | 社交货币 → 反杀场景 | "面试官问Docker，我掏出这张旧报纸" | 面试高频考点 |
| **F4** | 没用过`{X}`的`{岗位}`，`{严重后果}` | 紧迫感 → 身份威胁 | "没用过K8s的后端，简历直接被筛掉" | 行业趋势技术 |
| **F5** | 把`{X}`画成`{画面}`，`{对象}`一看就懂 | 好奇心 → 认知降维 | "把Raft画成连环画，实习生一看就懂" | 复杂概念，用可视化表达 |
| **F6** | 花了`{N}`小时搞懂`{X}`，现在`{N}分钟`讲给你听 | 时间投入 → 读者占便宜 | "花了80小时搞懂Transformer，现在8分钟讲给你" | 高度复杂、需要长时间消化的技术 |
| **F7** | `{N}`个问题，带你彻底搞懂`{X}` | 结构清晰 → 获得感可量化 | "3个问题，带你彻底搞懂HTTPS" | 问题驱动的讲解结构 |

**生成标题时的铁律**：
1. **禁止说明书式标题**：如"Redis 武林秘籍""Docker 知识卡片"→ 这等于主动放弃点击
2. **禁止空洞情绪词**：不要写"惊天揭秘""99%的人不知道"这种脱离内容的标题党
3. **必须对位读者身份**：标题里的人设必须是目标读者（后端/前端/面试者/小白），不是作者
4. **≤ 32 字**，含标点。超出就删修饰词，留核心钩子
5. **每个标题提供 3 个候选**，按预估点击率排序，第1个是最优解

#### 2. 开场白情绪钩子
文章开头 50 字必须抓住注意力：

**模板 A（共鸣型）**：
> "去年我面试阿里，面试官问我 Docker 和网络的关系，我愣了 3 秒... 这篇文章帮你不再尴尬。"

**模板 B（反直觉型）**：
> "你以为 Docker 是虚拟机？错了。它和 VM 的区别，就像租房和买房。"

**模板 C（故事型）**：
> "上个月线上崩溃，排查 3 小时发现是 Docker 网络配置问题。血泪教训，分享给你。"

#### 3. 内容节奏情绪曲线
整篇文章的情绪节奏设计：

```
开头：共鸣/焦虑（抓住注意力）
  ↓
是什么：好奇/惊喜（类比生动，打破认知）
  ↓
为什么用：获得感（列出优势，强化价值）
  ↓
怎么用：成就感（最小示例，立即上手）
  ↓
有什么问题：警惕/信任（指出坑点，建立专业度）
  ↓
结尾：行动召唤（关注/分享/留言）
```

#### 4. 互动设计（提升 engagement）
- **埋彩蛋**：文中隐藏小问题，文末公布答案，引导留言
- **留悬念**："这个问题我们下期讲"，引导关注
- **求互动**："你踩过哪些坑？评论区告诉我"
- **晒成就**："学会这个，面试不怕被问"

#### 5. 分享诱导设计
让用户愿意分享到朋友圈/技术群：

- **金句提炼**：文中加粗 3-5 句可独立传播的金句
- **配图友好**：卡片设计适合截图分享（含署名和二维码）
- **身份认同**："作为一名后端工程师，这篇文章你必须看"
- **利他诱导**："转发给还在踩坑的同事"

### 涨粉转化路径

```
内容吸引（标题+开场） → 情绪共鸣（类比+故事） → 价值交付（干货+示例）
       ↓                ↓                     ↓
   点击阅读          读完率提升            建立信任
       ↓                ↓                     ↓
                                         关注转化
                                             ↓
                                      后续内容留存
```

### 数据指标（优化方向）
- **点击率**：标题情绪设计效果
- **读完率**：内容节奏和情绪曲线效果
- **分享率**：分享诱导设计效果
- **关注转化率**：结尾行动召唤效果

---

## 常见错误避免

- **概念别混淆**：相近技术名词必须厘清边界（如运行时 vs 编排平台、框架 vs 库、协议 vs 实现），不要张冠李戴。
- **别绝对化安全/性能**：避免"比 XXX 更安全""比 XXX 快 10 倍"等无数据支撑的断言，差异要说清前提条件和场景。
- **别忽略反作用条件**：技术优势往往带有代价（如高可用带来复杂度、无状态带来外部存储依赖），必须点出适用边界。
- **类比要贴切**：类比必须抓住技术核心特征，一个技术只找一个最贴切的类比，不要生搬硬套。
- **写代码遵循阿里代码规范，禁止代码使用表情**
- **运营禁忌**：
  - 标题不要过度标题党（内容必须匹配标题承诺）
  - 情绪调动要真实（不要用虚假故事引发焦虑）
  - 涨粉是结果不是目的（内容价值是第一位的）

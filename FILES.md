# FILES — Tech Knowledge Card 全局路径规划（单一真相源）

> 本文档是所有子技能的**单一真相源**。SKILL.md 和各子 Skill 引用本文档，避免路径信息重复散落。若需新增/修改产物路径，只需改本文档。

---

## 〇、根目录约定

```
D:/workspace/tech-knowledge-card/
```

> 所有 `assets/`、`generated-images/`、`output/`、`scripts/` 均相对于此根目录。
> 子技能（wuxia-card/、wuxia-pipeline-card/、html-to-image/、wechat-publisher/、wechat-article/、blog-sync/ 等）与 SKILL.md 同级，位于根目录下。

---

## 一、变量约定

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `{{AUTHOR_NAME}}` | `daner技术栈` | 作者署名，出现在所有模板的署名/印章/byline 位置 |
| `{{QR_CODE_IMAGE}}` | `../../assets/qrcode_wechat.jpg` | 公众号二维码图片路径（**相对 `output/{style}/{技术名词}/` 的路径**，向上两级回到根目录） |

> 用户在请求中指定了作者名（如"署名 XXX"），则覆盖默认值。

---

## 二、输出目录结构

```
output/
├── newspaper/                      ← 旧报纸风产物（默认风格）
│   ├── {技术名词}/...
├── wuxia/                          ← 武侠风产物
│   ├── {技术名词}/{时间戳}_wuxia.html
│   ├── {技术名词}/{时间戳}_wuxia_web.html
│   ├── {技术名词}/{时间戳}_wuxia.png
│   ├── {技术名词}/{时间戳}_wuxia_pipeline.html   ← 流程卡 HTML
│   ├── {技术名词}/{时间戳}_wuxia_pipeline_web.html
│   ├── {技术名词}/{时间戳}_wuxia_conquest.html   ← 攻克式 HTML
│   └── {技术名词}/...
└── generated-images/               ← 墨小颠配图（所有风格共用，在根目录下）
    ├── xiaodian_1_概念类比.png
    ├── xiaodian_2_招式流程.png
    └── xiaodian_3_陷阱警告.png
```

> **关键变化**：扁平化后，`generated-images/` 从嵌套目录提升到根层，与 `output/`、`assets/` 同级。
> HTML 内图片引用从 `../../../generated-images/` 简化为 `../../generated-images/`（output/{style}/{name}/ → 上两级到根）。

---

## 三、文件命名规则

```index
{技术名词}_{YYYYMMDD_HHMMSS}_{style}.{ext}
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `{技术名词}` | 中文/英文均可，保持原始写法 | `Docker`、`Raft`、`ZooKeeper脑裂` |
| `{时间戳}` | `YYYYMMDD_HHMMSS` | `20260703_095500` |
| `{style}` | 风格标识 | `wuxia` / `wuxia_conquest` / `wuxia_pipeline` / `newspaper` |
| `{ext}` | 扩展名 | `.html` / `_web.html` / `.png` / `_01.png` / `_cover.png` |

> 每次生成使用当前时间戳，同名技术多次生成不会覆盖。

---

## 四、HTML 产物（两类）

| 产物 | 用途 | 模板源 | CSS 源 | 宽度 | 正文字体 |
|------|------|--------|--------|------|----------|
| **移动端 HTML** | 截图生成 PNG 长图 → 切割 → 公众号图片直传 | `card_template_{style}.html` | `css/{style}.css`（生成时内联） | 固定 420px | 15px（Wuxia/Newspaper） |
| **网页版 HTML** | 桌面/手机浏览器直接阅读 | `card_template_web.html` | `css/web.css`（外部引用） | 响应式（max 820px） | 17px 基体，480px↓ 16px |

> **前端工程化规范**：模板仅包含 HTML 结构，CSS 样式独立存放在 `assets/css/` 目录。移动端生成时将 CSS 内联以保证截图自包含渲染；网页版保留外部 `<link>` 引用。

> **网页版 HTML**：`data-theme` 属性切换风格，CSS Grid 自适应网格，`clamp()` 流式字体，`@media` 断点，Print 友好。**不进截图管线。**

---

## 五、Blog 静态站点（`D:\IdeaProjects\daner20190523.github.io\blog`）

Blog 是一个独立于截图管线的**静态博客站点**（GitHub Pages 部署），所有 HTML 直接在浏览器中阅读。

| 文件 | 用途 |
|------|------|
| `index.html` | 博客首页 — 武侠主题、顶部导航、文章卡片列表、页脚二维码 |
| `wuxia/articles.html` | 全部文章列表页 — 按时间倒序排列所有已生成的技术卡片 |
| `wuxia/gallery.html` | 武林图录 — 图片画廊页，读取 `images/images.json` 渲染分类画廊 |
| `wuxia/{技术名词}_{时间戳}_{style}.html` | 单篇文章 — 从网页版 HTML 同步而来 |
| `images/` | 博客图片资源 — AI 生成的配图 + 墨小颠手绘 |
| `images/images.json` | 图片索引 — 按分类组织图片列表 |
| `qrcode_wechat.jpg` | 公众号二维码 — 页脚关注入口 |
| `_includes/footer_article.html` | **共享页脚模板** — 所有文章页脚的统一 HTML 片段 |
| `_includes/nav_article.html` | **共享导航模板** — 所有文章顶部导航的统一 HTML 片段 |

> **与截图管线的关系**：blog 中的单篇文章 HTML 由网页版 HTML（`_web.html`）复制同步。图片从根目录 `generated-images/` 复制到 `blog/images/`。blog 不参与截图管线。

---

## 六、模板文件

**HTML 模板**（仅结构，样式已独立到 CSS 文件）：

| 模板文件 | 风格 | 说明 |
|----------|------|------|
| `assets/card_template_wuxia.html` | Wuxia | 武侠漫画风（宣纸卷轴、朱砂红/墨色/金色） |
| `assets/card_template_wuxia_conquest.html` | Wuxia 攻克式 | 攻坚手札·大事记（编年体、竖线时间轴、菱形节点） |
| `assets/card_template_wuxia_pipeline.html` | Wuxia 流程卡 | 连环画流程（五章结构、步骤面板、箭头连接） |
| `assets/card_template_newspaper.html` | Newspaper | 旧报纸风（红色宋体报头、错落双栏、花边分隔） |
| `assets/card_template_web.html` | 网页版通用 | 响应式阅读版（data-theme 切换三种风格） |

**CSS 样式文件**（独立分离，符合前端工程化规范）：

| 样式文件 | 对应模板 | 说明 |
|----------|----------|------|
| `assets/css/wuxia.css` | card_template_wuxia.html | Wuxia 武侠漫画风全量样式 |
| `assets/css/wuxia_conquest.css` | card_template_wuxia_conquest.html | Wuxia 攻克式全量样式 |
| `assets/css/wuxia_pipeline.css` | card_template_wuxia_pipeline.html | Wuxia 流程卡全量样式 |
| `assets/css/newspaper.css` | card_template_newspaper.html | Newspaper 旧报纸风全量样式 |
| `assets/css/web.css` | card_template_web.html | Web 响应式通用样式（三主题） |

---

## 七、脚本文件

| 脚本 | 用途 |
|------|------|
| `scripts/html_slice.py` | HTML → 多张 PNG 切片（Playwright 截全页 + Pillow 竖切），小红书卡片用 |
| `scripts/extract_css.py` | 从 `<style>` 标签提取 CSS 内容 |
| `scripts/md_to_wechat_html.py` | Markdown → 微信兼容 HTML（仅纯文字文章使用） |

---

## 八、配置文件

| 配置文件 | 用途 |
|----------|------|
| `config/wechat_config.yaml` | 真实微信公众号密钥（[WARNING] gitignore） |
| `config/wechat_config.template.yaml` | 配置模板，供用户复制使用 |
| `config/.token_cache.json` | access_token 缓存（自动生成） |

---

## 九、子技能文件

| 文件/技能 | 风格/用途 |
|-----------|-----------|
| `SKILL.md` | **总入口** — 生成流程、风格分发、运营策略 |
| `SKILL_MAIN.md` | 总入口备份（功能同 SKILL.md） |
| `@skill://wuxia-card` | 武侠漫画风·标准版 |
| `@skill://wuxia-conquest-card` | 武侠漫画风·攻克式 |
| `@skill://wuxia-pipeline-card` | 武侠漫画风·流程卡（从0到1连环画） |
| `@skill://wechat-article` | 公众号 HTML 图文直传 |
| `@skill://wechat-publisher` | 推送公众号草稿箱（图片直传模式） |
| `@skill://html-to-image` | 截图管线（HTML→PNG→切割） |
| `@skill://blog-sync` | Blog 静态站点同步 |
| `@skill://xiaohongshu-reading-card` | 小红书读书卡片 |
| `@skill://xiaohongshu-aiart-card` | 小红书 AI 艺术卡片 |

> **同工作区独立技能**（非 tech-knowledge-card 子技能，产物目录与输入要求由本文件统一规定）：
> - `前端专家级工程师/` — 生产级前端项目代码生成，**产物目录与输入配置格式见 §十三**
> - `html排版大师/` — 排版设计美学顾问（含编辑杂志风、武侠风等设计风格库）

---

## 十、共享资源

| 资源 | 路径 | 说明 |
|------|------|------|
| 墨小颠配图 | `generated-images/xiaodian_{序号}_{描述}.png` | 所有风格共用，`<img>` 标签嵌入 HTML |
| 公众号二维码 | `assets/qrcode_wechat.jpg` | 出现在所有模板页脚 |
| 文章目录 | `output/article_catalog.txt` | 格式：`时间戳|技术名词|风格|标题|HTML路径|PNG路径|封面路径|微信链接|` |

---

## 十一、嵌入 HTML 的配图引用规则

```html
<!-- 移动端 HTML（位于 output/{style}/{技术名词}/）→ 上两级到根 -->
<img src="../../generated-images/xiaodian_1_概念类比.png" class="illo-img" />
<img src="../../generated-images/xiaodian_2_招式流程.png" class="illo-img" />
<img src="../../generated-images/xiaodian_3_陷阱警告.png" class="illo-img" />

<!-- 二维码引用 -->
<img src="../../assets/qrcode_wechat.jpg" class="qr-code" />
```

> **路径对照表**（扁平化前后）：

| HTML 位置 | 扁平化前 | 扁平化后 |
|-----------|----------|----------|
| `output/{style}/{name}/file.html` → `generated-images/` | `../../../generated-images/` | `../../generated-images/` |
| `output/{style}/{name}/file.html` → `assets/` | `../../../assets/` | `../../assets/` |
| SKILL.md → 子技能 | `../html-to-image/SKILL.md` | `html-to-image/SKILL.md` |

---

## 十二、Blog 同步路径映射

生成 Blog 文章时，需将 HTML 中的绝对/相对路径替换为 Blog 内的路径：

| 原路径（HTML 内） | Blog 路径 |
|-------------------|-----------|
| `../../generated-images/xxx.png` | `../images/xxx.png` |
| `../../assets/qrcode_wechat.jpg` | `../qrcode_wechat.jpg` |

---

## 十三、前端专家级工程师（独立技能）

> 本技能独立于 tech-knowledge-card，负责生成**生产级前端项目代码**（非知识卡片）。其**产物目录**与**输入配置文件格式**由本文件统一规定，避免路径与输入约定散落各处。SKILL.md 引用本文件，不硬编码目录结构。

### 13.1 输出根目录

```
D:/workspace/html/
```

> 所有生成的前端项目文件存放于此根目录。修改此根目录只需改本文件，SKILL.md 自动同步。

### 13.2 输出目录结构

```
D:/workspace/html/
├── index.html              # 主入口文件
├── config.json             # 配置文件（网站内容，可编辑）
├── config.js               # 配置加载器（运行时使用）
├── css/
│   ├── main.css            # 主样式文件
│   ├── variables.css       # CSS变量定义（颜色/字体/间距/圆角/阴影/过渡）
│   ├── base.css            # 基础重置样式
│   ├── components.css      # 组件样式（容器/按钮/卡片/导航/Footer）
│   └── utils.css           # 工具类（文本/间距/显示/flex/响应式/动画）
├── js/
│   ├── main.js             # 主入口
│   ├── config.js           # 配置加载器
│   ├── components/         # 组件 js
│   │   ├── header.js       # 头部组件
│   │   └── footer.js       # 底部组件
│   └── utils/              # 工具函数
│       ├── dom.js          # DOM 操作工具
│       └── helper.js       # 辅助函数（节流/防抖/格式化等）
├── img/                    # 图片资源
├── fonts/                  # 字体文件
└── assets/                 # 其他静态资源
```

### 13.3 输入要求（配置文件格式）

支持三种配置文件格式作为内容输入，结构一致：

| 格式 | 输入文件 | 说明 |
|------|----------|------|
| JSON | `config.json` | 标准 JSON 配置（详见 SKILL.md 配置系统） |
| YAML | `config.yaml` | 同结构 YAML 写法 |
| Markdown | `config.md` | Frontmatter 作配置，正文作页面内容 |

**配置字段（通用结构）**：

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `site.name` | string | 网站名称 |
| `site.title` | string | 页面标题 |
| `site.description` | string | 页面描述 |
| `site.logo` | string | Logo 图片路径 |
| `site.favicon` | string | Favicon 路径 |
| `nav` | array | 导航菜单项 `[{text, url, active}]` |
| `hero.badge` | string | Hero 角标文字 |
| `hero.title` | string | Hero 主标题 |
| `hero.subtitle` | string | Hero 副标题 |
| `hero.image` | string | Hero 图片路径 |
| `hero.primaryBtn` | object | 主按钮 `{text, url}` |
| `hero.secondaryBtn` | object | 次按钮 `{text, url}` |
| `features` | array | 功能特点 `[{icon, title, description}]` |
| `pricing` | array | 定价方案 |
| `footer.copyright` | string | 版权信息 |
| `footer.columns` | array | 页脚列 |

**三种输入方式**：

| 方式 | 触发语 | 处理流程 |
|------|--------|----------|
| 直接提供内容 | "帮我生成产品页，公司名是XXX…" | 解析关键信息 → 自动构建配置 → 生成 HTML |
| 提供 Markdown | "根据这个 markdown 生成网页：content.md" | 读取文件 → Frontmatter 作配置 → 正文作内容 → 生成 HTML |
| 提供 JSON/YAML | "用这个配置生成网站：config.json" | 读取校验 → 生成 HTML → 同时输出 `config.js` |

### 13.4 变量预留规范

所有可变内容使用双括号 `{{VARIABLE_NAME}}` 格式预留，便于后端对接与二次配置：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{PAGE_TITLE}}` | 页面标题 | 产品名称 - 首页 |
| `{{PAGE_DESCRIPTION}}` | 页面描述 | 现代化产品介绍页面 |
| `{{SITE_NAME}}` | 网站名称 | MyWebsite |
| `{{SITE_LOGO}}` | 网站 Logo | /img/logo.svg |
| `{{NAV_ITEMS}}` | 导航项 | JSON 数组格式 |
| `{{HERO_TITLE}}` | Hero 主标题 | 欢迎来到… |
| `{{HERO_SUBTITLE}}` | Hero 副标题 | 副标题内容 |
| `{{CTA_TEXT}}` | 按钮文字 | 立即注册 |
| `{{CTA_LINK}}` | 按钮链接 | /register |
| `{{FOOTER_TEXT}}` | 底部版权 | © 2024 公司名 |
| `{{IMAGE_SRC}}` | 图片路径 | /img/banner.jpg |
| `{{IMAGE_ALT}}` | 图片 alt | 描述文字 |

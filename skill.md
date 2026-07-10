---
name: wuxia-conquest-wechat-pipeline
agent_created: true
description: 武侠风攻坚手札一站式流水线：wuxia-conquest-card（内容策划 + 视觉规范）→ wuxia-avatar + ai-prompt-master（墨小颠配图）→ 前端实现 HTML（移动端 + 网页版）→ wechat-article（公众号图文模板填充）→ wechat-publisher（封面图 + 推送到公众号草稿箱）。当用户要求以攻坚手札风格生成技术难题攻克内容并推送到公众号时触发。覆盖"发现问题→三败→突破→新问题"的大事记叙事 + 墨小颠武侠配图 + 武侠风图文直推 + 公众号草稿箱发布全流程。
---

# Wuxia Conquest → WeChat 一站式发布流水线

## 流水线概览

本技能将五个子技能串联为一条完整的发布流水线：

```
wuxia-conquest-card        wuxia-avatar + ai-prompt-master       前端实现 HTML             wechat-article              wechat-publisher
  （内容策划+视觉规范）  →   （墨小颠武侠配图）              →  （移动端+网页版）  →   （公众号图文模板填充）   →   （封面图 + 草稿箱推送）
```

> **一句话**：用户给一个技术难题 → 输出到公众号草稿箱的武侠风攻坚手札图文（含墨小颠配图）。

## 触发场景

以下任一表述出现时触发：

- "把 XXX 技术难题写成攻坚手札，推到公众号"
- "用武侠大事记风格记录 XXX 攻坚过程，发布到微信"
- "把 XXX 的踩坑过程写成武侠手札发公众号"
- "生成 XXX 的攻坚手札并推送到草稿箱"
- "攻克 XXX 的武侠手札 + 发布公众号"

## 变量约定

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `{{AUTHOR_NAME}}` | `daner技术栈` | 作者署名 |
| `{{QR_CODE_IMAGE}}` | `../assets/qrcode_wechat.jpg` | 公众号二维码图片路径（相对 HTML 文件） |

> 用户在请求中指定了作者名（如"署名 XXX"），则覆盖默认值。

## 前置依赖

```bash
# 推送依赖
pip install pyyaml Pillow pygments

# 截图依赖（Playwright，如需要截图模式）
pip install playwright
playwright install chromium
```

## 流水线执行步骤

按以下顺序执行，每步完成后自动进入下一步：

---

### 阶段一：wuxia-conquest-card — 内容策划 + 视觉规范

**定位**：不是讲"这个技术是什么"，而是还原"这个难题是怎么被啃下来的"。

以「攻坚手札·大事记」编年体格式，逐阵记录攻坚的每一步。

#### 内容构建：四回目大事记

##### 壹回 · 兵临城下 → 【问题】

**目标**：让读者站在你的位置，看到同样的困难，感到同样的压力。

**写作要求**：
1. **场景还原**：用真实可感的场景开场，如"凌晨三点，CPU 飙到 95%"
2. **问题定义**：一句话说清核心矛盾——「A 和 B 不能同时满足，但业务要求两者必须兼得」
3. **已有方案为什么不够用**：它们的假设条件在这个具体场景下不成立
4. **赌注**：不解决会怎样？说真实损失
5. **结尾留钩子**：「前面有三座城要一座一座地破」

**组件**：`.crisis-scene` 军情急报 + `.stake-box` 赌注框

##### 贰回 · 逐鹿破阵 → 【探索】大事记

**目标**：读者跟着你一起试、一起败、一起学。

**写作要求**：至少 3 阵递进，每阵统一结构：

| 组件 | 写法 |
|------|------|
| **阵号 + 标签** | `第一阵 / 第二阵 / 第三阵` + `败`/`成` 标签 |
| **思路** `.be-attempt` | 为什么你觉得这能行？说直觉、推理、假设 |
| **沙盘推演** `.sandbox-box` | 技术逻辑推理链：因为 X，所以 Y，应该能 Z |
| **为什么败了** `.be-failure` | 具体、可复现的失败原因，最好有数字 |
| **悟到的** `.be-lesson` | 这次失败教给你什么？与下一阵有因果链条 |

**递进要求**：
- 第一阵 → 第二阵：暴露出某个假设是错的
- 第二阵 → 第三阵：发现是架构层面的问题
- 每一阵都比上一阵更接近问题本质

**字数建议**：每阵 200-400 字

##### 叁回 · 一剑封喉 → 【突破】

**目标**：让读者感受到「原来如此！前面三次失败都是在铺路！」

**写作要求**：
1. **决胜局思路**：必须说清它和前三阵的关系
2. **破阵时刻** `.breakthrough-box`：你看到了什么证据确信这次对了
3. **利器清单** `.arsenal-list`：2-3 个核心设计决策，每个回答：解决了前面哪阵的问题 / 不用会怎样 / 代价是什么
4. **总结**：一句话说出这道题的关键

##### 肆回 · 余波未平 → 【新问题】

**目标**：诚实面对每个解决方案都会引入新问题。

**写作要求**：
1. **新狼烟** `.new-threat`：2-3 个新问题，具体说清场景和临界条件
2. **展望** `.forward-path`：这套方法论的可复用价值
3. **攻坚者旁白**：结尾点睛——"技术攻坚的本质不是找到完美答案"

#### 攻坚者旁白 ⚔

各回转折处，每回至少 1 条。干练、幽默、像老兵的战后复盘：
- 失败后："当时觉得天塌了，现在想想——幸亏那一阵败了"
- 突破后："不是突然开窍，是前三阵已经把错误答案全排除了"

#### 视觉风格约束

- **配色 DNA**：宣纸底 `#f6f1e6` / 朱砂红 `#c43a31` / 金 `#b8943e` / 墨 `#1a1410`
- **排版**：大事记编年体，左侧竖线 + 菱形节点（失败朱砂红 / 突破金色圆）
- **材质**：宣纸帘纹 + 卷轴 box-shadow 立体感

#### 核心组件清单

| 区块语义 | 建议类名 |
|----------|----------|
| 封面核心字 | `.conquest-cover` |
| 军情急报 | `.crisis-scene` |
| 赌注框 | `.stake-box` |
| 大事记时间轴 | `.chronicle-log` |
| 大事条目 | `.battle-entry` |
| 思路 | `.be-attempt` |
| 沙盘推演 | `.sandbox-box` |
| 败因 | `.be-failure` |
| 悟到 | `.be-lesson` |
| 破阵时刻 | `.breakthrough-box` |
| 利器清单 | `.arsenal-list` |
| 新狼烟 | `.new-threat` |
| 展望 | `.forward-path` |
| 朱砂印章 | `.seal-box` |

---

### 阶段二：wuxia-avatar + ai-prompt-master — 墨小颠武侠配图

**定位**：为四回目内容生成墨小颠风格的武侠正文配图，把文章里的关键判断、流程、结构、状态或隐喻，变成一张压在宣纸上随手画出的解释草图。

> 墨小颠 IP：手绘线稿小人，头顶乱毛丸子头、腰挂朱砂红葫芦、松垮灰青袍子盖到脚、表情慵懒认真。墨小颠必须参与画面核心动作，不能只当装饰。技能包内置 IP 参考图 `wuxia-avatar/assets/xiaodian_ip_reference.png`，生成时用 img2img 继承角色形神。

#### 配图策略（谋篇）

先读阶段一四回目正文，提炼画面感强的认知锚点，出 shot list：

- 优先选：核心判断、两种状态对比、输入→输出流转、前后变化、常见陷阱、角色心境迁移、一句话洞察
- 默认 4-8 张，短文 1-3 张，长文别过 9 张。够用就好。
- 每张写：放在哪段落后 / 图主题 / 核心意思 / 章法 / 墨小颠动作 / 物件 / 批注词

#### 章法选型（九选一）

| 内容 | 章法 |
|------|------|
| 来龙→去脉，输入→输出 | 一章·行云流水 |
| 系统的某个局部 | 二章·管中窥豹 |
| A 对 B，新旧 PK，左右互搏 | 三章·双峰并峙 |
| 心态/状态/痛点的变化 | 四章·七情图谱 |
| 抽象概念，需要具象 | 五章·借物喻理 |
| 层次框架，武功体系 | 六章·九层之台 |
| 路径/成长/步骤 | 七章·曲径通幽 |
| 吐槽/过程/变化 | 八章·浮生三帧（漫画） |
| 一句话洞察，金句 | 九章·一语点穴 |

#### 生成执行（主路径：ai-prompt-master）

**调用 `@skill://ai-prompt-master` 生成配图**，墨小颠视觉 DNA 与 ai-prompt-master 8 模块映射：

| ai-prompt-master 模块 | 墨小颠填入内容 |
|---|---|
| 【风格】 | `Chinese ink brush painting × hand-drawn sketch` |
| 【艺术家】 | `Yoshida Seiji × Cai Guo-Qiang`（可据意境微调） |
| 【光影】 | `soft warm ambient light, candlelight feel` |
| 【色彩】 | `warm rice paper #f6f1e6, deep ink #1a1410, cinnabar #c43a31 accents, gold #b8943e highlights` |
| 【细节】 | `hand-drawn ink brush lines, rough xuan paper texture, calligraphy annotations` |
| 【主题】 | {章法描述 + 墨小颠动作 + 核心物件 + 核心意思} |
| 【创意】 | {此生造的隐喻——每次从正文长出来，不翻旧稿} |
| 【签名】 | `--no gradient, --no digital, --no vector, --no neon, --size 1024x768` |

**关键参数**：
- 以 `wuxia-avatar/assets/xiaodian_ip_reference.png` 作参考图走 img2img，命令加 `--image wuxia-avatar/assets/xiaodian_ip_reference.png --strength 0.55`
- 尺寸固定 4:3（如 1024x768），不要拼图
- 使用版本 A（经典版）`--count 1`

**退化路径**：ai-prompt-master 不可用时，直接使用 `image_gen` 工具，参考 `wuxia-avatar/references/prompt-template.md` 组装完整英文 prompt（含 IP 参考图描述），生成 1024x768 图片。

#### 验稿（关键，避免废图）

- 墨小颠只当看客 → 让他上手干
- 汉字笔画缺失/潦草/重叠/出现假名乱码 → 直接重生成，prompt 强调 `Chinese text ONLY, clearly legible Chinese calligraphy brush strokes`
- 缺锚点（bun/葫芦）→ 强化 prompt
- 像商业插画 → 强调手绘线稿、毛笔抖动

#### 归档

保存到 `generated-images/`，命名 `xiaodian_{序号}_{desc}.png`，不覆盖已有稿。最终交付 4-8 张配图供阶段三填充。

---

### 阶段三：前端实现 HTML 模板（移动端 + 网页版）

**定位**：基于阶段一的四回目内容 + 视觉规范 + 阶段二的墨小颠配图，从零实现自包含 HTML。

> 本流水线**不内置 HTML 模板文件**，由主 agent 按下方规范直接实现（原委托 `@skill://顶尖的前端产品` / `@skill://前端专家级工程师` 在独立环境下调用受限，降级为自实现，但组件清单与色值必须严格遵守）。

#### 实现要求

- **移动端 HTML**：宽 420px 固定，CSS 内联/自包含，用于截图或浏览器阅读
- **网页版 HTML**：响应式 max-width 820px，浏览器直接阅读，作为武侠风长文
- **配色 DNA**：宣纸底 `#f6f1e6` / 朱砂红 `#c43a31` / 金 `#b8943e` / 墨 `#1a1410`
- **排版**：大事记编年体，左侧竖线 + 菱形节点（失败朱砂红 / 突破金色圆），宣纸帘纹 + 卷轴 box-shadow 立体感
- **组件类名**：严格对齐阶段一「核心组件清单」（`.crisis-scene` / `.stake-box` / `.chronicle-log` / `.battle-entry` / `.be-attempt` / `.sandbox-box` / `.be-failure` / `.be-lesson` / `.breakthrough-box` / `.arsenal-list` / `.new-threat` / `.forward-path` / `.seal-box`）
- **必含位置（页脚）**：朱砂红底金边书法武侠印章，填充 `{{AUTHOR_NAME}}`；印章旁放公众号二维码，路径 `{{QR_CODE_IMAGE}}`
- **配图嵌入**：移动端/网页版中按 shot list 嵌入 `generated-images/xiaodian_*.png`，配图路径使用相对路径

#### 输出文件

```
output/{技术名词}_{时间戳}/
├── {技术名词}_{时间戳}_wuxia_conquest.html       ← 移动端 HTML（420px）
└── {技术名词}_{时间戳}_wuxia_conquest_web.html   ← 网页版 HTML（响应式）
```

---

### 阶段四：wechat-article — 公众号图文模板填充

**定位**：将攻坚手札内容填充到武侠风公众号图文模板，生成可直接推送到微信的纯内联样式 HTML。

#### 模板

基于 `wechat-article/assets/card_template_wx_article_wuxia.html`，所有样式写在 `style=""` 属性中（纯内联样式，绕过微信过滤）。

#### 微信安全清单

| 禁用项 | 原因 | 替代方案 |
|--------|------|----------|
| `<style>` 块 | 微信可能直接删除 | 所有样式写 `style=""` |
| `position: absolute/relative` | 被过滤 | 用流式布局 / 负 margin |
| `::before` / `::after` | 伪元素直接消失 | 用真实 `<span>` / `<div>` |
| `float: left/right` | 微信中不可靠 | 用 `<table>` 做网格布局 |
| `display: flex` | 部分场景失效 | 小范围可试，复杂布局用 `<table>` |

#### 模板变量填充

将阶段一产出 + 阶段二配图，映射到模板变量：

| 变量 | 内容来源 |
|------|----------|
| `{{ARTICLE_TITLE}}` | `<title>` 标签标题 |
| `{{KICKER}}` | 卷首封印文字，如「攻坚手札」 |
| `{{TITLE}}` | 正标题，如「攻克{技术名词}：三败出真知」 |
| `{{DECK}}` | 副标题，一句话定位 |
| `{{AUTHOR_NAME}}` | 作者署名 |
| `{{QR_CODE_IMAGE}}` | 公众号二维码路径 |
| `{{STORYTELLER_INTRO}}` | 说书人开场白（古风口吻引入） |
| `{{CHAPTER_WHAT_HEADER}}` | 壹回·兵临城下 标题 HTML |
| `{{CHAPTER_WHAT_BODY}}` | 场景还原 + 军情急报 + 赌注 |
| `{{CHAPTER_WHY_HEADER}}` | 贰回·逐鹿破阵 标题 HTML |
| `{{CHAPTER_WHY_BODY}}` | 至少 3 阵大事记 |
| `{{CHAPTER_HOW_HEADER}}` | 叁回·一剑封喉 标题 HTML |
| `{{CHAPTER_HOW_BODY}}` | 决胜局 + 破阵时刻 + 利器清单 |
| `{{CHAPTER_PROBLEMS_HEADER}}` | 肆回·余波未平 标题 HTML |
| `{{CHAPTER_PROBLEMS_BODY}}` | 新狼烟 + 展望 |
| `{{ILLO_WHAT/WHY/HOW/PROBLEMS}}` | 墨小颠配图 HTML（阶段二产出） |
| `{{SEAL_TEXT}}` | 印章文字（2-4字），如「攻克」 |
| `{{REFERENCES}}` | 参考文献列表 |

#### 文件写入

```
output/{技术名词}_{时间戳}/{技术名词}_{时间戳}_wx_article_wuxia.html
```

---

### 阶段五：wechat-publisher — 封面图 + 推送到公众号草稿箱

**定位**：生成 AI 封面图，并将阶段四生成的图文 HTML 推送到微信公众号草稿箱。

#### 前置条件

微信配置已就绪（`wechat-publisher/config/wechat_config.secret.yaml` 中的 AppID/AppSecret 非占位值，由 `wechat_config.template.yaml` 复制填入）。

#### 生成封面图

**步骤 1**：构建 AI Prompt
```bash
python wechat-publisher/scripts/generate_cover_image.py prompt "{技术名词}" --style minimalist --palette tech
```

**8 套配色方案**（节选）：`tech`（深海蓝→极光青）、`warm`（暖米白+焦糖棕）、`dark`（纯黑+香槟金）、`cyber`（深空紫+霓虹粉）等。

**步骤 2**：AI 生图（`image_gen` 生成 1024×1024）

**步骤 3**：裁剪到 900×383
```bash
python wechat-publisher/scripts/generate_cover_image.py crop \
  -i raw.png \
  -o output/{技术名词}_{时间戳}/{技术名词}_{时间戳}_cover.png
```

#### HTML 直推公众号草稿箱

**[CRITICAL]** 核心推送命令：

```bash
python wechat-publisher/scripts/push_to_wechat_draft.py \
  "output/{技术名词}_{时间戳}/{技术名词}_{时间戳}_wx_article_wuxia.html" \
  --upload-images \
  --title "{营销标题}" \
  --author "daner" \
  --cover-image "output/{技术名词}_{时间戳}/{技术名词}_{时间戳}_cover.png"
```

> Windows/PowerShell 注意：脚本打印 emoji 在 GBK 环境下会崩溃，执行前需设 `$env:PYTHONIOENCODING='utf-8'`。

**`--upload-images` 自动处理**：
1. 扫描 HTML 中所有 `<img src="…">` 标签
2. 本地路径 → 上传到微信 CDN → 替换为微信 URL
3. 远程 URL → 跳过
4. 不存在的文件 → 跳过并警告

#### 推送完成确认

推送完成后告知用户：
- ✅ 草稿已创建
- 📷 文中图片已上传到微信 CDN
- 🖼 封面图状态
- 🔗 在公众号后台「草稿箱」可预览和编辑

---

## 营销标题规则

**[WARNING] 标题必须是营销标题**：禁止直接用技术名词 + 风格后缀。必须从**焦虑感 / 好奇心 / 获得感 / 社交货币 / 紧迫感**中选题，≤32 字。

### 标题公式速查

| 编号 | 公式模板 | 适合场景 |
|------|----------|----------|
| **F1** | 搞懂`{X}`，`{领域}`你就横着走 | 单个核心技术 |
| **F2** | 被`{X}`虐哭后，我悟了这套`{比喻}` | 学习曲线陡峭的技术 |
| **F3** | 面试官问`{X}`，我掏出`{独家武器}` | 面试高频考点 |
| **F4** | 没用过`{X}`的`{岗位}`，`{严重后果}` | 行业趋势技术 |
| **F5** | 把`{X}`画成`{画面}`，`{对象}`一看就懂 | 复杂概念可视化 |
| **F6** | 花了`{N}`小时搞懂`{X}`，现在`{N}分钟`讲给你听 | 高复杂度技术 |
| **F7** | `{N}`个问题，带你彻底搞懂`{X}` | 问题驱动结构 |

**标题铁律**：
1. 禁止说明书式标题（如"Docker 攻坚手札"）
2. 禁止空洞情绪词
3. 必须对位读者身份
4. ≤ 32 字，含标点
5. 每个标题提供 3 个候选

### 攻坚手札专属标题模板

| 编号 | 公式 | 示例 |
|------|------|------|
| **C1** | 攻克`{X}`，我败了`{N}`阵才想通 | "攻克ZooKeeper脑裂，我败了三阵才想通" |
| **C2** | `{X}`这个问题困了我`{N}`天，解法简单到不敢相信 | "Redis雪崩困了我三天，解法简单到不敢相信" |
| **C3** | 别再踩`{X}`的坑了，这是我的血泪手札 | "别再踩MySQL死锁的坑了，这是我的血泪手札" |

---

## 运营策略（涨粉导向）

### 情绪调动

1. **标题**：好奇心 + 获得感为第一驱动力，暗示"里面有真实的失败和转折"
2. **开场白**：用共鸣/反直觉/故事型钩子抓住注意力
3. **内容节奏**：共鸣 → 好奇/惊喜 → 获得感 → 成就感 → 警惕/信任 → 行动召唤

### 互动设计

- 每次"败了"的环节设悬念："如果是你，你会怎么改？评论区写下你的答案"
- 文末引导："你工作中遇到过什么'一计不成再生一计'的时刻？"
- 分享诱导："把这篇文章转给正在焦头烂额的同事——告诉他，你不是一个人在死磕"

---

## 完整交付物清单

```
output/{技术名词}_{时间戳}/
├── {技术名词}_{时间戳}_wuxia_conquest.html       ← 移动端 HTML（420px）
├── {技术名词}_{时间戳}_wuxia_conquest_web.html   ← 网页版 HTML（响应式）
├── {技术名词}_{时间戳}_wx_article_wuxia.html     ← 公众号图文 HTML（内联样式）
├── {技术名词}_{时间戳}_cover.png                 ← 封面图（900×383）
└── generated-images/
    └── xiaodian_*.png                            ← 墨小颠配图
```

---

## 依赖技能一览

| 技能 | 用途 | 在本流水线中的位置 |
|------|------|-------------------|
| `@skill://wuxia-conquest-card` | 内容策划 + 视觉规范 | 阶段一 |
| `@skill://wuxia-avatar` | 墨小颠武侠配图（画什么：章法/物件/批注） | 阶段二 |
| `@skill://ai-prompt-master` | prompt 结构化组装 + 生图（怎么画） | 阶段二 |
| `@skill://wechat-article` | 公众号图文模板填充 | 阶段四 |
| `@skill://wechat-publisher` | 封面图生成 + 推送草稿箱 | 阶段五 |

> HTML 制卡环节（阶段三）原本委托 `@skill://顶尖的前端产品` → `@skill://前端专家级工程师`，因独立环境调用受限，在本流水线中降级为按规范自实现 HTML 模板（组件清单与色值不变）。

---

## 两种发布模式对比

| 维度 | 图片直传（--image-files） | HTML 直推（--upload-images） |
|------|--------------------------|------------------------------|
| 视觉效果 | ✅ 完整保留（纹理/印章/渐变） | ✅ 基本保留 |
| 文字可选中 | ❌ | ✅ |
| 代码可复制 | ❌ | ✅ |
| 微信兼容性 | ✅ 不受 CSS 过滤影响 | ⚠️ 受微信 CSS 过滤限制 |
| 推荐场景 | 追求视觉还原 | 追求阅读体验 |

---

## 常见错误避免

- **概念别混淆**：相近技术名词必须厘清边界
- **失败原因要具体**：不要"性能不够"，要说"10万 QPS 下锁竞争占 80% 时间"
- **递进要有因果**：每阵失败必须和下一阵思路有逻辑链条
- **标题别说明书式**：禁止"XXX 攻坚手札"这种标题
- **微信安全**：HTML 直推必须纯内联样式，不用 `<style>` 块和伪元素
- **配图锚点**：墨小颠必须上手干活，bun/葫芦不能丢；汉字必须清晰可读，乱码即重生成

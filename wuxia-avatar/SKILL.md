---
name: wuxia-avatar
description: 生成墨小颠风格的中文正文配图。用于用户要求为中文文章、帖子、博客、公众号、Notion 文档、技术卡片生成"墨小颠""武侠配图""小颠插图""正文配图""文章插图""配图建议""shot list"等任务；默认使用墨小颠 IP、宣纸底色、墨线手绘、朱砂金玉批注、简洁清爽但江湖气十足的视觉风格。
---

# 墨小颠 — 江湖散人手稿配图

## 核心定位

为中文文章设计和生成配图。目标不是做商业插画、PPT 信息图或山水画，而是把文章里的关键判断、流程、结构、状态或隐喻，变成一张**压在宣纸上随手画出的解释草图——画它的人是个穿旧袍子挂葫芦的江湖散人**。

默认视觉 IP 是**「墨小颠」**：手绘线稿小人，头顶乱毛丸子头、腰挂朱砂红葫芦、松垮灰青袍子盖到脚、表情慵懒认真。墨小颠必须参与画面的核心动作，不能只是站在旁边当装饰。

为保持跨图角色一致性，技能包内置一张预生成的**白底墨小颠 IP 参考图**：`assets/xiaodian_ip_reference.png`。生成新图时，优先以该图为参考走 **img2img** 模式，让 AI 在继承角色形神的基础上执行新的动作与场景。

## 🎨 首选生图方式：ai-prompt-master

**墨小颠配图的 prompt 组装和 API 调用，原生对接 `@skill://ai-prompt-master`。** ai-prompt-master 提供：

- **8 模块 prompt 结构**：风格 × 艺术家 + 光影 + 色彩 + 细节 + 主题 + 创意 + 签名
- **内置 Agnes AI API**：开箱即用的 `agnes_image.py` 脚本，无需配置
- **批量生图**：同一 prompt 生成 4 张变体，从中选最稳的
- **双版本策略**：版本 A（经典/稳定）+ 版本 B（创意/大胆）

墨小颠技能负责 **"画什么"**（章法选型、物件喻体、小颠动作、批注文案），ai-prompt-master 负责 **"怎么画"**（prompt 结构化组装 + API 调用）。

> 当 ai-prompt-master 不可用时，退化到直接写完整 prompt + 直接调用 `agnes_image.py`。集成细节见 `references/ai-prompt-integration.md`。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/style-dna.md`：色彩体系、宣纸画幅、线条语言、禁忌。
- `references/character_design.md`：墨小颠的形、神、动作、不可为（含 IP 参考图说明）。
- `references/composition-patterns.md`：九种章法、造喻三步法、江湖物件谱和动作谱。
- `references/prompt-template.md`：单张生图提示词模板（含 ai-prompt-master 8 模块映射 + img2img 参考图用法）。
- `references/qa-checklist.md`：落笔后自查。
- `references/ai-prompt-integration.md`：与 ai-prompt-master 的集成协议（风格/艺术家/光影/色彩模块推荐值 + img2img 参数）。
- `assets/xiaodian_ip_reference.png`：预生成的白底墨小颠 IP 参考图，img2img 时传入。


## 工作流

### 1. 观文

先读用户给的正文、链接、Markdown 或截图内容。提炼：

- 核心观点是什么
- 哪些段落是认知转折点
- 哪些内容用图比用文字更有穿透力
- 哪些地方只适合文字，不要硬配图

**不要平均配图。**优先选择有「画面感」的认知锚点：核心判断、两种状态对比、输入到输出的流转、分流与合流、前后变化、一个动作完成多个目的、常见陷阱、角色心境迁移、一句话洞察。

### 2. 谋篇（可选：先出配图策略）

如果用户说"分析怎么配图 / 思考哪些地方需要配图"，先给 shot list。每张图写：

- 放在哪个段落后
- 图的主题
- 核心意思
- 用哪种章法
- 墨小颠在图里做什么
- 画什么物件
- 批注什么词

默认 4-8 张。短文 1-3 张；长文也别轻易过 9 张。够用就好。

### 3. 落笔（生成单张 → PRIMARY：ai-prompt-master）

如果用户明确要求"生成 / 做图 / 输出"，立刻画，不停下来等确认。

#### 🔷 主路径：走 ai-prompt-master 全流程（带 IP 参考图）

**调用 `@skill://ai-prompt-master` 生成 1 张图**，尺寸固定 4:3（如 1024x768），不要拼图。

**关键：使用 `assets/xiaodian_ip_reference.png` 作为参考图走 img2img，确保每一张新图里的墨小颠都继承同一个角色的形、神、色。**

对接协议（详见 `references/ai-prompt-integration.md`）：

1. **传入参考图**：`--image assets/xiaodian_ip_reference.png`
2. **重绘强度**：`--strength 0.55`（保留角色，重画动作与场景；若场景变化大可提到 0.65，不建议超过 0.7）
3. **从墨小颠视觉 DNA → 映射 ai-prompt-master 8 模块**：
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

2. **使用版本 A（经典版）** 的完整 prompt 生图，`--count 1`（不是 4）

3. **ai-prompt-master 负责**：prompt 结构化组装 → 以 IP 参考图走 img2img → 自动调用 Agnes API → 下载保存

#### 🔶 退化路径：直接写完整 prompt + 直接调 Agnes API

当 ai-prompt-master 不可用时：

1. 从 `prompt-template.md` 取完整英文模板，填入章法、主题、物件、批注
2. 通过 Python 脚本直接调用（不走 PowerShell 管道，避免中文编码损坏）。退化路径也支持 img2img，以 `assets/xiaodian_ip_reference.png` 作为参考图：

```python
# 写入 prompt 到临时文件，脚本内直接读取
# 文生图：调用 agnes_image.py --size "1024x768" --count 1
# 图生图：调用 agnes_image.py --size "1024x768" --image "assets/xiaodian_ip_reference.png" --strength 0.55
# 输出到 generated-images/
# 文件名: xiaodian_01.png
```

**关键参数：**
- `--size "1024x768"` 固定 4:3 横版
- `--count 1` 只生成 1 张
- prompt 通过 Python 直接读取文件避开 PowerShell 管道编码问题

#### 3a. 选章法

根据内容选构图模式（见 composition-patterns.md）：

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

#### 3b. 组 Prompt

从 `prompt-template.md` 取模板，填入：

1. 这图讲什么
2. 用哪种章法
3. 核心意思（一句）
4. 画面怎么摆（墨小颠在哪、干嘛、什么物件、意怎么流）
5. 画什么物件（2-4件）
6. 批注什么词（3-5个短词）
7. 隐喻要新——每次从正文里长出来，不翻旧稿

**主路径**：将以上内容按 `references/ai-prompt-integration.md` 的模块映射表，填入 ai-prompt-master 的 8 模块结构中。
**退化路径**：填入 `prompt-template.md` 的完整英文模板中。

#### 3c. 对镜（确认角色锚点与参考图一致）

**每次生成前扫一眼** `character_design.md` 和 `assets/xiaodian_ip_reference.png`，确认：
- 乱毛 bun 在（第一锚）
- 朱砂红葫芦在（第二锚）
- 灰青旧袍 + 草鞋的气质与参考图一致
- 表情是放松/认真/会心，不是崩溃/卖萌/癫狂
- 他在干活，不是在站桩

### 4. 验稿

按 `qa-checklist.md` 逐项验。有问题优先重生成：

- 墨小颠只当看客 → 让他上手干
- 画面太挤 → 舍得删
- 太像说明书 → 换成手绘散人感
- 缺锚点（bun/葫芦）→ 强化 prompt
- 批注太多或错字 → 砍到 5 个以内
- 左上角有分类标题 → 局部编辑去掉
- 太可爱/太死板 → 调 prompt 里的气质
- 底色跑偏 → 强调宣纸底色
- 像商业插画 → 强调手绘线稿、毛笔抖动
- 汉字可读性问题，逐字逐句读——任何一笔不到位都可能毁掉整张图的可用性：
  - 汉字笔画缺失（如「大」变成「人」、「口」少一竖）→ 直接重生成，不要抱有侥幸
  - 汉字潦草到无法辨认 → 在 prompt 中强调「clearly legible Chinese calligraphy brush strokes」
  - 汉字重叠/粘连（两个字挤成一体）→ 减少该区域批注数量或增大间距
  - 汉字出现日文假名/韩文/乱码 → 在 prompt 最前面加「Chinese text ONLY」
  - 汉字颜色太浅或太细看不清 → 指定「dark ink #1a1410 brush strokes, bold enough to read」
  - 多个批注拥挤导致阅读障碍 → 砍批注到 3 个，拉开间距
  - 文字太小（如远低于画面 5%） → 要求「large enough Chinese characters, at least 8% of image height」
  - 出现英文单词与中文混排 → prompt 中明确「ALL text must be Chinese characters only, no English, no alphabet」

### 5. 归档

保存到 `generated-images/`，命名 `xiaodian_{序号}_{desc}.png`。

不覆盖已有稿。

## 交付格式

```
## 墨小颠画了 N 张

| # | 主题 | 章法 | 干嘛 | 小颠在干嘛 | 文件名 |
|---|------|------|------|-----------|--------|
| 1 | ... | ... | ... | ... | ... |

📁 generated-images/
✅ 最稳：第 X 张
⚠️ 可调：第 Y 张
```

让图自己说话，不写长篇画论。

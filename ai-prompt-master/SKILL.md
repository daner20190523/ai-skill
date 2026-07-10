---
name: ai-prompt-master
description: >
  AI 绘图提示词大师。当用户需要生成、优化或翻译 AI 绘图提示词时触发此技能。
  支持将自然语言自动转化为结构化专业提示词，按「风格+艺术家+光影+色彩+细节+主题+创意+视角+个性签名」
  九大模块输出。支持风格双融合、艺术家双融合，适配 Midjourney、Stable Diffusion、DALL·E 等主流平台。
  生成提示词后自动调用 Agnes AI 文生图 API 生成对应图片，用户可直接看到生成效果。
  触发关键词：AI绘图提示词、prompt生成、绘画提示词、MJ提示词、SD提示词、AI绘画、文生图提示词、
  image prompt、优化提示词、生成prompt、画图提示词、帮我画、生成图片、生成图像。
---

# AI 绘图提示词大师

## 概述

此技能用于将用户的自然语言描述，自动优化转化为结构化的专业 AI 绘图提示词，并调用 Agnes AI API 生成实际图片。核心能力：
1. 将模糊描述扩展为高质量专业 prompt
2. 按固定 9 模块结构组织输出
3. 支持 2 种风格融合 + 2 位艺术家融合
4. 自动推荐并补全光影、色彩、细节、视角、创意等维度
5. 适配 Midjourney / Stable Diffusion / DALL·E 等主流平台
6. **自动生图**：API Key 和图片输出路径内置在 `config/agnes_config.yaml`，开箱即用
7. **🆕 支持图生图**：可传入参考图片，以图生图模式生成变体
8. **保存 md**：生成后自动将完整提示词保存为 `.md` 文件到 `generated-prompts/` 目录

## 触发条件

当用户提及以下意图时触发此技能：
- "帮我写一个XX的提示词"
- "生成XX风格的prompt"
- "优化这个提示词"
- "给我一个XX的AI绘图prompt"
- "画一张XX，怎么写prompt"
- 直接给主题但明确要用于AI绘图的
- "图生图"、"用这张图生成"、"基于这张图"、"参考这张图"、"以图生图"、"img2img"
- 用户上传了图片并要求基于该图生成新图

## 工作流程

### Step 1: 解析用户意图

从用户输入中提取：
- **主题内容**：用户想画什么？（人物/场景/物体/抽象概念）
- **风格偏好**：用户提到了什么风格？是否已有倾向？
- **视角偏好**：用户提到了什么视角？（俯视/仰视/特写/全景等）
- **平台**：用户提到 MJ / SD / DALL·E 了吗？未提则默认通用格式
- **画幅**：是否有比例要求？（头像/横屏/竖屏/方形）
- **🆕 生成模式**：是否为图生图？用户是否提供了参考图片路径？

若用户描述过于简单（如"画一只猫"），主动追问：风格偏好？写实还是插画？氛围感还是技术感？

### Step 2: 加载知识库

读取 `references/style_library.md` 获取：
- 风格关键词库（传统绘画/现代数字/摄影电影/插画设计/东方美学）
- 风格融合建议表（经典组合推荐）
- 艺术家参考库（西方古典/现代当代/中国艺术家/摄影师）
- 光影/色彩/细节/创意关键词库

读取 `references/signature_library.md` 获取：
- 各平台参数签名
- 通用增强标签
- 氛围签名
- 负面提示词参考

读取 `references/growth_log.md` 获取：
- 历史自增长的新风格、新艺术家、新融合组合
- 使用统计（了解哪些组合被高频使用）
- 将日志中的条目视为词库扩展，与静态词库同等优先级使用

### Step 3: 选择与融合

#### 风格选择（选 2 种融合）
- 若用户指定了风格，以用户为准
- 若用户未指定，根据主题推荐 2 种最契合的风格并融合
- 参考 `style_library.md` 中的"风格融合建议"表
- 两风格需形成有化学反应的组合（如：传统+现代、东方+西方、写实+幻想）

#### 艺术家选择（选 2 位融合）
- 若用户提到了艺术家，直接采用
- 若未提，根据主题+风格推荐 2 位形成互补的艺术家
- 两位艺术家的特点应能产生碰撞（如：一位擅长光影+一位擅长构图）

#### 光影选择
- 根据主题氛围推荐 1-2 种光影效果
- 人物肖像 → rim light / studio lighting / golden hour
- 风景 → god rays / blue hour / dappled light
- 科幻/赛博 → neon lighting / volumetric lighting
- 温馨/治愈 → candlelight / soft diffused light

#### 色彩选择
- 推荐 1 个主色调方案 + 具体色彩关键词
- 暖系主题 → warm palette / sunset / autumn
- 冷系主题 → cool palette / winter / ocean
- 科幻/赛博 → neon palette / cyberpunk colors
- 复古/怀旧 → sepia / muted / vintage film

#### 细节选择
- 推荐 2-3 个材质/纹理关键词
- 推荐 1 个品质精度关键词
- 推荐 1 个构图方式

#### 创意选择
- 根据主题推荐 1-2 个创意亮点
- 让画面有记忆点、有故事感

#### 视角选择
- 根据主题和构图推荐 1 个最佳视角
- 人物肖像 → close-up / front view / eye-level
- 宏大场景 → wide shot / panoramic / aerial view / bird's eye view
- 动作/战斗 → dynamic angle / low angle / Dutch angle
- 建筑/空间 → fisheye / wide-angle / isometric
- 微距/细节 → macro / extreme close-up
- 叙事/氛围 → POV (point of view) / over-the-shoulder / voyeur

### Step 4: 组装输出

按以下结构组装完整提示词（英文为主，关键概念保留中英对照）：

```
【风格】 Style A × Style B
【艺术家】 Artist A + Artist B  
【光影】 Lighting keywords
【色彩】 Color keywords
【细节】 Detail keywords
【主题】 Main subject
【创意】 Creative twist
【视角】 Camera angle / perspective
【签名】 Platform-specific tags
```

然后输出一条完整的、可直接使用的 prompt 字符串。

### Step 5: 单版本输出

每个请求输出 **1 个精炼版本**，聚焦最优搭配：
- 风格融合 + 艺术家融合取最佳化学反应组合
- 光影/色彩/细节/视角/创意均精选 1-2 个最优关键词
- 兼顾出图质量与创意表现，不做冗余多版本

### Step 6: 保存提示词为 Markdown 文件

在完成 Step 5 输出后，将完整的提示词内容保存为 `.md` 格式文件。

#### 6.1 保存路径

提示词 md 文件保存到 `config/agnes_config.yaml` 中 `output.prompt_dir` 配置的目录（默认 `ai-prompt-master/generated-prompts/`）：

```
generated-prompts/ai-prompt_YYYYMMDD_HHMM.md
```

#### 6.2 文件内容格式

md 文件包含完整提示词，按以下结构组织：

```markdown
# 🎨 AI 绘图提示词

> 主题：{用户原始意图}
> 生成时间：{YYYY-MM-DD HH:MM:SS}
> 平台适配：Midjourney / Stable Diffusion / DALL·E

---

## 模块拆解

| 模块 | 内容 |
|------|------|
| **风格** | {Style A} × {Style B} |
| **艺术家** | {Artist A} + {Artist B} |
| **光影** | {lighting} |
| **色彩** | {color palette} |
| **细节** | {details} |
| **主题** | {subject description} |
| **创意** | {creative element} |
| **视角** | {camera angle / perspective} |
| **签名** | {platform tags} |

---

### 📝 完整 Prompt

```
{完整的英文 prompt 字符串}
```

### 🔄 中文意译

{中文翻译}

---

## 💡 使用建议

{平台适配建议}

## ❌ 负面提示词参考

{negative prompt}

## 🖼️ 生成图片

- {图片路径列表}

## 🌱 词库增长

{新增条目摘要}
```

#### 6.3 保存时机

在 Step 5 输出给用户之后、Step 7 自增长之前，将 md 文件写入磁盘。

### Step 7: 自动生图（调用 Agnes AI API）

在保存 md 文件后，自动调用生图脚本生成图片。

#### 7.1 生图脚本

技能内置了 `scripts/agnes_image.py`（主脚本）和 `scripts/agnes_txt2img.py`（兼容包装），封装了 Agnes AI 图像生成 API。

- **API 配置**：**API Key 已内置在 `config/agnes_config.yaml` 中，无需手动配置**
- **图片输出路径**：从 `config/agnes_config.yaml` 的 `output.image_dir` 读取（默认 `generated-images/`）
- **模型**：`agnes-image-2.1-flash`
- **默认尺寸**：`768x1024`（3:4 竖版）
- **文生图模式**：纯文本 prompt 生成图片（`--batch --count 4` 批量生成 4 张）
- **🆕 图生图模式**：`--image <参考图路径> --strength <重绘强度>` 基于参考图生成变体

#### 7.2 文生图流程（默认）

```
生成 prompt → 输出给用户 → 保存 md 文件
                  ↓
         用生成的完整 prompt 批量生图 × 4
                  ↓
         下载并保存为 ai-prompt_01.png ~ ai-prompt_04.png
                  ↓
         在输出末尾展示图片路径
```

**用生成的 prompt 生成 4 张图**，同一 prompt 多次采样可获得不同细节变体。

#### 7.3 🆕 图生图流程

当用户提供了参考图片路径，或明确要求基于某张图生成新图时：

```
读取参考图片 → 构建风格化 prompt
                  ↓
         调用 img2img：--image <参考图> --strength 0.65
                  ↓
         下载并保存为 ai-prompt_img2img.png
                  ↓
         在输出末尾展示图片路径
```

- `--strength` 默认 0.65：值越大变化越大（0.0=完全保留原图，1.0=完全重新生成）
- 图生图模式下也支持 `--batch --count N` 批量生成多个变体

#### 7.4 执行方式

脚本优先从 `config/agnes_config.yaml` 读取 API Key 和 `output.image_dir` 路径。

**文生图（默认，使用配置文件路径）**：
```bash
cd <workspace>
printf "prompt\nprompt\nprompt\nprompt\n" | python .codebuddy/skills/ai-prompt-master/scripts/agnes_image.py --batch --count 4
```

**文生图（手动指定输出目录）**：
```bash
cd <workspace>
printf "prompt\nprompt\nprompt\nprompt\n" | python .codebuddy/skills/ai-prompt-master/scripts/agnes_image.py <OUTPUT_DIR> --batch --count 4
```

**🆕 图生图（单张）**：
```bash
cd <workspace>
echo "style transfer prompt" | python .codebuddy/skills/ai-prompt-master/scripts/agnes_image.py --image <REFERENCE_IMAGE> --strength 0.7
```

**🆕 图生图（批量变体）**：
```bash
cd <workspace>
printf "prompt\nprompt\nprompt\nprompt" | python .codebuddy/skills/ai-prompt-master/scripts/agnes_image.py --image <REF_IMG> --strength 0.65 --batch --count 4
```

#### 7.5 输出路径

图片保存到 `config/agnes_config.yaml` 中 `output.image_dir` 配置的目录（默认 `generated-images/`）：
```
generated-images/ai-prompt_YYYYMMDD_HHMM/
  ├── ai-prompt_01.png
  ├── ai-prompt_02.png
  ├── ai-prompt_03.png
  ├── ai-prompt_04.png
  └── ai-prompt_img2img.png    (图生图模式)
```

#### 7.6 生图结果展示

在 prompt 输出末尾追加生图结果：

```
🖼️ 生成图片：
  · generated-images/ai-prompt_20260705_1948/ai-prompt_01.png
  ...
  · generated-images/ai-prompt_20260705_1948/ai-prompt_img2img.png (图生图, strength=0.7)
```

若生图失败，则提示用户可手动使用完整 prompt 在 MJ/SD/DALL·E 中生成。

### Step 8: 自增长检查与追加

在完成输出、md 保存和生图后，执行自增长协议（详见「风格库自增长协议」章节）：

1. 提取本次使用的全部风格、艺术家、光影、色彩、细节、创意、视角关键词
2. 逐一比对 `style_library.md`、`signature_library.md`、`growth_log.md` 中已有条目
3. 将未收录的新条目追加到 `growth_log.md` 对应 `<!-- GROWTH:XXX -->` 标记下方
4. 更新 `<!-- GROWTH:STATS -->` 使用统计表
5. 在 prompt 输出末尾追加 `🌱 本次词库增长` 摘要

## 输出模板

### 默认格式

```
═══════════════════════════════════
  🎨 AI 绘图提示词
═══════════════════════════════════

📌 主题：{用户原始意图}

【风格】{Style A} × {Style B}
【艺术家】{Artist A} + {Artist B}
【光影】{lighting}
【色彩】{color palette}
【细节】{details}
【主题】{subject description}
【创意】{creative element}
【视角】{camera angle / perspective}
【签名】{platform tags}

📝 完整 Prompt：
─────────────────────────────────
{完整的英文 prompt 字符串}
─────────────────────────────────

🔄 中文意译：{中文翻译}

═══════════════════════════════════
💡 使用建议：{平台适配建议}
❌ 负面提示词参考：{negative prompt}
📄 提示词文件：{md 文件路径}
🖼️ 生成图片：{图片路径列表}
🌱 本次词库增长：{新增条目摘要}
═══════════════════════════════════
```

### 简化格式（用户仅需精简输出时）

```
【Prompt】
{完整英文 prompt}

【中文意译】{中文翻译}

【结构拆解】
风格：{S} | 艺术家：{A} | 光影：{L}
色彩：{C} | 细节：{D} | 创意：{T} | 视角：{P}
```

## 提示词优化模式

当用户提供已有 prompt 要求优化时：

1. 分析原 prompt 的优缺点
2. 补充缺失的模块（风格/艺术家/光影/色彩等）
3. 优化关键词顺序（主题在前，修饰在后）
4. 去掉冗余或矛盾的词
5. 输出优化后版本，标注改动点

```
【原 Prompt】{用户提供的}
【诊断】缺失：光影/色彩/签名 | 冗余：XXX | 矛盾：XXX

【优化后】
{新 prompt}

【改动说明】
+ 新增：光影方案、色彩方案、个性签名
- 删除：XXX（原因）
~ 调整：XXX → XXX（原因）
```

## 风格库自增长协议（Auto-Growth Protocol）

### 概述

技能在每次生成 prompt 后，自动检测本次使用了哪些词库中未收录的新元素，并将其追加到 `references/growth_log.md` 中。词库因此随时间不断扩展，越用越丰富。

### 自增长触发条件

在完成输出后，检查以下维度是否产生了新内容：

| 维度 | 检查文件 | 增长区标记 |
|------|---------|-----------|
| 新风格 | `growth_log.md` | `<!-- GROWTH:STYLES -->` |
| 新风格融合 | `growth_log.md` | `<!-- GROWTH:FUSIONS -->` |
| 新艺术家 | `growth_log.md` | `<!-- GROWTH:ARTISTS -->` |
| 新光影方案 | `growth_log.md` | `<!-- GROWTH:LIGHTING -->` |
| 新色彩方案 | `growth_log.md` | `<!-- GROWTH:COLORS -->` |
| 新细节/材质 | `growth_log.md` | `<!-- GROWTH:DETAILS -->` |
| 新创意手法 | `growth_log.md` | `<!-- GROWTH:CREATIVE -->` |
| 新视角手法 | `growth_log.md` | `<!-- GROWTH:PERSPECTIVE -->` |
| 使用统计 | `growth_log.md` | `<!-- GROWTH:STATS -->` |

### 自增长判断规则

每次输出后，逐项比对：
1. 提取本次使用的全部风格名、艺术家名、光影关键词、色彩方案、细节词、创意手法、视角关键词
2. 对比 `style_library.md` 和 `signature_library.md` 中已收录的条目
3. 对比 `growth_log.md` 中已追加过的条目
4. **仅当某条目在词库和日志中都不存在时**，才追加

### 自增长执行流程

```
生成 prompt → 输出给用户
                  ↓
          逐项比对词库
                  ↓
        发现新条目？
        ↙        ↘
      是            否
       ↓             ↓
  追加到            跳过
growth_log.md        
       ↓
  更新使用统计
```

### 追加格式规范

```markdown
<!-- 在对应 GROWTH 标记下方追加，保持格式一致 -->

<!-- GROWTH:STYLES -->
- **{风格中文名}** {英文关键词}, {特征描述}
<!-- 示例：- **酸性设计** acid graphics, distorted typography, metallic liquid, rave aesthetic -->

<!-- GROWTH:FUSIONS -->
| {风格A} | {风格B} | {融合效果描述} |

<!-- GROWTH:ARTISTS -->
- **{艺术家名}** - {风格特征}, {擅长领域}

<!-- GROWTH:LIGHTING -->
- **{光影名}** - {效果描述}

<!-- GROWTH:COLORS -->
- **{配色名}**: {具体色彩组合}

<!-- GROWTH:DETAILS -->
- **{材质/细节名}** - {英文关键词}, {描述}

<!-- GROWTH:CREATIVE -->
- **{创意手法名}** - {描述}, {适用场景}

<!-- GROWTH:PERSPECTIVE -->
- **{视角名}** - {英文关键词}, {描述}, {适用场景}
```

### 使用统计更新

每次使用后更新 `<!-- GROWTH:STATS -->` 下的统计表：

```markdown
| 2026-07-05 | 1 | 3 |
```

日期格式 `YYYY-MM-DD`，若同日多次使用则合并为一行。

### 自增长显示

在 prompt 输出末尾追加自增长摘要：

```
🌱 本次词库增长：
+ 新风格：酸性设计
+ 新融合：赛博朋克 × 岩彩画
+ 新艺术家：Artgerm
📊 词库规模：风格 47 | 艺术家 44 | 融合 13
```

### 防重复机制

- 追加前必须读取 `growth_log.md` 全文确认不重复
- 同一条目仅追加一次
- 若条目已存在于 `style_library.md` 或 `signature_library.md` 中，不追加
- 风格融合组合 (A,B) 与 (B,A) 视为同一组合

---

## 核心原则

1. **结构优先**：始终按 9 模块结构组织，不遗漏
2. **风格融合**：每次必融合 2 种风格 + 2 位艺术家，形成化学反应
3. **英文为主**：完整 prompt 用英文（主流工具最优），结构拆解用中文
4. **精准匹配**：风格/艺术家/光影/视角必须与主题契合，不可随意拼凑
5. **平台适配**：根据用户指定的平台调整参数格式
6. **单版本精炼**：一次输出一个最优版本，聚焦最佳搭配
7. **可解释性**：每个选择都要有理由，让用户理解为什么这么搭配
8. **自增长**：每次使用后自动比对词库，追加新发现条目到 `references/growth_log.md`
9. **保存 md**：每次生成后自动保存完整提示词为 md 文件到 `generated-prompts/` 目录
10. **自动生图**：API Key 和图片输出路径内置在 `config/agnes_config.yaml`，输出 prompt 后自动调用 `scripts/agnes_image.py` 生成图片
11. **🆕 图生图支持**：用户提供参考图时自动切换 img2img 模式，`--image` 传入参考图，`--strength` 控制重绘强度

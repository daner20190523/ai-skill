# ai-prompt-master 集成协议

墨小颠技能通过 `@skill://ai-prompt-master` 生成配图时的对接规范。

## 架构分工

```
┌─ wuxia-avatar ────────────────────┐
│  章法选型 → 物件喻体 → 小颠动作    │
│  → 批注文案 → 隐喻创意              │
│          ↓                         │
│  填入 8 模块映射表                  │
│          ↓                         │
├─ ai-prompt-master ────────────────┤
│  风格融合 → 艺术家配对              │
│  → 光影/色彩/细节/签名             │
│  → prompt 组装输出                 │
│  → 调用 Agnes API → 下载图片        │
└────────────────────────────────────┘
```

- **wuxia-avatar** 负责：章法选型、物件喻体、小颠动作、批注文案、隐喻创意
- **ai-prompt-master** 负责：8 模块 prompt 结构组装、风格/艺术家融合、API 调用、图片下载

## 调用规格

### 参考图（img2img）

**必须传入 IP 参考图**，以维持墨小颠跨图一致性。

| 项 | 设定 |
|----|------|
| 参考图路径 | `assets/xiaodian_ip_reference.png` |
| 模式 | img2img（图生图） |
| 默认强度 | `--strength 0.55` |
| 强度范围 | `0.45 ~ 0.70` |
| 强度含义 | 越低越像参考图（只变动作/场景）；越高越自由重画 |

**强度选择指南**：
- `0.45 ~ 0.55`：小颠站姿/神态基本不变，主要替换背景和道具（最稳）
- `0.55 ~ 0.65`：继承角色形神，重画动作与构图（默认推荐）
- `0.65 ~ 0.70`：动作幅度大、场景变化大时使用（不建议超过 0.70，否则容易丢锚点）

**传入方式**：
```bash
python .codebuddy/skills/ai-prompt-master/scripts/agnes_image.py \
  generated-images/xiaodian_01.png \
  --image wuxia-avatar/assets/xiaodian_ip_reference.png \
  --strength 0.55 \
  --size "1024x768"
```

### 尺寸

**`1024x768`**（4:3 横版）。墨小颠配图固定 4:3，不是 ai-prompt-master 默认的 3:4 竖版。

### 数量

**`--count 1`**（只生成 1 张）。墨小颠每张图是一个独立隐喻，不需要同一 prompt 生成 4 张变体。

如果用户要 AI 帮忙多选一，可以 `--count 4`，但默认 1 张。

### 版本

**只用版本 A（经典版）** 的 prompt 生成。版本 B 可能偏离墨小颠的视觉 DNA。

## 8 模块固定映射表

每次调用 ai-prompt-master 时，以下模块使用固定值（不随文章内容变化）：

### 【风格】Style × Style

```
Chinese ink brush painting × hand-drawn sketch
```

固定组合。如需微调，仅换第二风格：
- 需要更多留白 → `× zen minimalism`
- 需要更暖的氛围 → `× vintage illustration`
- 需要更轻快的节奏 → `× loose watercolor sketch`

**禁止**：
- `× anime` / `× manga` — 会让小颠变可爱风
- `× digital painting` / `× vector art` — 会丢失手绘毛笔感
- `× realistic` / `× photography` — 会丢失散人手稿气质

### 【艺术家】Artist + Artist

```
Yoshida Seiji + Cai Guo-Qiang
```

- **吉田诚治**：暖光氛围、治愈感空间、毛笔细节
- **蔡国强**：东方材料感、留白控制、爆破式笔触

可替换选项：
- 第二艺术家可选换 `Qi Baishi`（齐白石，水墨写意）或 `Zhang Daqian`（张大千，泼墨意境）
- 需要更多建筑/空间感 → `Hayao Miyazaki (background art only)`

### 【光影】Lighting

```
soft warm ambient light, candlelight feel, gentle paper-lamp glow
```

固定不变。墨小颠的世界永远是烛光或纸灯笼的光——柔暖、不刺眼、像老屋子里点盏灯。

### 【色彩】Color

```
warm rice paper #f6f1e6 as base, deep ink black #1a1410 for lines, 
cinnabar red #c43a31 for accents and gourd, gold #b8943e for 
single highlight point, jade green #3a7a4a for gentle annotations
```

固定不变。与 `style-dna.md` 的色彩体系一一对应。

### 【细节】Details

```
hand-drawn ink brush lines with slight wobble, loose sketch style, 
rough xuan paper texture, handwritten calligraphy annotations, 
uneven brush strokes, open airy composition with 40%+ negative space
```

固定不变。

### 【签名】Signatures

```
--no gradient, --no digital art, --no vector illustration, --no neon lighting, --no cute, --no mascot, --no big eyes, --no 3D render, --ar 4:3
```

固定不变。这些签名确保生成图不偏离手绘散人审美。

## 可变模块填写指南

以下 2 个模块每张图由 wuxia-avatar 动态填入：

### 【主题】Subject

按以下结构填入（英文）：

```
A small hand-drawn wuxia figure (墨小颠, messy bun + cinnabar gourd) 
{小颠在干嘛——从动作谱选 1 个动词} {章法的空间描述}。{物件列表，2-4 件}。
Core meaning: {一句话核心意思}。
Hand-brushed Chinese annotations: {批注1}, {批注2}, {批注3}。
```

### 【创意】Creative twist

```
{本文独有的隐喻——每次从正文重新长出来，不翻旧稿}
```

示例：
- "An old inkstone grinding time itself, each layer revealing deeper understanding"
- "A bamboo sieve filtering chaotic data streams, only golden insights passing through"
- "A compass cart rebuilt from broken parts, pointing not north but toward the right answer"

## 完整调用示例

当需要生成一张"行云流水"章法的配图时：

```
调用 @skill://ai-prompt-master 生成配图，规格如下：

尺寸：1024x768 (4:3)
数量：1 张
参考图：wuxia-avatar/assets/xiaodian_ip_reference.png
重绘强度：0.55
仅用版本 A

模块填入：
- 风格：Chinese ink brush painting × hand-drawn sketch
- 艺术家：Yoshida Seiji + Cai Guo-Qiang
- 光影：soft warm ambient light, candlelight feel
- 色彩：warm rice paper #f6f1e6, deep ink #1a1410, cinnabar #c43a31, gold #b8943e
- 细节：hand-drawn ink brush lines, slight wobble, loose sketch, calligraphy annotations, 40%+ negative space
- 主题：A small wuxia figure (墨小颠, messy bun + cinnabar gourd) pushing a massive stone mill, 
  raw data flowing in from top-left as rough grains, refined insights flowing out from bottom-right 
  as golden powder. Old inkstone and bamboo scroll nearby. 
  Core meaning: data flows through processing pipeline, each step refines and transforms.
  Annotations: 原料入, 碾磨, 过滤, 金粉出.
- 创意：A stone mill as a data pipeline — rough enters, refined exits — the millstone is ancient 
  but the data flowing through it is modern, creating surprise through temporal contrast.
- 签名：--no gradient --no digital --no vector --no neon --ar 4:3
```

## 退化路径

当 ai-prompt-master 不可用时，直接：

1. 使用 `prompt-template.md` 的完整英文模板拼出 prompt
2. 调用 `agnes_image.py` 生成。推荐以 IP 参考图走 img2img，保持角色一致：

```bash
# 退化路径：直接文生图
echo "完整英文 prompt" | \
  python .codebuddy/skills/ai-prompt-master/scripts/agnes_image.py \
  generated-images/xiaodian_01.png --size "1024x768"

# 退化路径：以 IP 参考图走 img2img（推荐）
echo "完整英文 prompt" | \
  python .codebuddy/skills/ai-prompt-master/scripts/agnes_image.py \
  generated-images/xiaodian_01.png \
  --size "1024x768" \
  --image wuxia-avatar/assets/xiaodian_ip_reference.png \
  --strength 0.55
```

## 验稿对比

| 检查项 | 主路径（ai-prompt-master） | 退化路径（直接调 API） |
|--------|--------------------------|----------------------|
| prompt 结构化 | ✅ 8 模块自动组装 | ❌ 手动拼完整英文 |
| 风格融合 | ✅ 自动融合 2 种风格 | ❌ 手动写入 |
| 色彩精度 | ✅ 模块化指定 | ⚠️ 混在长 prompt 中可能稀释 |
| 角色一致性 | ✅ 以 `assets/xiaodian_ip_reference.png` 走 img2img | ⚠️ 需手动传 `--image --strength` |
| 批量生图 | `--count 4` 可选 | `--count N` 手动指定 |
| 自增长 | ✅ 新风格/艺术家自动记入 growth_log | ❌ 不触发自增长 |

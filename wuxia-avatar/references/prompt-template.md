# 落笔模板 — 生图提示词

每张单独生成，不拼。

## 主路径：ai-prompt-master 8 模块映射（带 IP 参考图）

当通过 `@skill://ai-prompt-master` 生成时，将视觉 DNA 填入其 8 模块结构中，并**传入参考图 `assets/xiaodian_ip_reference.png` 走 img2img**（详见 `ai-prompt-integration.md`）。

| 参数 | 设置 |
|------|------|
| 参考图 | `--image assets/xiaodian_ip_reference.png` |
| 强度 | `--strength 0.55`（默认），可据动作幅度在 0.45-0.70 间调整 |
| 尺寸 | `--size 1024x768`（固定 4:3） |
| 数量 | `--count 1` |

### 模块填入速查

| 模块 | 固定值 | 可变部分 |
|------|--------|---------|
| 【风格】 | `Chinese ink brush painting × hand-drawn sketch` | 按意境可微调第二风格 |
| 【艺术家】 | `Yoshida Seiji + Cai Guo-Qiang` | 按意境可选换 1 位 |
| 【光影】 | `soft warm ambient light, candlelight feel` | — |
| 【色彩】 | `warm rice paper #f6f1e6, deep ink #1a1410, cinnabar #c43a31, gold #b8943e, jade #3a7a4a` | — |
| 【细节】 | `hand-drawn ink brush lines, calligraphy annotations, rough xuan paper, loose sketch` | — |
| 【主题】 | — | **填入**：章法场景描述 + 墨小颠动作 + 物件 |
| 【创意】 | — | **填入**：此生造的隐喻亮点 |
| 【签名】 | `--no gradient, --no digital, --no vector, --no neon --ar 4:3` | — |

### 主题模块填写示例

```
A small wuxia figure (墨小颠, messy bun + cinnabar gourd) {动作描述}
on warm xuan paper background. {章法构图描述}。{物件列表}。
Core meaning: {一句话意思}。
Handwritten Chinese annotations: {批注列表}。
```

---

## 退化路径：完整英文 prompt 模板

当 ai-prompt-master 不可用时，直接组装完整 prompt。若走 img2img，仍需在生成时传入 `assets/xiaodian_ip_reference.png` 作为参考图。

```text
Generate one standalone Chinese article illustration, lay-flat reading, 4:3 landscape ratio (1024x768).

Visual DNA:
Xuan paper (rice paper) background in warm off-white #f6f1e6 — NOT pure white #ffffff, NOT beige. Clean and flat, no paper texture patterns, no gradients, no shadows, no noise. Just the warm cream tone of handmade paper.

Hand-drawn ink brush line art. Slightly wobbly, uneven brush strokes, not mechanical vector lines, not polished commercial illustration. Lines use 墨 (ink) tones: deep ink #1a1410 for main subjects and structures, medium ink #3a3028 for secondary details, light ink #6b5e50 for faint background marks.

Color accents — used with extreme restraint:
- 朱砂 cinnabar red #c43a31: for key call-outs, warnings, important labels, AND 墨小颠's gourd at the waist
- 金 gold #b8943e: for THE single most important keyword or a subtle warm highlight glow — use sparingly, maybe once or not at all
- 玉 jade green #3a7a4a: for secondary notes, gentle annotations, state labels — optional, not every image needs it

Aesthetic: like an old wandering scholar (江湖散人) doodled a martial arts manual diagram on his scrap of rice paper — the lines are a bit crooked, the handwriting is a bit messy, but the meaning lands like a punch. Not instructional, not a textbook, not a product sketch. Just a guy with a gourd and too much experience drawing you the answer.

墨小颠 IP (REQUIRED):
A small hand-drawn wuxia 江湖 figure, ~2.5 heads tall, with these two MUST-HAVE visual anchors:
1. 【乱毛丸子头 bun】— messy black hair tied in a loose bun on top, with wild strands sticking out in all directions — THIS IS THE PRIMARY IDENTIFIER
2. 【朱砂红葫芦】— a tiny dark cinnabar-red gourd (#c43a31) hanging from a hemp rope at the waist — SECOND IDENTIFIER and the only colored personal item

Other features: loose gray-green robe (simple ink line sketch, not detailed), straw sandals (few strokes), narrow relaxed eyes with faint undereye line (subtle), bit of stubble (three faint brush strokes). Expression is relaxed, a little sleepy, but already locked onto the problem — warm, capable, slightly amused. NOT cute, NOT mascot-y, NOT big-eyes, NOT generic cartoon.

墨小颠 MUST perform the core action that drives the metaphor — he pushes, pulls, grinds, measures, builds, guards, points, writes. He is NOT a bystander. If you can remove 墨小颠 and the image still works, the image is wrong.

Theme:
{配图主题}

Structure:
{章法：行云流水 / 管中窥豹 / 双峰并峙 / 七情图谱 / 借物喻理 / 九层之台 / 曲径通幽 / 浮生三帧 / 一语点穴}

Core meaning:
{核心意思，一句话}

Scene composition:
{墨小颠在哪、干什么、什么物件、视觉流线怎么走}

Objects:
{物件1} / {物件2} / {物件3} / {物件4}

Hand-brush Chinese annotations (3-5 short labels, 2-6 characters each):
{批注1} / {批注2} / {批注3} / {批注4} / {可选5}

Color rules:
Deep ink #1a1410 for 墨小颠, main lines, structures. Medium ink #3a3028 for annotation text, secondary details. Cinnabar #c43a31 on 墨小颠's gourd AND on 1-2 critical annotations/warnings. Gold #b8943e optionally on ONE most important highlight. Jade #3a7a4a optionally on 1-2 gentle secondary notes. NO bright saturated red, NO orange, NO bright blue, NO neon, NO gradient fills.

Hard rules:
One image = one core idea. Main subject occupies 35-55% of canvas. At least 40% empty paper space. Warm xuan paper background only. Hand-drawn brush feel. NO title block in top-left corner. NO structure type label on image. NO formal diagram, NO PPT slide, NO course lecture layout. Each image invents its own fresh visual metaphor from the content. Do NOT reuse any previous composition. It should feel like a wandering scholar's notebook sketch, not a product design whiteboard.
```

## 局部编辑

去掉多余标题：

```text
Edit the provided image. Remove only the handwritten label "{要删除的文字}" from the top-left corner. Fill that area with matching warm rice paper background #f6f1e6. Preserve everything else exactly. Do not add new text or objects.
```

提升角色参与感：

```text
Regenerate: same core meaning, but 墨小颠 must be the one DOING the core metaphorical action — pushing, grinding, measuring, building, or operating the key object that explains the concept. Not standing beside a diagram. Keep xuan paper background, ink brush lines, cinnabar accents, messy bun + red gourd anchors.
```

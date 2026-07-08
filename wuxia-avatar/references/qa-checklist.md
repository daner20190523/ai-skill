# 墨检 — 落笔后自查

## 一票否决

- [ ] 底色是宣纸暖白 `#f6f1e6`（不是纯白 `#fff`，不是深米色）
- [ ] 有墨小颠，且有乱毛 bun + 朱砂红葫芦
- [ ] 墨小颠的形象与 `assets/xiaodian_ip_reference.png` 基本一致（img2img 参考图已传）
- [ ] 墨小颠在干核心活——不是在站桩/装饰/导游看戏
- [ ] 是全新造的隐喻，没有翻旧稿的老物件和旧构图

## 色过

- [ ] 主线和墨小颠用浓墨 `#1a1410`，批注和细节用行墨 `#3a3028`
- [ ] 朱砂 `#c43a31` 出现在葫芦 + 1-2 处关键批注，没滥用
- [ ] 金 `#b8943e` 只出现在最核心的一个点——或不存在（不需要硬塞）
- [ ] 玉 `#3a7a4a` 只出现在 1-2 处辅批——或不存在
- [ ] 没有橙色、没有亮蓝、没有荧光色

## 线过

- [ ] 手绘毛笔线感——不是钢笔机械线、不是矢量圆滑线
- [ ] 浓淡有层次——主体浓墨，细节行墨，最次要淡墨
- [ ] 结构开放透气——不画死板封闭框

## 气过

- [ ] 一张图只讲一个核心——没有试图一张讲三个道理
- [ ] 主体占 35%-55%，留空 ≥ 40%
- [ ] 批注 3-5 处，每处 2-8 字——没有大段说明
- [ ] 没有左上角的类型标题（"流程图""系统架构"等）

## 败相（发现了就重来）

- 宣纸没了——出现纯白底、商业白、科技灰
- 墨小颠没了识别锚——没 bun 或没葫芦
- 墨小颠变成吉祥物——大眼睛、卖萌、闪亮高光
- 画面挤成说明书——箭头太多、节点太多、每个都标注
- 批注变正文——变成大段解释
- 出现产品感物件——PPT 流程图、科技 UI、商业图标
- 构图跟已有案例雷同
- 角色动作像 stationery decoration——只是站在图旁边

## 救画术

| 病 | 药 |
|----|-----|
| 太呆了 | 让小颠上手干一个物理动作（磨、扛、拉、筛） |
| 太挤了 | 砍掉一半元素，只留一个动作 + 3 个批注 |
| 太可爱了 | 强调 relaxed, slightly sleepy expression / wandering scholar loose brush sketch / NOT cute NOT mascot |
| 太教材了 | 去掉硬框、整齐网格、类型标题；改成歪歪的手绘稿 |
| 太像旧作 | 保留意思，换掉全部物件和小颠动作 |
| 缺锚点 | 强化 messy bun on top + tiny cinnabar gourd at waist |
| 不像参考图 | 降低 img2img strength 到 0.45-0.55，并在 prompt 里强调 "same character face, same messy bun, same cinnabar gourd at waist" |
| 底色错了 | 强调 warm xuan paper background #f6f1e6 / NOT pure white / NOT beige |
| 色彩跑偏 | 强调 NO orange / NO bright blue / only cinnabar #c43a31 and gold #b8943e as accents |

## 字过

生成图里的汉字是核心信息载体——如果一个字的任意一笔画糊了、缺了、歪到认不出，整张图就不能用。此项必检、必严：

- [ ] 每个批注汉字能逐一辨认——逐一默念确认，一笔都不含糊
- [ ] 无笔画缺失（如「大」缺捺变「人」、「口」缺底横变冂）→ 有则重画
- [ ] 无笔画粘连（两字挤成一团分不出边界）
- [ ] 无日文假名（あいうえお⋯）、韩文（ᄀᄂᄃ⋯）、乱码混入
- [ ] 无英文单词/字母与中文混排（如出现「OK」「API」「Redis」→ 重画）
- [ ] 字体大小足够——至少占画面高度 5%-8%，手机上看也清晰
- [ ] 墨色够深——与宣纸底色形成清晰对比，不靠放大镜才能读
- [ ] 字数 ≤ 5 处批注，每处 2-8 字，总字数 ≤ 30
- [ ] 批注间距足够——字与字不挤，行与行不打

## 字相（发现了就重来）

- 出现不是中文的字符 → 在 prompt 最前面加「ALL text MUST be Chinese characters, no exception」
- 字糊了/太淡 → 强调「dark ink brush strokes, crisp edges」
- 字太密 → 砍批注数量到 3 个，拉开间距
- 字太小 → 要求「characters at least 8% of total image height」
- 笔画变形为装饰图案 → 强调「standard Chinese character forms, no stylization that reduces legibility」

## 救字术

| 病 | 药 |
|----|-----|
| 汉字缺笔少画 | prompt 加「each Chinese character must be complete with all strokes, standard form」 |
| 假名/韩文混入 | prompt 第一行加「Chinese text ONLY, no Japanese, no Korean」 |
| 字太淡看不清 | 指定「dark ink #1a1410, crisp calligraphy strokes」 |
| 字太小 | 指定「Chinese text fills at least 8%-12% of image height」 |
| 英文混入 | prompt 加「absolutely no English alphabet, all text is Chinese」 |
| 字挤成坨 | 减少批注数，prompt 加「spread text annotations apart with breathing room」 |
| 笔画变花纹 | 强调「plain brush strokes, standard character forms, not decorative script」 |

## 判画

好画 = 第一眼感觉是"谁在宣纸上随手画的？有点潦草但意思真准"，然后一眼看懂结构。

如果第一眼看着像 PPT、教程、商业海报、儿童绘本、或者别人家的产品草图——都不对。

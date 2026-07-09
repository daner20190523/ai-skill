# 前端架构模板参考

本文档提供各种前端项目模板的完整代码参考。

---

## 一、产品介绍页模板

### 1.1 index.html

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{{PAGE_DESCRIPTION}}">
  <title>{{PAGE_TITLE}}</title>
  
  <!-- 预连接 -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  
  <!-- 字体 -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
  
  <!-- CSS -->
  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/components.css">
  <link rel="stylesheet" href="css/utils.css">
  <link rel="stylesheet" href="css/main.css">
  
  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="{{SITE_FAVICON}}">
</head>
<body>
  <div id="app">
    <!-- 头部导航 -->
    <header id="header" class="site-header">
      <div class="container">
        <a href="{{INDEX_URL}}" class="site-logo">
          <img src="{{SITE_LOGO}}" alt="{{SITE_NAME}}" class="logo-img">
          <span class="logo-text">{{SITE_NAME}}</span>
        </a>
        
        <nav class="nav-menu">
          <ul class="nav-list">
            {{NAV_ITEMS}}
          </ul>
        </nav>
        
        <div class="header-cta">
          <a href="{{CTA_LINK}}" class="btn btn-primary">{{CTA_TEXT}}</a>
        </div>
        
        <!-- 移动端菜单按钮 -->
        <button class="menu-toggle mobile-hidden" aria-label="菜单">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </header>
    
    <!-- 主内容 -->
    <main id="main" class="site-main">
      
      <!-- Hero 区域 -->
      <section class="hero-section">
        <div class="container">
          <div class="hero-content">
            <div class="hero-text">
              <span class="hero-badge">{{HERO_BADGE}}</span>
              <h1 class="hero-title">{{HERO_TITLE}}</h1>
              <p class="hero-subtitle">{{HERO_SUBTITLE}}</p>
              <div class="hero-buttons">
                <a href="{{PRIMARY_BTN_LINK}}" class="btn btn-primary btn-lg">{{PRIMARY_BTN_TEXT}}</a>
                <a href="{{SECONDARY_BTN_LINK}}" class="btn btn-secondary btn-lg">{{SECONDARY_BTN_TEXT}}</a>
              </div>
              <div class="hero-stats">
                <div class="stat-item">
                  <span class="stat-value">{{STAT_VALUE_1}}</span>
                  <span class="stat-label">{{STAT_LABEL_1}}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{STAT_VALUE_2}}</span>
                  <span class="stat-label">{{STAT_LABEL_2}}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{STAT_VALUE_3}}</span>
                  <span class="stat-label">{{STAT_LABEL_3}}</span>
                </div>
              </div>
            </div>
            <div class="hero-visual">
              <div class="hero-image-wrapper">
                <img src="{{HERO_IMAGE}}" alt="{{HERO_IMAGE_ALT}}" class="hero-image">
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 客户Logo -->
      <section class="clients-section">
        <div class="container">
          <p class="clients-label">{{CLIENTS_LABEL}}</p>
          <div class="clients-grid">
            {{CLIENT_LOGOS}}
          </div>
        </div>
      </section>
      
      <!-- 功能特点 -->
      <section class="features-section" id="features">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">{{FEATURES_TITLE}}</h2>
            <p class="section-subtitle">{{FEATURES_SUBTITLE}}</p>
          </div>
          <div class="features-grid">
            {{FEATURES_ITEMS}}
          </div>
        </div>
      </section>
      
      <!-- 定价 -->
      <section class="pricing-section" id="pricing">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">{{PRICING_TITLE}}</h2>
            <p class="section-subtitle">{{PRICING_SUBTITLE}}</p>
          </div>
          <div class="pricing-grid">
            {{PRICING_ITEMS}}
          </div>
        </div>
      </section>
      
      <!-- FAQ -->
      <section class="faq-section" id="faq">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">{{FAQ_TITLE}}</h2>
          </div>
          <div class="faq-list">
            {{FAQ_ITEMS}}
          </div>
        </div>
      </section>
      
      <!-- CTA -->
      <section class="cta-section">
        <div class="container">
          <div class="cta-content">
            <h2 class="cta-title">{{CTA_SECTION_TITLE}}</h2>
            <p class="cta-subtitle">{{CTA_SECTION_SUBTITLE}}</p>
            <a href="{{CTA_SECTION_BTN_LINK}}" class="btn btn-lg">{{CTA_SECTION_BTN_TEXT}}</a>
          </div>
        </div>
      </section>
      
    </main>
    
    <!-- 页脚 -->
    <footer id="footer" class="site-footer">
      <div class="container">
        <div class="footer-grid">
          {{FOOTER_COLUMNS}}
        </div>
        <div class="footer-bottom">
          <p class="copyright">{{FOOTER_COPYRIGHT}}</p>
        </div>
      </div>
    </footer>
  </div>
  
  <!-- JS -->
  <script src="js/utils/dom.js"></script>
  <script src="js/utils/helper.js"></script>
  <script src="js/components/header.js"></script>
  <script src="js/components/footer.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
```

### 1.2 css/main.css

```css
/* ===== 主样式文件 ===== */

/* ===== Hero 区域 ===== */
.hero-section {
  padding: calc(var(--header-height) + var(--space-3xl)) 0 var(--space-2xl);
  background: linear-gradient(180deg, var(--color-bg-alt) 0%, var(--color-bg) 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -30%;
  right: -10%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, var(--color-primary) 0%, transparent 70%);
  opacity: 0.05;
  border-radius: 50%;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-2xl);
  align-items: center;
  position: relative;
  z-index: 1;
}

@media (min-width: 960px) {
  .hero-content {
    grid-template-columns: 1fr 1fr;
  }
}

.hero-text {
  max-width: 560px;
}

.hero-badge {
  display: inline-block;
  padding: var(--space-xs) var(--space-md);
  background: var(--color-primary);
  color: white;
  font-size: var(--font-size-sm);
  font-weight: 600;
  border-radius: var(--radius-full);
  margin-bottom: var(--space-md);
}

.hero-title {
  font-size: clamp(36px, 5vw, 56px);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: var(--space-md);
  color: var(--color-text);
}

.hero-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-light);
  margin-bottom: var(--space-lg);
  line-height: 1.7;
}

.hero-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.hero-stats {
  display: flex;
  gap: var(--space-xl);
  flex-wrap: wrap;
}

.stat-item {
  text-align: left;
}

.stat-value {
  display: block;
  font-size: var(--font-size-3xl);
  font-weight: 800;
  color: var(--color-text);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.hero-visual {
  display: flex;
  justify-content: center;
}

.hero-image-wrapper {
  width: 100%;
  max-width: 500px;
  aspect-ratio: 4/3;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ===== 客户 Logo ===== */
.clients-section {
  padding: var(--space-xl) 0;
  border-bottom: 1px solid var(--color-border);
}

.clients-label {
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-bottom: var(--space-lg);
}

.clients-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: var(--space-xl);
}

.client-logo-item {
  padding: var(--space-sm) var(--space-lg);
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-light);
  opacity: 0.5;
  transition: opacity var(--transition-base);
}

.client-logo-item:hover {
  opacity: 1;
}

/* ===== 区块通用样式 ===== */
.section-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.section-title {
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 800;
  margin-bottom: var(--space-sm);
}

.section-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-light);
  max-width: 600px;
  margin: 0 auto;
}

/* ===== 功能特点 ===== */
.features-section {
  padding: var(--space-2xl) 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
}

.feature-item {
  padding: var(--space-xl);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.feature-item:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.feature-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-bottom: var(--space-md);
}

.feature-title {
  font-size: var(--font-size-xl);
  font-weight: 700;
  margin-bottom: var(--space-sm);
}

.feature-desc {
  color: var(--color-text-light);
  line-height: 1.7;
}

/* ===== 定价 ===== */
.pricing-section {
  padding: var(--space-2xl) 0;
  background: var(--color-bg-alt);
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
  max-width: 1000px;
  margin: 0 auto;
}

.pricing-card {
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  position: relative;
  transition: all var(--transition-base);
}

.pricing-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-lg);
}

.pricing-card.featured {
  border-color: var(--color-primary);
}

.pricing-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: white;
  padding: var(--space-xs) var(--space-md);
  font-size: var(--font-size-sm);
  font-weight: 600;
  border-radius: var(--radius-full);
}

.pricing-name {
  font-size: var(--font-size-xl);
  font-weight: 700;
  margin-bottom: var(--space-xs);
}

.pricing-price {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: var(--space-xs);
}

.pricing-price span {
  font-size: var(--font-size-base);
  font-weight: 400;
  color: var(--color-text-light);
}

.pricing-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-light);
  margin-bottom: var(--space-lg);
}

.pricing-features {
  margin-bottom: var(--space-xl);
}

.pricing-features li {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) 0;
  border-bottom: 1px solid var(--color-border);
  font-size: var(--font-size-sm);
}

.pricing-features li:last-child {
  border-bottom: none;
}

.pricing-features .check {
  color: var(--color-accent);
  font-weight: bold;
}

/* ===== FAQ ===== */
.faq-section {
  padding: var(--space-2xl) 0;
}

.faq-list {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  border-bottom: 1px solid var(--color-border);
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg) 0;
  cursor: pointer;
  font-size: var(--font-size-lg);
  font-weight: 600;
  transition: color var(--transition-fast);
}

.faq-question:hover {
  color: var(--color-primary);
}

.faq-icon {
  font-size: var(--font-size-xl);
  transition: transform var(--transition-base);
}

.faq-item.active .faq-icon {
  transform: rotate(45deg);
}

.faq-answer {
  padding-bottom: var(--space-lg);
  color: var(--color-text-light);
  line-height: 1.7;
  display: none;
}

.faq-item.active .faq-answer {
  display: block;
}

/* ===== CTA ===== */
.cta-section {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  padding: var(--space-2xl) 0;
  text-align: center;
}

.cta-title {
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 800;
  margin-bottom: var(--space-sm);
}

.cta-subtitle {
  font-size: var(--font-size-lg);
  opacity: 0.9;
  margin-bottom: var(--space-xl);
}

.cta-section .btn {
  background: white;
  color: var(--color-primary);
}

.cta-section .btn:hover {
  background: var(--color-bg);
  transform: translateY(-2px);
}

/* ===== Footer ===== */
.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-xl);
  margin-bottom: var(--space-xl);
}

.footer-col h4 {
  font-size: var(--font-size-base);
  font-weight: 700;
  margin-bottom: var(--space-md);
}

.footer-col ul li {
  margin-bottom: var(--space-sm);
}

.footer-col a {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  transition: color var(--transition-fast);
}

.footer-col a:hover {
  color: white;
}

.footer-bottom {
  padding-top: var(--space-xl);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.copyright {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .nav-menu {
    display: none;
  }
  
  .header-cta {
    display: none;
  }
  
  .menu-toggle {
    display: flex;
  }
  
  .hero-stats {
    justify-content: center;
  }
  
  .hero-section {
    padding: calc(var(--header-height) + var(--space-xl)) 0 var(--space-xl);
  }
}
```

---

## 二、变量速查表

| 变量分类 | 变量名 | 说明 |
|----------|--------|------|
| **页面** | `{{PAGE_TITLE}}` | 页面标题 |
| | `{{PAGE_DESCRIPTION}}` | 页面描述 |
| **站点** | `{{SITE_NAME}}` | 网站名称 |
| | `{{SITE_LOGO}}` | Logo图片路径 |
| | `{{SITE_FAVICON}}` | Favicon路径 |
| **导航** | `{{INDEX_URL}}` | 首页链接 |
| | `{{NAV_ITEMS}}` | 导航项HTML |
| **Hero** | `{{HERO_BADGE}}` | 角标文字 |
| | `{{HERO_TITLE}}` | 主标题 |
| | `{{HERO_SUBTITLE}}` | 副标题 |
| | `{{HERO_IMAGE}}` | 主图路径 |
| | `{{HERO_IMAGE_ALT}}` | 主图alt |
| **按钮** | `{{CTA_TEXT}}` | CTA按钮文字 |
| | `{{CTA_LINK}}` | CTA按钮链接 |
| | `{{PRIMARY_BTN_TEXT}}` | 主按钮文字 |
| | `{{PRIMARY_BTN_LINK}}` | 主按钮链接 |
| | `{{SECONDARY_BTN_TEXT}}` | 次按钮文字 |
| | `{{SECONDARY_BTN_LINK}}` | 次按钮链接 |
| **统计** | `{{STAT_VALUE_1}}` | 数值1 |
| | `{{STAT_LABEL_1}}` | 标签1 |
| | ... | ... |
| **功能** | `{{FEATURES_TITLE}}` | 标题 |
| | `{{FEATURES_SUBTITLE}}` | 副标题 |
| | `{{FEATURES_ITEMS}}` | 功能项HTML |
| **定价** | `{{PRICING_TITLE}}` | 标题 |
| | `{{PRICING_ITEMS}}` | 定价项HTML |
| **FAQ** | `{{FAQ_TITLE}}` | 标题 |
| | `{{FAQ_ITEMS}}` | FAQ项HTML |
| **Footer** | `{{FOOTER_COLUMNS}}` | 列HTML |
| | `{{FOOTER_COPYRIGHT}}` | 版权文字 |

---

## 三、组件速查

### 导航项模板

```html
<li class="nav-item">
  <a href="{{LINK}}" class="nav-link{{IS_ACTIVE}}">{{TEXT}}</a>
</li>
```

### 功能项模板

```html
<div class="feature-item">
  <div class="feature-icon">{{ICON}}</div>
  <h3 class="feature-title">{{TITLE}}</h3>
  <p class="feature-desc">{{DESCRIPTION}}</p>
</div>
```

### 定价项模板

```html
<div class="pricing-card{{IS_FEATURED}}">
  {{HAS_BADGE}}
  <div class="pricing-name">{{NAME}}</div>
  <div class="pricing-price">{{PRICE}}<span>/{{PERIOD}}</span></div>
  <p class="pricing-desc">{{DESCRIPTION}}</p>
  <ul class="pricing-features">
    {{FEATURES}}
  </ul>
  <a href="{{LINK}}" class="btn {{BTN_CLASS}}">{{BTN_TEXT}}</a>
</div>
```

---

## 四、使用流程

1. **生成项目**：运行技能生成完整前端项目
2. **替换变量**：编辑所有 `{{VARIABLE}}` 为实际内容
3. **添加图片**：将图片放入 `img/` 目录
4. **修改样式**：根据需要调整 `css/` 中的样式
5. **添加交互**：在 `js/` 中添加自定义逻辑
6. **预览测试**：用浏览器打开 `index.html`
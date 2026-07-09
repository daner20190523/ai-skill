# 网站配置示例

本文档提供各种网站类型的完整配置示例。

---

## 一、博客配置示例

```json
{
  "site": {
    "name": "墨染博客",
    "title": "墨染博客 - 记录技术生活",
    "description": "一个专注于前端开发与设计的技术博客",
    "logo": "/img/logo.svg",
    "favicon": "/img/favicon.ico"
  },
  "nav": [
    {"text": "首页", "url": "/", "active": true},
    {"text": "归档", "url": "/archive.html"},
    {"text": "关于", "url": "/about.html"}
  ],
  "hero": {
    "badge": "欢迎访问",
    "title": "记录学习，分享思考",
    "subtitle": "热爱技术，专注于前端开发与用户体验设计",
    "image": "/img/hero-blog.png",
    "primaryBtn": {"text": "开始阅读", "url": "/articles"},
    "secondaryBtn": {"text": "了解更多", "url": "/about"}
  },
  "posts": [
    {
      "title": "如何从零开始学习前端开发",
      "excerpt": "分享我的前端学习路线，从HTML基础到React框架...",
      "category": "技术",
      "date": "2024-01-15",
      "views": 1250,
      "tags": ["JavaScript", "前端", "学习"],
      "url": "/article/frontend-learning"
    },
    {
      "title": "10个提高工作效率的VS Code插件",
      "excerpt": "介绍我日常开发中必用的10个VS Code插件...",
      "category": "工具",
      "date": "2024-01-10",
      "views": 980,
      "tags": ["VS Code", "效率", "工具"],
      "url": "/article/vscode-plugins"
    }
  ],
  "sidebar": {
    "author": {
      "name": "博主",
      "avatar": "👨‍💻",
      "bio": "热爱技术，专注前端，偶尔写写生活"
    },
    "categories": [
      {"name": "技术分享", "count": 28},
      {"name": "设计思考", "count": 15},
      {"name": "生活随笔", "count": 12}
    ],
    "hotPosts": [
      {"title": "如何从零开始学习前端开发", "views": 3500},
      {"title": "2024年Web开发趋势", "views": 2800}
    ]
  },
  "footer": {
    "copyright": "© 2024 墨染博客. 保留所有权利",
    "description": "记录技术生活，分享学习心得",
    "columns": [
      {
        "title": "快速链接",
        "links": [
          {"text": "首页", "url": "/"},
          {"text": "归档", "url": "/archive.html"},
          {"text": "关于", "url": "/about.html"}
        ]
      },
      {
        "title": "技术支持",
        "links": [
          {"text": "使用指南", "url": "/docs"},
          {"text": "常见问题", "url": "/faq"},
          {"text": "留言反馈", "url": "/contact"}
        ]
      }
    ]
  }
}
```

---

## 二、产品官网配置示例

```json
{
  "site": {
    "name": "产品名称",
    "title": "产品名称 - 为您带来极致体验",
    "description": "一款专为现代人打造的效率工具，帮助您更好地管理时间、提升效率",
    "logo": "/img/logo.svg",
    "favicon": "/img/favicon.ico"
  },
  "nav": [
    {"text": "首页", "url": "/", "active": true},
    {"text": "功能", "url": "#features"},
    {"text": "定价", "url": "#pricing"},
    {"text": "问答", "url": "#faq"}
  ],
  "hero": {
    "badge": "v2.0 新版发布",
    "title": "让工作更高效\n让生活更美好",
    "subtitle": "一款专为现代人打造的效率工具，帮助您更好地管理时间、提升效率、实现目标",
    "image": "/img/hero-product.png",
    "primaryBtn": {"text": "免费试用", "url": "/signup"},
    "secondaryBtn": {"text": "了解更多", "url": "#features"},
    "stats": [
      {"value": "10万+", "label": "活跃用户"},
      {"value": "4.9", "label": "用户评分"},
      {"value": "99.9%", "label": "可用率"}
    ]
  },
  "clients": {
    "title": "深受 thousands of 企业信赖",
    "logos": ["Google", "Microsoft", "Apple", "Amazon", "Meta"]
  },
  "features": [
    {
      "icon": "🚀",
      "title": "快速启动",
      "description": "几分钟内即可完成部署，快速上线您的产品"
    },
    {
      "icon": "⚡",
      "title": "高性能",
      "description": "优化的架构确保极致的加载速度和响应体验"
    },
    {
      "icon": "🔒",
      "title": "安全可靠",
      "description": "企业级安全防护，保障您的数据安全"
    },
    {
      "icon": "📊",
      "title": "数据分析",
      "description": "强大的数据分析功能，帮助您更好地了解用户"
    },
    {
      "icon": "🤖",
      "title": "智能自动化",
      "description": "自动化工作流程，减少重复劳动"
    },
    {
      "icon": "🌐",
      "title": "全球部署",
      "description": "覆盖全球的CDN节点，快速访问"
    }
  ],
  "showcase": [
    {"icon": "📱", "title": "移动端", "desc": "iOS & Android"},
    {"icon": "💻", "title": "桌面端", "desc": "Mac & Windows"},
    {"icon": "🌐", "title": "网页版", "desc": "浏览器直接访问"},
    {"icon": "🔌", "title": "API", "desc": "开放接口集成"}
  ],
  "pricing": [
    {
      "name": "免费版",
      "price": "¥0",
      "period": "/月",
      "description": "适合个人用户试用",
      "featured": false,
      "features": [
        "基础功能",
        "1GB 存储空间",
        "每月100次API调用",
        "社区支持"
      ],
      "btn": {"text": "免费开始", "url": "/signup"}
    },
    {
      "name": "专业版",
      "price": "¥99",
      "period": "/月",
      "description": "适合成长中的团队",
      "featured": true,
      "badge": "最受欢迎",
      "features": [
        "全部功能",
        "100GB 存储空间",
        "无限API调用",
        "优先支持",
        "团队协作"
      ],
      "btn": {"text": "立即开通", "url": "/signup"}
    },
    {
      "name": "企业版",
      "price": "¥599",
      "period": "/月",
      "description": "适合大型组织",
      "featured": false,
      "features": [
        "专业版全部功能",
        "无限存储空间",
        "专属客户经理",
        "定制开发",
        "SLA保障"
      ],
      "btn": {"text": "联系销售", "url": "/contact"}
    }
  ],
  "faq": [
    {
      "question": "如何开始使用？",
      "answer": "注册账号后即可免费开始使用，我们提供14天全功能试用。"
    },
    {
      "question": "支持哪些支付方式？",
      "answer": "我们支持微信、支付宝、银行卡等多种支付方式，企业用户也可对公转账。"
    },
    {
      "question": "数据安全如何保障？",
      "answer": "采用银行级加密技术，数据多重备份，符合ISO27001安全管理体系认证。"
    }
  ],
  "cta": {
    "title": "准备好开始了么？",
    "subtitle": "立即加入 thousands of 用户的行列，开启高效之旅",
    "btn": {"text": "免费试用 14 天", "url": "/signup"}
  },
  "footer": {
    "copyright": "© 2024 产品名称. All rights reserved.",
    "columns": [
      {
        "title": "产品",
        "links": [
          {"text": "功能介绍", "url": "#"},
          {"text": "定价方案", "url": "#"},
          {"text": "更新日志", "url": "#"},
          {"text": "API文档", "url": "#"}
        ]
      },
      {
        "title": "公司",
        "links": [
          {"text": "关于我们", "url": "#"},
          {"text": "博客", "url": "#"},
          {"text": "招聘", "url": "#"},
          {"text": "联系我们", "url": "#"}
        ]
      },
      {
        "title": "支持",
        "links": [
          {"text": "帮助中心", "url": "#"},
          {"text": "常见问题", "url": "#"},
          {"text": "联系客服", "url": "#"},
          {"text": "提交反馈", "url": "#"}
        ]
      },
      {
        "title": "法律",
        "links": [
          {"text": "服务条款", "url": "#"},
          {"text": "隐私政策", "url": "#"},
          {"text": "Cookie政策", "url": "#"}
        ]
      }
    ]
  }
}
```

---

## 三、个人主页/作品集配置示例

```json
{
  "site": {
    "name": "我的个人主页",
    "title": "张三 - 前端开发者",
    "description": "前端开发者，热爱技术和设计，专注于用户体验",
    "logo": null,
    "favicon": "/img/favicon.ico"
  },
  "profile": {
    "name": "张三",
    "title": "前端开发者",
    "avatar": "👨‍💻",
    "bio": "热爱技术和设计，专注于用户体验。3年前端开发经验，擅长React、Vue等主流框架。",
    "location": "北京",
    "email": "zhangsan@example.com",
    "github": "https://github.com/zhangsan",
    "twitter": "https://twitter.com/zhangsan"
  },
  "nav": [
    {"text": "首页", "url": "#home", "active": true},
    {"text": "关于", "url": "#about"},
    {"text": "技能", "url": "#skills"},
    {"text": "作品", "url": "#works"},
    {"text": "联系", "url": "#contact"}
  ],
  "hero": {
    "title": "你好，我是张三",
    "subtitle": "前端开发者 & 设计师",
    "description": "我致力于创造美观、易用的数字产品。"
  },
  "about": {
    "title": "关于我",
    "content": "我是一名专注于前端开发的设计师，喜欢将复杂的问题简单地解决。"
  },
  "skills": [
    {"name": "HTML/CSS", "level": 95},
    {"name": "JavaScript", "level": 90},
    {"name": "React", "level": 85},
    {"name": "Vue", "level": 80},
    {"name": "Node.js", "level": 75},
    {"name": "UI设计", "level": 70}
  ],
  "works": [
    {
      "title": "电商平台重构",
      "category": "网页设计",
      "image": "/img/work1.png",
      "tags": ["React", "UI/UX"],
      "url": "#",
      "description": "负责前端架构设计和实现"
    },
    {
      "title": "健身App设计",
      "category": "移动应用",
      "image": "/img/work2.png",
      "tags": ["React Native", "UI设计"],
      "url": "#",
      "description": "全流程设计开发"
    },
    {
      "title": "品牌视觉系统",
      "category": "品牌设计",
      "image": "/img/work3.png",
      "tags": ["VI", "品牌"],
      "url": "#",
      "description": "企业视觉形象设计"
    }
  ],
  "timeline": [
    {"year": "2024", "title": "加入ABC公司", "description": "担任高级前端工程师"},
    {"year": "2022", "title": "加入XYZ公司", "description": "开始前端开发职业生涯"},
    {"year": "2021", "title": "毕业于北京大学", "description": "计算机科学专业"}
  ],
  "footer": {
    "copyright": "© 2024 张三. 用心创作",
    "social": [
      {"name": "GitHub", "icon": "🐙", "url": "https://github.com/zhangsan"},
      {"name": "Email", "icon": "📧", "url": "mailto:zhangsan@example.com"}
    ]
  }
}
```

---

## 四、Markdown配置示例

有时用户会提供Markdown格式的内容，可以从中提取配置：

```markdown
---
title: 我的博客
description: 分享技术和生活的博客
logo: /img/logo.svg
author: 博主
---

# 导航
- [首页](/)
- [关于](/about)

## Hero
title: 欢迎来到我的博客
subtitle: 记录学习，分享生活

## 功能特点
- 🚀 快速: 极致的加载速度
- 💎 美观: 精心设计的界面
- 🔒 安全: 数据安全保障

## 底部
copyright: © 2024 我的博客
```

---

## 五、配置加载器代码 (config.js)

这是自动生成的配置文件，用于运行时加载配置：

```javascript
/**
 * 网站配置加载器
 * 自动读取 config.json 并应用到页面
 */

const SITE_CONFIG = {
  // 站点信息
  site: {
    name: '默认网站',
    title: '网站标题',
    description: '网站描述',
    logo: ''
  },
  
  // 导航
  nav: [],
  
  // Hero区域
  hero: {},
  
  // 功能特点
  features: [],
  
  // 定价
  pricing: [],
  
  // FAQ
  faq: [],
  
  // 页脚
  footer: {}
};

/**
 * 加载配置并应用
 */
function loadConfig() {
  // 1. 首先应用默认值
  applyConfig(SITE_CONFIG);
  
  // 2. 尝试加载 config.json
  fetch('config.json')
    .then(response => response.json())
    .then(config => {
      // 合并用户配置
      const mergedConfig = deepMerge(SITE_CONFIG, config);
      applyConfig(mergedConfig);
      console.log('配置已加载:', mergedConfig);
    })
    .catch(err => {
      console.log('使用默认配置:', err.message);
    });
}

/**
 * 应用配置到页面
 */
function applyConfig(config) {
  // 站点信息
  if (config.site) {
    if (config.site.title) {
      document.title = config.site.title;
    }
    const descMeta = document.querySelector('meta[name="description"]');
    if (descMeta && config.site.description) {
      descMeta.setAttribute('content', config.site.description);
    }
  }
  
  // 导航
  if (config.nav && config.nav.length > 0) {
    renderNav(config.nav);
  }
  
  // Hero
  if (config.hero) {
    renderHero(config.hero);
  }
  
  // 功能特点
  if (config.features && config.features.length > 0) {
    renderFeatures(config.features);
  }
  
  // 定价
  if (config.pricing && config.pricing.length > 0) {
    renderPricing(config.pricing);
  }
  
  // FAQ
  if (config.faq && config.faq.length > 0) {
    renderFaq(config.faq);
  }
  
  // 页脚
  if (config.footer) {
    renderFooter(config.footer);
  }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', loadConfig);
```

---

## 六、使用流程总结

1. **用户输入** → 提供内容或配置文件
2. **解析配置** → 将内容转换为结构化配置对象
3. **生成代码** → 生成HTML + CSS + JS + config.json
4. **运行时加载** → config.js 读取 config.json 并应用
5. **修改配置** → 用户可随时修改 config.json 调整内容

这样的设计确保了：
- ✅ 100% 配置化，无需修改代码
- ✅ 配置文件可复用
- ✅ 支持多种输入格式
- ✅ 网站完整性保证
# CalcTools - 免费在线计算器

## 功能全景图 — 完成度: 100%

> 项目定义：多语言静态计算器工具站（SEO 优化，纯前端计算）
> 当前阶段：已上线
> 下一步优先级：
> 1. 新增更多计算器类型
> 2. 接入 Google AdSense
> 禁止：无

CalcTools
├── 计算器（calculators/）
│   ├── BMI 计算器 — ✅
│   ├── 年龄计算器 — ✅
│   ├── 折扣计算器 — ✅
│   ├── 贷款计算器 — ✅
│   ├── 百分比计算器 — ✅
│   ├── 温度换算器 — ✅
│   ├── 小费计算器 — ✅
│   ├── 长度单位换算器 — ✅
│   └── 重量单位换算器 — ✅
├── 基础设施
│   ├── 构建系统（build.py） — ✅
│   ├── Docker 部署 — ✅
│   ├── Lucide SVG 图标 — ✅
│   └── E2E 测试（Playwright, 16用例） — ✅
└── 多语言
    ├── 英文 — ✅
    └── 中文 — ✅

## 技术栈

- 构建：Python 3.11 (build.py 模板渲染)
- 前端：纯 HTML/CSS/JS（无框架）
- 部署：Docker + nginx:alpine
- 测试：Playwright
- 图标：Lucide Icons (内联 SVG)

## 部署信息

- Mac Mini: `http://192.168.3.9:8234`
- 线上: `https://calculator-tools.todonot.com`

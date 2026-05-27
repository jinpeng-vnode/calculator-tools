# L1-TASK-001: calculator-tools MVP 上线设计

## 1. 需求摘要

将 calculator-tools 静态站点通过 Docker 容器化部署到 Mac Mini，包含：
- 多阶段 Docker 构建（Python 构建 + Nginx 服务）
- docker-compose 编排
- GitHub Actions CI 流水线
- hreflang 国际化 SEO 增强
- 项目启动文档模板

## 2. 方案选择

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 构建方式 | 多阶段 Dockerfile | 镜像最小化，构建产物不含 Python 运行时 |
| Web 服务器 | nginx:alpine | 轻量、高性能、默认配置即可服务静态文件 |
| 编排工具 | docker-compose | 单服务场景足够，部署简单 |
| CI 平台 | GitHub Actions | 项目已在 GitHub |
| hreflang 实现 | 模板变量注入 | 复用现有 {{key}} 模板引擎，零依赖 |

## 3. 文件结构

```
calculator-tools/
├── Dockerfile                  # 新增
├── docker-compose.yml          # 新增
├── .github/workflows/ci.yml    # 新增
├── .gitignore                  # 新增
├── PROJECT_BOOTSTRAP.md        # 新增
├── build.py                    # 修改（hreflang 变量注入）
├── templates/base.html         # 修改（hreflang 标签）
└── design/                     # 设计文档目录
```

## 4. 配置详情

### 4.1 Dockerfile

```dockerfile
# 阶段1：构建静态文件
FROM python:3.11-slim AS builder
WORKDIR /app
COPY build.py .
COPY templates/ templates/
COPY calculators/ calculators/
COPY static/ static/
RUN python build.py

# 阶段2：Nginx 服务
FROM nginx:alpine
COPY --from=builder /app/dist/ /usr/share/nginx/html/
EXPOSE 80
```

### 4.2 docker-compose.yml

```yaml
services:
  web:
    build: .
    ports:
      - "${PORT:-8080}:80"
    restart: unless-stopped
```

### 4.3 .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [dev, main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Build site
        run: python build.py

      - name: Verify output
        run: |
          test -d dist
          test -f dist/index.html
          test -f dist/en/index.html
          test -f dist/zh/index.html
          echo "✓ dist/ 验证通过"
```

### 4.4 .gitignore

```gitignore
dist/
__pycache__/
*.pyc
.env
```

### 4.5 hreflang 方案

#### 模板变量

在 `build.py` 的 `ctx` 字典中新增两个变量：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `alternate_lang` | 对应语言代码 | 当前 `en` → 值为 `zh`；当前 `zh` → 值为 `en` |
| `alternate_url` | 对应语言页面 URL | `https://calc.tools/zh/bmi/` |

#### templates/base.html 修改

在 `<head>` 中 `<link rel="canonical">` 之后添加：

```html
<link rel="alternate" hreflang="{{lang}}" href="{{canonical}}">
<link rel="alternate" hreflang="{{alternate_lang}}" href="{{alternate_url}}">
<link rel="alternate" hreflang="x-default" href="{{canonical}}">
```

#### build.py 修改逻辑

在 `build_calculator()` 函数中，构造 ctx 时添加：

```python
# hreflang：计算对应语言的 URL
alt_lang = "zh" if lang == "en" else "en"
alt_url = f"https://calc.tools/{alt_lang}/{calc_dir.name}/"

ctx = {
    # ... 现有字段 ...
    "alternate_lang": alt_lang,
    "alternate_url": alt_url,
}
```

在 `build_index()` 函数中同理：

```python
alt_lang = "zh" if lang == "en" else "en"
alt_url = f"https://calc.tools/{alt_lang}/"

ctx = {
    # ... 现有字段 ...
    "alternate_lang": alt_lang,
    "alternate_url": alt_url,
}
```

### 4.6 PROJECT_BOOTSTRAP.md 模板

```markdown
# PROJECT_BOOTSTRAP

## 环境信息

| 项目 | 值 |
|------|-----|
| 部署机器 | Mac Mini (___) |
| 宿主机端口 | ____ (8080-8099 范围，lsof 确认可用) |
| 域名 | calc.tools |
| Git 仓库 | https://github.com/jinpeng-vnode/calculator-tools |

## 首次部署步骤

1. 克隆仓库并切换分支
   ```bash
   git clone https://github.com/jinpeng-vnode/calculator-tools.git
   cd calculator-tools
   git checkout main
   ```

2. 检查端口可用性
   ```bash
   lsof -i :8080
   ```

3. 启动服务
   ```bash
   PORT=8080 docker compose up -d --build
   ```

4. 验证
   ```bash
   curl -I http://localhost:8080/en/
   ```

## 更新部署

```bash
git pull
docker compose up -d --build
```

## 回滚

```bash
git checkout <上一个稳定 commit>
docker compose up -d --build
```

## 注意事项

- 禁止修改宿主机 nginx/系统配置，一切在 Docker 内完成
- dist/ 不提交到 git，由 Docker 构建阶段生成
- 端口范围限制：8080-8099
```

## 5. 模块分配表

| 文件 | 负责角色 | 说明 |
|------|----------|------|
| `Dockerfile` | 全栈工程师 | 直接复制，无需修改 |
| `docker-compose.yml` | 全栈工程师 | 部署时确定 PORT 值 |
| `.github/workflows/ci.yml` | 全栈工程师 | 直接复制 |
| `.gitignore` | 全栈工程师 | 直接复制，提交后需从 git 移除已跟踪的 dist/ |
| `templates/base.html` | 全栈工程师 | 添加 hreflang 三行 |
| `build.py` | 全栈工程师 | 添加 alternate_lang/alternate_url 变量 |
| `PROJECT_BOOTSTRAP.md` | 全栈工程师 | 填写部署机器信息和端口 |

## 6. 开发者备注

1. **dist/ 清理**：当前 dist/ 已被提交到 git，需执行：
   ```bash
   git rm -r --cached dist/
   ```
   然后提交 .gitignore，之后 dist/ 仅由 Docker 构建阶段生成。

2. **端口选择**：部署时在 Mac Mini 上执行 `lsof -i :8080` 确认端口未被占用，如被占用则递增尝试 8081、8082...

3. **hreflang x-default**：设为与 canonical 相同（即当前语言页面），符合 Google 推荐做法——让搜索引擎根据用户语言自动选择。

4. **CI 触发分支**：dev 和 main 都触发构建验证，确保合并前代码可正常生成站点。

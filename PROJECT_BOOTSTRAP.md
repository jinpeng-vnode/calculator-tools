# PROJECT_BOOTSTRAP.md

## 项目概述
calculator-tools 是一个多语言（中/英）静态站点生成器，提供 9 种在线计算器工具。

## 技术栈
- 构建：Python 3.11（build.py 模板渲染）
- 服务：Nginx（Alpine Docker 镜像）
- 容器化：Docker + Docker Compose
- CI：GitHub Actions

## 本地开发
```bash
# 构建静态文件
python3 build.py

# Docker 本地运行
docker compose up --build
```

## 部署信息
- 服务器：Mac Mini (192.168.3.9)
- 端口：8080
- 部署方式：Docker Compose
- 分支：mvp-deploy/fullstack

## 部署命令
```bash
cd /home/jinpeng/calculator-tools
git pull origin mvp-deploy/fullstack
PORT=8080 docker compose up -d --build
```

## 目录结构
```
├── build.py              # 静态站点生成器
├── templates/            # HTML 模板
├── calculators/          # 计算器定义（JSON + logic.html）
├── static/               # 静态资源（CSS、favicon）
├── Dockerfile            # 多阶段构建
├── docker-compose.yml    # 容器编排
├── nginx.conf            # Nginx 配置
└── .github/workflows/    # CI 配置
```

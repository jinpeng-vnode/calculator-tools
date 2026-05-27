# 阶段1：构建静态文件
FROM python:3.11-slim AS builder
WORKDIR /app
COPY . .
RUN python build.py

# 阶段2：Nginx 服务
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

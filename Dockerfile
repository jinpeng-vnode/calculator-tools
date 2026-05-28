FROM python:3.11-slim AS builder
WORKDIR /app
COPY . .
RUN python3 build.py

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY blog /usr/share/nginx/html/blog
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

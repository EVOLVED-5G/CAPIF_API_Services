FROM nginxinc/nginx-unprivileged:latest

COPY ./nginx.conf /etc/nginx/nginx.conf

WORKDIR /app

RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
        chown -R nginx:nginx /var/cache/nginx && \
        chown -R nginx:nginx /var/log/nginx && \
        chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /tmp/nginx.pid && \
        chown -R nginx:nginx /tmp/nginx.pid

USER nginx
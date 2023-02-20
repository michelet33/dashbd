FROM nginx:1.23.3-alpine-slim

RUN apk update
RUN apk upgrade
COPY default.conf /etc/nginx/conf.d/default.conf
# COPY default.conf /etc/nginx/sites-available/default
EXPOSE 80/tcp
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
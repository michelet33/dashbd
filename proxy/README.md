
docker build -t nginx-reverse-proxy .

# docker run -it -p 172.28.208.1:80:80 -e NGINX_PORT=80 --name proxy nginx-reverse-proxy
docker run -it -p 172.25.16.1:80:80 -e NGINX_PORT=80 --name proxy nginx-reverse-proxy
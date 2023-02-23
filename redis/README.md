#docker run -d -p 192.168.1.129:6379:6379 -v /myredis/conf:/usr/local/etc/redis --name myredis redis redis-server /usr/local/etc/redis/redis.conf

docker build -t redis .
docker run -d -p 192.168.1.129:6379:6379  --name myredis redis


## Docker 실행하기
docker build --build-arg VITE_SERVER_URL=http://okt13.oktree.com:8000 -t bbs .
docker run --rm --name fastapi-bbs -v /data/www/fastapi-bbs/config:/app/config -p 8000:8000 --add-host=host.docker.internal:host-gateway bbs

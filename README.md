## Docker 실행하기
docker build -t bbs .
docker container rm bbs2
docker run --name bbs2 -it -v ./config:/app/config -p 8002:8002 bbs2

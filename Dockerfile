# 베이스 이미지로 ubuntu:22.04 사용
FROM ubuntu:22.04

WORKDIR /app

COPY . .

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

###################################################################################################################################
# Python
###################################################################################################################################
RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt install -y curl python3.9 python3-pip python3.10-venv build-essential libsasl2-dev python3-dev libldap2-dev libssl-dev

# Install Poetry in this Docker stage.
#RUN pip install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/1.5.1/install-poetry.py | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry ./ && \
    poetry config virtualenvs.create false

# Copy the pyproject.toml and poetry.lock files to the /tmp directory.
# Because it uses ./poetry.lock* (ending with a *), it won't crash if that file is not available yet.
COPY ./pyproject.toml ./poetry.lock* ./
#COPY ./gunicorn_conf.py ./

# Generate the requirements.txt file.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install the package dependencies in the generated requirements.txt file.
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 환경변수 설정 (옵션)
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8

###################################################################################################################################
# nodejs
###################################################################################################################################
WORKDIR /app/frontend

# nodejs 설치
RUN curl -s https://deb.nodesource.com/setup_16.x | bash
RUN apt install -y nodejs

ARG VITE_SERVER_URL
RUN echo "VITE_SERVER_URL=$VITE_SERVER_URL" > /app/frontend/.env.production

# 여러분의 현재 디렉토리의 모든 파일들을 도커 컨테이너의 /myapi 디렉토리로 복사 (원하는 디렉토리로 설정해도 됨)
#ADD . /myapi

# 8000번 포트 개방 (FastAPI 웹 애플리케이션을 8000번 포트에서 띄움)
EXPOSE 8000
ENV PORT 8000

# 작업 디렉토리로 이동
#WORKDIR /myapi

# 작업 디렉토리에 있는 requirements.txt로 패키지 설치
#RUN pip install -r requirements.txt

# npm install
RUN npm install
RUN npm run build

WORKDIR /app
# 컨테이너에서 실행될 명령어.
ENTRYPOINT [ "/bin/bash", "/app/entrypoint.sh" ]

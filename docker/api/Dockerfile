FROM python:3.9.14
WORKDIR /app

RUN apt-get update && apt install -y \ 
    libgl1-mesa-glx \
    curl  \
    libglib2.0-0 && apt-get clean 

RUN pip install --no-cache-dir \
    fastapi[all]==0.80.0 \
    service-streamer==0.1.2 \
    fastapi-health==0.4.0 \
    loguru==0.6.0  \
    ujson==5.5.0 \
    pydantic[email] \
    pydantic \
    PyJWT==2.5.0
RUN pip install --no-cache-dir \
    SQLAlchemy==1.4.39 \
    PyMySQL==1.0.2 \
    aiomysql==0.1.1 \
    bcrypt==3.2.2 \
    aiohttp==3.8.1 \
    redis==4.3.4 \
    aiocache==0.11.1 \
    aioredis==1.3.1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . /app
RUN chmod +x /app/docker/api/start.sh
ENTRYPOINT /app/docker/api/start.sh
FROM nginx:stable-alpine
ENV TZ=America/Los_Angeles

RUN apk add --no-cache \
    bash \
    py3-pip \
    python3

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN mkdir -p /data/html
WORKDIR /status
COPY source/nginx.conf /etc/nginx/nginx.conf
COPY . .

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

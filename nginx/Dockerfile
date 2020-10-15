FROM nginx:alpine
ENV TZ=America/Los_Angeles

RUN apk add --no-cache bash util-linux

COPY nginx.conf /etc/nginx/nginx.conf
COPY . .

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

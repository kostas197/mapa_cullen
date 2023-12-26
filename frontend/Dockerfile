FROM nginx:stable-alpine3.17

WORKDIR /usr/share/nginx/html

COPY . .

COPY default.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g daemon off;"]
FROM node:21.5.0-alpine3.19

WORKDIR /usr/src/app

COPY server/package.json ./

RUN npm install

COPY server/ .

CMD ["npm", "start"]
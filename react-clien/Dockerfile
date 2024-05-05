
# -- dockerfile for react app
FROM node:18-alpine as build

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

RUN npm run build

# -- dockerfile for nginx
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# -- end of dockerfile

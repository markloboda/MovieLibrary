FROM node:22-alpine

WORKDIR /app

COPY src/user_interface /app

RUN npm install

RUN npm run build

FROM nginx:alpine

COPY --from=0 /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

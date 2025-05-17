# 1. build stage
FROM node:18-alpine AS build
WORKDIR /usr/src/app

COPY package*.json ./
RUN npm ci
COPY client/ ./

# run your actual build command (e.g. npm run build)
# and make sure it outputs into dist/
RUN npm run build

# 2. serve with nginx
FROM nginx:stable-alpine
# copy the dist folder (not build)
COPY --from=build /usr/src/app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

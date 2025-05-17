# 1. build image
FROM node:18-alpine
WORKDIR /usr/src/app

# copy and install only production deps
COPY package*.json ./
RUN npm ci --only=production

# copy source & expose
COPY . .
EXPOSE 5000

CMD ["npm", "start"]

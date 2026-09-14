FROM node:24.15.0-bookworm-slim

WORKDIR /app

COPY package*.json ./

ENV NPM_CONFIG_LEGACY_PEER_DEPS=true
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM node:lts-slim AS builder

WORKDIR /usr/src/web

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN mkdir -p .persistent && touch .persistent/sqlite.db

ENV NODE_ENV=production
ENV SERVER_PORT=80
ENV LOG_DIR_PATH=logs
ENV IMAGES_DIR_PATH=/usr/src/web/.persistent/images
ENV SERVER_CORS_ORIGINS=https://localhost,http://localhost,https://localhost:3001,http://localhost:3001,https://localhost:8080,http://localhost:8080,https://digi.teschnik.de,http://digi.teschnik.de,https://digiapi.teschnik.de,http://digiapi.teschnik.de
ENV DATABASE_URL=file:///usr/src/web/.persistent/sqlite.db
ENV SERVER_URL=https://digiapi.teschnik.de
# fuck this, its not secure anyway
ENV DATABASE_AUTH_TOKEN=1234

RUN pnpm run db:generate
RUN pnpm run db:push
RUN pnpm run build-only

EXPOSE 80/tcp
CMD ["node", "dist/index.js"]

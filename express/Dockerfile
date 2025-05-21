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
ENV PORT=8080
ENV LOG_DIR=logs
ENV FRONTEND_URL=http://localhost
ENV DATABASE_URL=file:///usr/src/web/.persistent/sqlite.db
ENV DATABASE_AUTH_TOKEN=1234
ENV ABSOLUTE_IMAGES_DIR=/usr/src/web/.persistent/images

RUN pnpm run db:generate
RUN pnpm run db:push
RUN pnpm run build

EXPOSE 8080/tcp
CMD ["node", "dist/index.js"]

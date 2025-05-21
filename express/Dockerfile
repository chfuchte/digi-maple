FROM node:lts-slim AS builder

WORKDIR /usr/src/web

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN touch sqlite.db
RUN pnpm run db:generate
RUN pnpm run db:push
RUN pnpm run build

EXPOSE 8080/tcp

CMD ["pnpm", "start"]

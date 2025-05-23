FROM node:lts-slim AS builder
WORKDIR /usr/src/web

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build-only

FROM nginx:alpine
WORKDIR /usr/share/nginx/www
EXPOSE 80/tcp

COPY --from=builder /usr/src/web/dist .
COPY nginx.conf /etc/nginx/nginx.conf

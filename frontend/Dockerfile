FROM node:lts-slim AS builder
WORKDIR /usr/src/web
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
ENV VITE_API_BASE_URL="https://digiapi.teschnik.de"
RUN pnpm run build

FROM nginx:alpine
WORKDIR /usr/share/nginx/www
EXPOSE 80/tcp

COPY --from=builder /usr/src/web/dist .
COPY nginx.conf /etc/nginx/nginx.conf

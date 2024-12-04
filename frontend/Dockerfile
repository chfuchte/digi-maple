FROM node:lts-slim AS base
WORKDIR /usr/src/web
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

# install dependencies
FROM base AS install
RUN mkdir -p /temp/dev
COPY package.json pnpm-lock.yaml /temp/dev/
RUN cd /temp/dev && pnpm install --frozen-lockfile

# copy node_modules from temp directory
# then copy all project files (the code)
FROM base AS prerelease
COPY --from=install /temp/dev/node_modules node_modules
COPY . .
# building
ENV NODE_ENV=production
RUN pnpm run build

# copy build bundle to the final image
FROM base AS release
COPY --from=prerelease /usr/src/web/.output .output

# run the frontend-ssr-server
USER node
EXPOSE 3000/tcp
ENTRYPOINT [ "node", ".output/server/index.mjs" ]

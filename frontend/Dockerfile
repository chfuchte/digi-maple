FROM oven/bun:latest AS base
WORKDIR /usr/src/web

# install dependencies
FROM base AS install
RUN mkdir -p /temp/dev
COPY package.json bun.lockb /temp/dev/
RUN cd /temp/dev && bun install --frozen-lockfile

# copy node_modules from temp directory
# then copy all project files (the code)
FROM base AS prerelease
COPY --from=install /temp/dev/node_modules node_modules
COPY . .
# building
ENV NODE_ENV=production
RUN bun run build

# copy build bundle to the final image
FROM base AS release
COPY --from=prerelease /usr/src/web/.output .output
COPY --from=prerelease /usr/src/web/package.json .

# run the frontend-server
USER bun-maple
EXPOSE 3000/tcp
ENTRYPOINT [ "bun", "run", "start" ]

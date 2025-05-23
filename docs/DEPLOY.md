# Deployment

## Table of Contents

-   [Docker](#docker)
    -   [Without Traefik](#without-traefik)
    -   [With Traefik](#with-traefik)
-   [Manual Setup](#manual-setup)
    -   [Requirements](#requirements)
    -   [Express Backend](#express-backend)
    -   [Vite Frontend](#vite-frontend)

## Docker (recommended)

The docker setup is the recommended way to run the application in production since it stores the sqlite database and all uploaded files in a volume and uses nginx to serve the static files. Furthermore, you may use Traefik as a reverse proxy to handle SSL termination and routing.

### Simple Setup

The simplest way to run the application is to use the docker compose file.

```bash
docker compose up # takes docker-compose.yaml by default
docker compose -f docker-compose.yaml up # explicitly specify the file
```

### With Traefik

The Traefik setup requires a valid traefik installation and configuration with an external network `sv-internal`.
Make sure to create the network before running the docker compose command.

```bash
docker compose -f docker-compose.prod.yaml up
```

## Manual Setup

### Requirements

-   Node.js (v22.11.0 or later) would be great (just download the LTS https://nodejs.org)
-   pnpm (node package manager of choice) (https://pnpm.io/installation)

### Express Backend

The backend is an Express application. Please create a `.env` file in the root directory of the backend with the following content:

```env
NODE_ENV=production
SERVER_PORT=<port_of_the_server>
LOG_DIR_PATH=<path_to_logs_folder>
IMAGES_DIR_PATH=<absolute_path_to_persistent_images_folder>
SERVER_URL=<url_of_the_server_including_port_and_protocol>
SERVER_CORS_ORIGINS=<comma_separated_list_of_allowed_origins>
DATABASE_URL=file://<absolute_path_to_sqlite.db>
DATABASE_AUTH_TOKEN=<your_auth_token_for_the_sqlite_database> 
```

```bash
pnpm install # or the install command of your choices package manager

touch sqlite.db # create the sqlite db file if not exists

pnpm db:generate # or the db:generate command of your choices package manager
pnpm db:push # or the db:push command of your choices package manager
pnpm db:studio # optional: check if the database is created correctly

pnpm build # or the build command of your choices package manager
pnpm start # or the start command of your choices package manager
```

### Vite Frontend

The frontend is a Vite application. Please create a `.env` file in the root directory of the frontend with the following content:

```env
VITE_API_BASE_URL=<url_of_the_backend_inkluding_port_and_protocol>
```

```bash
pnpm install # or the install command of your choices package manager

pnpm build # or the build command of your choices package manager
pnpm preview # or the preview command of your choices package manager
```

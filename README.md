# Maple

## Table of contents

- [License](#license)

## How to run (with Express Backend)

### Requirements

- Node.js (v22.11.0 or later) would be great (just download the LTS https://nodejs.org)
- pnpm (node package manager of choice) (https://pnpm.io/installation)

### Install dependencies

```bash
pnpm install # or the install command of your choices package manager
```

### Setup environment variables

Create a `.env` file in the root directory of the project and add the following variables:

```env
PORT = 8080 # port of the server
FRONTEND_URL = http://localhost:5173 # dev url of vite (frontend)
LOG_DIR = logs # should create them inside of the express folder
DATABASE_URL = file:///absolute/path/to/sqlite.db
DATABASE_AUTH_TOKEN = dbauth2025
```

### Setup SQLite database

Create a file called `sqlite.db` (if not exists) in the root of the express folder (or where your env variable points to)


```bash
touch sqlite.db
```

Next apply the schemas via the following command:

```bash
pnpm db:generate # or the db:generate command of your choices package manager
pnpm db:push # or the db:push command of your choices package manager
# optional: check if the database is created correctly
pnpm db:studio # should open up drizzle studio in your browser
```

### Build

```bash
pnpm build # or the build command of your choices package manager
```

### Run

```bash
pnpm start # or the start command of your choices package manager
```

### Run frontend

```bash
cd ../frontend
pnpm install # or the install command of your choices package manager
pnpm dev # or the dev command of your choices package manager
```

## License

This project is licensed under the [GPL-3.0](LICENSE.txt).

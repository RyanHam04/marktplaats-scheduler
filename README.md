# marktplaats-scheduler

A scheduler built on top of [marktplaats-py](https://github.com/jensjeflensje/marktplaats-py).

The system allows users to create scheduled Marktplaats search jobs. A background worker executes these jobs at configurable intervals and sends notifications when new advertisements are found.

The project is still under active development. Expect breaking changes.

## Requirements

- Python 3.11+
- `uv`
- Docker

## Installation

Clone the repository.

```bash
git clone <repository-url>
cd marktplaats-scheduler
```

Install the dependencies.

```bash
uv sync
```

`marktplaats-py` is automatically installed from the latest GitHub version.

## Configuration

Create a `.env` file in the project root following structure of `.env.example`.

## Running
The following all have to be executed from the root of the project.


Start the database.

```bash
docker compose --env-file .env up -d database
```

Start the API.

```bash
uv run uvicorn backend.main:app --reload
```

Wait until the application has finished the initialization.

In another terminal, start the worker process.

```bash
uv run python -m backend.worker
```

When both are running, jobs can be created through the API.

## Goals

- Schedule Marktplaats searches at configurable intervals.
- Execute searches in the background.
- Send notifications when new advertisements are found.
- Allow users to duplicate and modify existing jobs.
- Be easy to self-host.
- Support multiple users with a simple authentication system.

## Non-goals

- Production-grade authentication.
- Enterprise-level security.

## Documentation

Documentation is currently minimal.

I'll add proper documentation once the project is a bit more stable, including:

- OpenAPI documentation
- Updated C4 diagrams
- API examples
- Deployment documentation

## Demo

https://github.com/user-attachments/assets/d8fee32e-1f9b-47ac-a02c-4ef4a2171c10

## Credits

This project is built on top of https://github.com/jensjeflensje/marktplaats-py.

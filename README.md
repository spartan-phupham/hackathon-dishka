# service_platform_py

This is a template project for a python microservice using FastAPI framework.
Python 3.12 recommended.

## Configure

1. Click 'Python Interpreter'
2. Choose "Add New Interpreter" -> "Add Local Interpreter..."
3. Choose "Poetry Environment" -> Click "Poetry Environment"
4. At "Base interpreter" click dropdown and choose interpreter suitable.
5. Click "OK"

## Setting

copy `.envs/fastapi/.env.example` to `.envs/fastapi/.env`, for local we can use `.envs/fastapi/.env.local`

```bash
export ENVIRONMENT=local
```

## DB

postgres and redis can be launched on docker
`docker-compose -f docker-compose.ci.yml up -d`

## Flyway

migrate
`cd sql && flyway migrate -user=local -password=local -url=jdbc:postgresql://localhost:5432/db_py && cd -`

clean & migrate:
`cd sql && flyway clean migrate -user=local -password=local -url=jdbc:postgresql://localhost:5432/db_py && cd -`

## Poetry

This project uses poetry. It's a modern dependency management tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m service_platform_py
```

## Testing

```bash
poetry run pytest -vv --cov="service_platform_py"
pytest -vv service_platform_py/tests/test_user.py::test_user_creation
```
Or run the test directly in IDE (Pycharm/VSCode)

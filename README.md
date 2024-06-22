# service_platform

This is a template project for a python microservice using FastAPI framework.
Python 3.12 recommended.

## Structure

```shell
.
├── Dockerfile.migration
├── poetry.lock
├── pyproject.toml
└── src
    └── service_1
        ├── Dockerfile
        ├── __init__.py
        ├── __main__.py
        ├── config.yaml
        ├── settings.py
        ├── api
        │   ├── controller
        │   │   └── controller_1
        │   └── manager
        │       └── manager_1
        ├── client
        │   └── client_1
        ├── core
        │   ├── errors
        │   ├── repository
        │   └── response
        ├── db
        │   └── db_1
        ├── helper
        ├── k8s
        │   ├── dev
        │   └── prod
        ├── service
        │   └── service_1
        ├── sql
        ├── tests
        └── worker
            └── worker_1
                ├── consumer
                ├── processor
                └── repository
```
## Configure

1. Click 'Python Interpreter'
2. Choose "Add New Interpreter" -> "Add Local Interpreter..."
3. Choose "Poetry Environment" -> Click "Poetry Environment"
4. At "Base interpreter" click dropdown and choose interpreter suitable.
5. Click "OK"

### Note: If you use vscode, please follow these steps to install Python venv

```shell
python3 -m venv .venv
source .venv/bin/active
```

## Setting

Edit setting values on config.yaml

*If an environment variable exists, that value will override the yaml variable

### Note: Please notice the working dir `src/service_platform`

For development:

```bash
export ENVIRONMENT=local
cp config.yaml config.local.yaml
```

## JWT

Generate JWT Secret key and Public key

```shell
ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f jwtRS512.key
openssl rsa -in jwtRS512.key -pubout -outform PEM -out jwtRS512.key.pub
```

Encode the key

```shell
cat jwtRS512.key | base64 
cat jwtRS512.key.pub | base64
```

## DB

Postgres and Redis can be launched on docker
`docker-compose up -d`

## Ollama
Download and install the Ollama https://ollama.com/download/mac
Install the `llama3` model
```shell
ollama run llama3
```
Pull the `mxbai-embed-large` embedding model
```
ollama pull mxbai-embed-large
```
To avoid vector dimemsion mismatch, please delete old index in elastic search by using
```
curl -X DELETE {open_search_endpoint}/{index_name} 
```
Or just using new index to store vector database

Try to call the Ollama with Llama3 model
```shell
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

## Flyway

Add the flyway.conf to sql folder

```text
flyway.url=jdbc:postgresql://localhost:5432/service_platform
flyway.user=local
flyway.password=local
flyway.locations=filesystem:./
flyway.sqlMigrationPrefix=V
flyway.sqlMigrationSeparator=__
flyway.table=schema_version
flyway.cleanDisabled=false
```

Flyway migrate
`cd sql && flyway migrate && cd -`

Flyway clean & migrate:
`cd sql && flyway clean migrate && cd -`

## Poetry

This project uses poetry. It's a modern dependency management tool.

To run the project use this set of commands:

```bash
poetry install
```

If we have a problem with `openssl` is already installed

```shell
export PYCURL_SSL_LIBRARY=openssl
export LDFLAGS=-L/opt/homebrew/Cellar/openssl@3/3.3.0/lib
export CPPFLAGS=-I/opt/homebrew/Cellar/openssl@3/3.3.0/include
```

Install the dependencies
```shell
poetry install
```

Start the application
```shell
python -m service_platform
```

## Testing

```bash
poetry run pytest -vv --cov="service_platform" .
```

Or run the test directly in IDE (Pycharm/VSCode)

### Run Test in IDE Pycharm (**Recommend**)

### Notes:

- Working directory should be in root path of
  application: `src/**`

## Debug in Local

### Start the localstack

Ref: https://docs.localstack.cloud/overview

Use docker-compose.yaml to start the localstack

```yaml
  localstack:
    container_name: "${LOCALSTACK_DOCKER_NAME:-localstack-main}"
    image: localstack/localstack
    ports:
      - "127.0.0.1:4566:4566"            # LocalStack Gateway
      - "127.0.0.1:4510-4559:4510-4559"  # external services port range
    environment:
      # LocalStack configuration: https://docs.localstack.cloud/references/configuration/
      - DEBUG=${DEBUG:-0}
      - SERVICES=s3
    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
```

Install the localstack and awscli-local cli

```shell
brew install localstack/tap/localstack-cli
brew install awscli-local
```

Create a new S3 bucket

```shell
awslocal s3 mb s3://service-platform-local --region us-west-2
awslocal sqs create-queue --queue-name example-worker-local --region us-west-2
```

Create cors-config.json

```
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"]
    }
  ]
}
```

```shell
awslocal s3api put-bucket-cors --bucket service-platform-local --cors-configuration file://{PATH_TO_YOUR_FOLDER}/cors-config.json
```

Use the environment variable to overwrite the AWS Endpoint URL by using localstack

```shell
AWS__ENDPOINT_URL=http://localhost.localstack.cloud:4566
AWS__SQS_QUEUE_URL=http://sqs.us-west-2.localhost.localstack.cloud:4566/000000000000/example-worker-local"
```

or update the `config.local.yaml` file

```yaml
aws:
  endpoint_url: "http://localhost.localstack.cloud:4566"
  sqs_queue_url: "http://sqs.us-west-2.localhost.localstack.cloud:4566/000000000000/example-worker-local"
```

List the current objects on localstack s3 bucket

```shell
awslocal s3api list-objects --bucket service-platform-local
```

```json
{
    "Contents": [
        {
            "Key": "36506883-4552-423d-9fc2-c2adf8dd46f8/cP8tFnYxnnHJaAI2jFUffejR7CCjEvFp.pdf",
            "LastModified": "2024-05-20T04:08:46+00:00",
            "ETag": "\"5afaf79789a776d81ec91ccbdc9fdaba\"",
            "Size": 142786,
            "StorageClass": "STANDARD",
            "Owner": {
                "DisplayName": "webfile",
                "ID": "75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a"
            }
        }
    ],
    "RequestCharged": null
}
```

list sqs message

```shell
awslocal sqs receive-message --queue-url http://sqs.us-west-2.localhost.localstack.cloud:4566/000000000000/locals3-sqs
```

```json
{
    "Messages": [
        {
            "MessageId": "3964f2b3-0afa-4520-88f3-a23dc7cb0606",
            "ReceiptHandle": "MTZhNDU1ZjctNjk0YS00ZjFmLWExZjYtMDg2YmRhMzU2MTkyIGFybjphd3M6c3FzOnVzLXdlc3QtMjowMDAwMDAwMDAwMDA6bG9jYWxzMy1zcXMgMzk2NGYyYjMtMGFmYS00NTIwLTg4ZjMtYTIzZGM3Y2IwNjA2IDE3MTYyODMxMTIuNjU4MTYx",
            "MD5OfBody": "7207c5c25dc295e037848f7917b60393",
            "Body": "{\"user_id\": \"9b31b971-273e-481a-a961-942f46f6b122\", \"s3_object\": \"documents/9b31b971-273e-481a-a961-942f46f6b122/4PuwOQFkp8FEJ07vbMG8dPH6Ey7W0tf6.pdf\"}"
        }
    ]
}
```

### Run project in Pycharm

- Set environment variable `ENVIRONMENT=local`, the file `config.local.yaml` will be
  effected. For production, we will use `config.local` instead
- Environment variable convention:
    - By
      following [pydantic parsing environment](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#parsing-environment-variable-values)
      document, use `__` for nested delimiter.
    - For example: `POSTGRES__DB_NAME=new_db_name` will
      replace `{"postgres":{"db_name":"local"}}`
- Apply & Run

```shell
python -m service_platform
```

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

* ruff
* pytest

You can read more about pre-commit here: https://pre-commit.com/

## FQA

### How to fix SSL error: unable to get local issuer certificate?
#### ERROR:
```
INFO:     127.0.0.1:59531 - "POST /api/user/google/login HTTP/1.1" 401 Unauthorized
ERROR:service_platform.settings:Error verify_access_token: Cannot connect to host www.googleapis.com:443 ssl:True [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)')]
```
#### FIX:
Install the necessary certificates for Python to verify SSL connections:
```bash
bash /Applications/Python*/Install\ Certificates.command
```

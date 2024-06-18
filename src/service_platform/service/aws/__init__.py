from service_platform.settings import settings

# Localstack issue
if settings.environment == "local":
    # localstack dummy credentials
    aws_credentials_dummy = {
        "aws_access_key_id": "dummy",
        "aws_secret_access_key": "dummy",
    }
else:
    aws_credentials_dummy = {}

import databases

from starlette.config import Config
from starlette.datastructures import URL, Secret

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
HTTPS_ONLY = config("HTTPS_ONLY", cast=bool, default=True)
SECRET_KEY = config("SECRET_KEY", cast=str)

DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)
TEST_DATABASE_URL = DATABASE_URL.replace(
    database="test_" + DATABASE_URL.database
)

OAWS_API_KEY = config("OAWS_API_KEY", cast=Secret)

# Auth0
AUTH0_AUDIENCE = config("AUTH0_AUDIENCE", cast=str)
AUTH0_CLIENT_ID = config("AUTH0_CLIENT_ID", cast=str, default="")
AUTH0_CLIENT_SECRET = config("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = config("AUTH0_DOMAIN", cast=str)
AUTH0_GRANT_TYPE = config("AUTH0_GRANT_TYPE", cast=str, default="")

# AWS
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", cast=str, default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str, default="")
AWS_CLOUDSEARCH_ENDPOINT = config("AWS_CLOUDSEARCH_ENDPOINT", cast=str)
AWS_REGION_NAME = config("AWS_REGION_NAME", cast=str, default="")

MAPBOX_ACCESS_KEY = config("MAPBOX_ACCESS_KEY", cast=str, default="")

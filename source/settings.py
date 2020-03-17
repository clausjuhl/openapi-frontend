from starlette.config import Config
from starlette.datastructures import URL, Secret

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
HTTPS_ONLY = config("HTTPS_ONLY", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", cast=Secret)

AUTH0_AUDIENCE = config("AUTH0_AUDIENCE", cast=URL)
AUTH0_CLIENT_ID = config("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = config("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = config("AUTH0_DOMAIN")
AUTH0_GRANT_TYPE = config("AUTH0_GRANT_TYPE")

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_CLOUDSEARCH_ENDPOINT = config("AWS_CLOUDSEARCH_ENDPOINT", cast=URL)
AWS_REGION_NAME = config("AWS_REGION_NAME")

MAPBOX_ACCESS_KEY = config("MAPBOX_ACCESS_KEY")
OAWS_API_KEY = config("OAWS_API_KEY")

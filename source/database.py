from databases import Database

from source import configuration

# Database
if configuration.TESTING:
    database = Database(configuration.TEST_DATABASE_URL, force_rollback=True)
else:
    database = Database(configuration.DATABASE_URL)

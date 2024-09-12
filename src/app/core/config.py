# Standard Library
from os import getenv

MYSQL_DIVE_DB = getenv("MYSQL_DIVE_DB", "localhost")
MYSQL_AQUA_PASSWORD = getenv("MYSQL_AQUA_PASSWORD", "root123")
MYSQL_AQUA_SERVER = getenv("MYSQL_AQUA_SERVER", "localhost")
MYSQL_AQUA_USER = getenv("MYSQL_AQUA_USER", "root")

CONTAINER_NAME = getenv("CONTAINER_NAME")
AZURE_CONNECTION_STRING = getenv("AZURE_CONNECTION_STRING")

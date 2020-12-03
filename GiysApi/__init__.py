"""Project package."""
from .containers import Container


container = Container()
container.config.from_ini('./GiysApi/config.ini')
logger = container.logger()


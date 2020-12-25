from .schema import SCHEMA
from .subprocess_server_manager import SubprocessServerManager

SubprocessServerManager(SCHEMA).start()

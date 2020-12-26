import logging
from pathlib import Path

from .schema import SCHEMA
from .subprocess_server_manager import SubprocessServerManager

logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            filename=Path(Path(__file__).parent, 'debug.log'),
        )
    ],
    level=logging.DEBUG
)

SubprocessServerManager(SCHEMA).start()

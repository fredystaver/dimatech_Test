import sys
from logging import getLogger

import uvicorn

from app.server import app
from core.config import config

logger = getLogger(__name__)

def start():
    if __name__ == "__main__":
        if len(sys.argv) < 2:
            logger.error("No target specified")

        target = sys.argv[1]
        if target == "app":
            uvicorn.run(
                app,
                host=config.app.host,
                port=config.app.port,
                reload=False,
                workers=1
            )
        else:
            pass


start()

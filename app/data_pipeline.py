import asyncio
import logging
from app.utilities.etl import run_etl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    asyncio.run(run_etl())

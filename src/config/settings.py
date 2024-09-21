import os
from loguru import logger

# Configure Loguru to write logs to a file
def configure_logging():
    logger.add("src/logs/scraper.log", level="INFO", format="{time} - {level} - {message}")

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "scraper_db"

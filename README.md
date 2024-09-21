<img src="https://iranhrmedia.com/wp-content/uploads/2023/01/jobinja.png" width=450>

# Jobinja Web Scraper

This project is a web scraper designed to extract information from the [Jobinja](https://jobinja.ir) website, a popular job listing website similar to Glassdoor and Indeed. The scraper extracts links and detailed page information (such as main, job, and about pages) and stores the data in a MongoDB database. The project is Dockerized to ensure a consistent environment and ease of deployment.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Scraper](#running-the-scraper)
- [Docker](#docker)
  - [Building the Docker Image](#building-the-docker-image)
  - [Running with Docker Compose](#running-with-docker-compose)
- [Configuration](#configuration)
- [Logging](#logging)

## Project Structure

```
scraper/
├── logs/
│   └── scraper.log
├── config/
│   └── settings.py
├── modules/
│   ├── __init__.py
│   ├── database.py
│   ├── fetch_html.py
│   ├── link_extraction.py
│   └── detail_scraper.py
├── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Features

- **Link Extraction**: Automatically extract job-related links from Jobinja pages.
- **Multi-threading**: Utilize threading to speed up the scraping process.
- **Detailed Page Scraping**: Extract detailed information from main, job, and about pages.
- **Dockerized Setup**: Easily deploy the scraper using Docker and Docker Compose.
- **Logging**: Comprehensive logging with Loguru to track scraping progress and errors.
- **Data Storage**: Store extracted data in a MongoDB database for easy querying and analysis.

## Requirements

- Docker
- Docker Compose

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/jobinja-web-scraper.git
   cd jobinja-web-scraper
   ```

2. Install dependencies locally (optional, for local development):
   ```sh
   pip install -r requirements.txt
   ```

## Running the Scraper

To run the scraper locally without Docker:

1. Start a MongoDB instance:
   ```sh
   mongod --dbpath /path/to/your/db
   ```

2. Execute the main script:
   ```sh
   python3 main.py
   ```

## Docker

### Building the Docker Image

To build the Docker image, navigate to the `scraper/` directory and run:
```sh
docker-compose build
```

### Running with Docker Compose

To run the scraper with Docker Compose:
```sh
docker-compose up --build
```

This command will:
1. Build the Docker image for the scraper.
2. Start the MongoDB service.
3. Start the scraper service and connect to the MongoDB container.

### Stopping the Services

To stop the services, press `Ctrl + C` and then run:
```sh
docker-compose down
```

## Configuration

The configuration settings for the scraper can be found in `config/settings.py`. Adjust the MongoDB URI and other settings as needed.

```python
import os
from loguru import logger

# Configure Loguru to write logs to a file
def configure_logging():
    logger.add("/app/logs/scraper.log", level="INFO", format="{time} - {level} - {message}")

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "scraper_db"
```

## Logging

The scraper logs are written to `logs/scraper.log` using the Loguru library. Log rotation is configured to manage log file sizes.


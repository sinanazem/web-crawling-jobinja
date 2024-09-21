import requests
import time
import threading
from loguru import logger
from pymongo import MongoClient
from src.modules.database import setup_mongo_client


# Define base URL and headers
base_url = "https://jobinja.ir/companies?page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Function to scrape a single page
def scrape_page(page_number, collection):
    url = base_url + str(page_number)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        page_data = {
            'page_number': page_number,
            'html_content': response.text
        }
        collection.insert_one(page_data)
        logger.info(f"Successfully scraped and stored page {page_number}")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while scraping page {page_number}: {http_err}")
    except Exception as err:
        logger.error(f"An error occurred while scraping page {page_number}: {err}")

# Function to scrape pages using threading
def scrape_pages_threaded(start_page, end_page, collection, num_threads=10, delay=2):
    def thread_scrape(thread_id, page_range):
        for page_number in page_range:
            scrape_page(page_number, collection)
            time.sleep(delay)  # Sleep to avoid overwhelming the server

    page_ranges = [
        range(start_page + i * (end_page - start_page + 1) // num_threads, 
              start_page + (i + 1) * (end_page - start_page + 1) // num_threads)
        for i in range(num_threads)
    ]

    threads = []
    for i, page_range in enumerate(page_ranges):
        thread = threading.Thread(target=thread_scrape, args=(i, page_range))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main function to run the scraper
def run_scraper(start_page, end_page, num_threads=10, delay=2):
    collection_html, collection_links, collection_pages = setup_mongo_client()
    scrape_pages_threaded(start_page, end_page, collection_html, num_threads, delay)



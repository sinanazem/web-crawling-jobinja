from loguru import logger
from src.modules.database import setup_mongo_client
from src.modules.fetch_html import fetch_html
from src.modules.link_extraction import process_html_content
from src.modules.detail_scraper import scrape_url_detail_pages, store_results_in_mongo
from src.modules.html_extractor import run_scraper as extract_html_content
from src.config.settings import configure_logging


def run_extractor():
    configure_logging()
    collection_html, collection_links, collection_pages = setup_mongo_client()

    # Process HTML content first to extract links
    extract_html_content(start_page=20, end_page=32, num_threads=10)
    process_html_content(collection_html, collection_links)

    # Scrape detailed pages and store results
    cursor = collection_links.find()
    for item in cursor:
        url_list = item['url_list']
        url_detail_pages = scrape_url_detail_pages(url_list)
        store_results_in_mongo(url_detail_pages, collection_pages)
        logger.success(f"Links on page {item['page_number']} have been processed and stored in MongoDB.")

# Run the extractor
if __name__ == "__main__":
    run_extractor()

from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from src.modules.fetch_html import fetch_html

def scrape_url_detail_pages(url_list):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_html, url): url for url in url_list}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                main_html, actual_url = future.result()
            except Exception as exc:
                logger.error(f"Error fetching {url}: {exc}")
                main_html, actual_url = None, url

            if main_html is None:
                results.append({"url": url, "main_page": {"html_content": ""}, "job_page": {"html_content": ""}, "about_page": {"html_content": ""}})
                continue

            result = {
                "url": url,
                "main_page": {"html_content": main_html if not actual_url.endswith('/jobs') else ""},
                "job_page": {"html_content": main_html if actual_url.endswith('/jobs') else ""},
                "about_page": {"html_content": ""}
            }

            if not actual_url.endswith('/jobs'):
                about_page_url = url + "/about"
                job_page_url = url + "/jobs"

                # Fetch about and jobs pages
                about_html, _ = fetch_html(about_page_url)
                jobs_html, _ = fetch_html(job_page_url)

                result["about_page"]["html_content"] = about_html
                result["job_page"]["html_content"] = jobs_html

            results.append(result)

    logger.info("Scraping completed for the given list of URLs")
    return results

def store_results_in_mongo(url_detail_pages, collection):
    collection.insert_many(url_detail_pages)
    logger.info("Data has been stored in MongoDB")

import requests
from loguru import logger

def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            if response.url.endswith('/jobs'):
                logger.info(f"{url} redirects to /jobs")
            return response.text, response.url
        else:
            logger.error(f"Failed to fetch {url} with status code {response.status_code}")
            return None, url
    except Exception as e:
        logger.error(f"An error occurred while fetching {url}: {e}")
        return None, url

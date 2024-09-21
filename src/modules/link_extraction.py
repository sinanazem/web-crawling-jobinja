from bs4 import BeautifulSoup
from loguru import logger

def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True, attrs={"class": "c-companyOverview"})]
    return links

def process_html_content(collection_html, collection_links):
    url_results = []
    cursor = collection_html.find()

    for item in cursor:
        page_number = item['page_number']
        html_content = item['html_content']
        links = extract_links(html_content)
        
        url_results.append({
            "page_number": page_number,
            "url_list": links
        })
        logger.info(f"Extracted links on page {page_number}")
        
    # Insert the results into the new collection
    collection_links.insert_many(url_results)
    logger.info("All links have been extracted and saved to the database.")

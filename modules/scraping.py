import requests
from bs4 import BeautifulSoup


def scrape_url(base_url) -> list:
    """
    Scrapes a URL looking for downloadable contents

    Args:
        base_url (list): A list of URLs to be scraped
    Returns:
        list: A list of download links scraped from the urls in the input
    """
    # Sending a GET request to the website

    scraped_data = {'available_downloads': []}

    for target in base_url.keys():
        r = requests.get(base_url[target])

        # Parsing the HTML content
        soup = BeautifulSoup(r.content, 'html.parser')

        extracted_url = base_url[target].split('/')[2]

        protocol = 'http://'

        # Extracting elements with the <a> tag to find possible downloads
        anchors = soup.find_all('a')

        # Looking for available downloads
        for anchor in anchors:
            if anchor.get('href').endswith('.csv'):
                scraped_data['available_downloads'].append(f'{protocol}{extracted_url}/{anchor.get("href")}')

    return scraped_data

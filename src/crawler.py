import requests 
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from indexer import InvertedIndex

'''
@func a crawler to traverse the site visiting urls
    extract and tokenise data 
@params base_url - the initial url to visit
@outputs scraped_data - text and data extracted from the url
'''
def build_crawler(base_url):
    #list of urls on the page to visit and those already visited
    visited_urls = set()
    urls_to_visit = [base_url]

    #initialise the indexer
    indexer = InvertedIndex()

    while urls_to_visit:
        #get next page and check if already visited
        current_url = urls_to_visit.pop(0)
        if current_url in visited_urls:
            continue

        print(f'Crawling page: {current_url}')

        try:
            #request the page and parse the html
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            visited_urls.add(current_url)

            #then add each page to the indexer
            page_text = soup.get_text(separator=' ', strip=True)
            indexer.add_document(current_url, page_text)

            '''!!! ADJUST LATER TO FOCUS QUOTES/AUTHORS !!!'''

            #find buttons with next text to scrape url
            '''!!! ADJUST LATER TO CHECK ALL BUTTONS !!!'''
            next_button = soup.find('li', class_='next')
            if next_button:
                next_link = next_button.find('a')['href']

                #add full url to queue
                full_next_url = urljoin(base_url, next_link)
                if full_next_url not in visited_urls:
                    urls_to_visit.append(full_next_url)

        except requests.exceptions.RequestException as e:
            print(f'Error crawling {current_url}: {e}')

        #politeness window of 6 seconds
        time.sleep(6)

    #save the index
    print("Finished Crawling - Saving Now")
    indexer.save()

    return "File Saved"

#initial execution
if __name__ == "__main__":
    start_url = 'https://quotes.toscrape.com/'
    build_crawler(start_url)
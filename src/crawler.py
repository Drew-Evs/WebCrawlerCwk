import requests 
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
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

            #want to crawl just the domain then find every <a> tag
            base_domain = urlparse(base_url).netloc
            all_links = soup.find_all('a')

            #go through all links with the href attribute
            for link in all_links:
                href = link.get('href')
                if not href:
                    continue

                #strip url fragments and ignore non web links e.g. email/javascript
                href = href.split('#')[0]
                if href.startswith('mailto:') or href.startswith('javascript:'):
                    continue

                #create full url and parse to ensure in same domain
                full_url = urljoin(current_url, href)
                link_domain = urlparse(full_url).netloc
                if link_domain != base_domain:
                    continue

                #queue url if not added yet
                if full_url not in visited_urls and full_url not in urls_to_visit:
                    urls_to_visit.append(full_url)

        except requests.exceptions.RequestException as e:
            print(f'Error crawling {current_url}: {e}')

        #politeness window of 6 seconds
        time.sleep(6)

    #save the index
    print("Finished Crawling - Saving Now")
    indexer.save()

    return indexer

#initial execution
if __name__ == "__main__":
    start_url = 'https://quotes.toscrape.com/'
    build_crawler(start_url)
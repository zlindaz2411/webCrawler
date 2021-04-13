from urllib.parse import urldefrag, urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import collections

class Crawler:

    def __init__(self, url):
        self.visited = set()
        self.urls_of_url = {}
        self.start_url = url 
        self.global_domain = urlparse(url).hostname
        self.crawl_queue = collections.deque()
        self.crawl_queue.append(url)


    def crawl(self, limit = 10):
        while(self.crawl_queue and limit > 0):
            url = self.crawl_queue.popleft()
            if(url in self.visited):
                continue
            urls = self.request(url)
            if(urls):
                for link in urls:
                    self.crawl_queue.append(link)
            limit -=1
        
        return self.visited

            
    def request(self, url):
        session = requests.session()
        try:
            response = session.get(url)
            if(response.status_code == 200):
                self.visited.add(url)
                soup = BeautifulSoup(response.text, 'html.parser') 
                # print(response.text)
                return self.extract_urls(url, soup)
                # return get_urls(url, domain, so)
            return None
        except(requests.exceptions):
            return None

    def extract_urls(self, url, soup):

        urls = []
        for a in soup.find_all('a'):
            link =  a.get('href')
            urls.append(link)

        #Convert relative links
        for i in range(len(urls)):
            urls[i] = urljoin(url, urls[i])

        #Crawling elements in the same domain
        urls = set(urls)
        print("Crawled website: " + url)
        print("Links in the crawled website: ")
        print(urls)
        print()
        self.urls_of_url[url] =urls
        filtered_urls = []
        for link in urls:
            if(self.is_same_domain(link)):
                filtered_urls.append(link)

        return filtered_urls


    def is_same_domain(self, url):
        new_domain = urlparse(url).hostname

        return new_domain == self.global_domain

 

if __name__ == "__main__":
    url = "https://monzo.com/"
    crawler = Crawler(url)
    limit = 100
    crawler.crawl(limit)

from urllib.parse import urldefrag, urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import queue
import threading

class Crawler(threading.Thread):

    def __init__(self, url, lock, visited, urls_of_url, crawl_queue, limit ):

        threading.Thread.__init__(self)
        
        self.visited = visited
        self.urls_of_url = urls_of_url
        self.start_url = url 
        self.global_domain = urlparse(url).hostname
        self.crawl_queue = crawl_queue
        self.lock = lock
        self.limit = limit
    
    def run(self):
        while(not self.crawl_queue.empty() and self.limit > 0):
            self.lock.acquire()
            url = self.crawl_queue.get()
            self.lock.release()

            if(url not in self.visited):
                self.visited.add(url)
                urls = self.request(url)
                if(urls):
                    for link in urls:
                        self.crawl_queue.put(link)
                self.limit -=1

            
    def request(self, url):
        session = requests.session()
        try:
            response = session.get(url)
            if(response.status_code == 200):
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

    limit = 1
    num_threads = 5
    threads = []
    visited = set()
    crawl_queue = queue.Queue() 
    crawl_queue.put(url)
    dic = {}
    # crawler.crawl(limit)
    for i in range(num_threads):
        crawler = Crawler(
            url, threading.Lock(), visited, dic, crawl_queue, limit)

        crawler.start()
        threads.append(crawler)

    for crawler in threads:
        crawler.join()

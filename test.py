import unittest
from crawler import Crawler
from bs4 import BeautifulSoup 
import requests

class Test(unittest.TestCase):
    crawler = None
    def setUpClass():
        Test.crawler = Crawler("https://monzo.com/")

    def test_crawl(self):
        self.assertEqual(Test.crawler.crawl(0), set())
        self.assertEqual(len(Test.crawler.crawl(10)), 10 )

    def test_request(self):
        self.assertEqual(Test.crawler.request("sdas"), None)
        self.assertIsNotNone(Test.crawler.request("https://monzo.com/"))

    
    def test_is_same_domain(self):
        self.assertTrue(Test.crawler.is_same_domain("https://monzo.com/ds/dsa/sd"))
        self.assertFalse(Test.crawler.is_same_domain("https://community.monzo.com/ds/dsa/sd"))
        self.assertFalse(Test.crawler.is_same_domain(""))

if __name__ == '__main__':
    unittest.main()
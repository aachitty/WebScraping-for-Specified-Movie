from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  
from urllib.parse import urlparse
import requests

class MovieSpider(CrawlSpider):
    name = 'updated_movie_spider'
    
    allowed_domains = []
    start_urls = []
    matched_domains = set()
    
    rules = (
        Rule(LinkExtractor(allow=('/movie'), deny=('play.google', 'hulu.com', 'primevideo', 'netflix', 'youtube', 'disney', 'hotstar', 'manorama', 'hbo', 'max')), follow=True, callback='parse_item'),
    )
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.offsite.OffsiteMiddleware': None,
        },
    }

    def __init__(self, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        # Setup Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        google_api_key = 'AIzaSyCNVntztAynON4mpCBFFflBSPkmUq7_1Zo'
        cse_id = 'b187b3d32ac74425e'
        query = 'Paradise movie watch online free site:.to OR site:.ru OR site:.xyz OR site:.go OR site:.me OR site:.cam OR site:.sh OR site:.llc'
        self.start_urls = self.get_urls_from_google(google_api_key, cse_id, query)
        self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]
        
    def get_urls_from_google(self, api_key, cse_id, query):
        search_url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}"
        response = requests.get(search_url)
        search_results = response.json()
        urls = [item['link'] for item in search_results.get('items', [])]
        return urls

    def parse_item(self, response):
        domain = urlparse(response.url).netloc
        
        # Skip if this domain has already matched content
        if domain in self.matched_domains:
            return
        
        self.driver.get(response.url)
        html = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=html, encoding='utf-8')
        
        movie_title = "Paradise"  
        movie_synopsis = "An Indian tourist couple arrive in the hill country of crisis ridden Sri Lanka to celebrate their 5th wedding anniversary. But, when things take an unexpected turn, conflicts deepen revealing cracks in their relationship."

        # Extract title and synopsis from potential tags
        title_element = response.css('meta[property="og:title"]::attr(content)').get().lower() or ''
        synopsis_element = response.css('meta[property="og:description"]::attr(content)').get().lower() or ''
        
        # Check if the movie title and synopsis match
        title_match = movie_title.lower() in title_element
        synopsis_match = movie_synopsis.lower() in synopsis_element

        if title_match or synopsis_match:
            output = f"Found {movie_title} in {response.url}\n"
            with open('updated_movies_found.txt', 'a') as f:
                f.write(output)
            
            # Add domain to matched_domains set to prevent further requests
            self.matched_domains.add(domain)
            
            yield {
                'url': response.url,
                'title': title_element,
                'synopsis': synopsis_element,
                'verification': 'Title or synopsis found',
            }


    def close(self, reason):
        # Close Selenium WebDriver
        self.driver.quit()

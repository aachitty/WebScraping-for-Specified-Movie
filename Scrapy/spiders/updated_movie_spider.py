from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  

class MovieSpider(CrawlSpider):
    name = 'updated_movie_spider'
    
    allowed_domains = ['0gomovies.cam']
    start_urls = ['https://0gomovies.cam/movie/filter/movies/latest/all/all/all/all/']
    
    rules = (
        Rule(LinkExtractor(allow=('/movie/')), follow=True, callback='parse_item'),
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

    def parse_item(self, response):
        self.driver.get(response.url)
        html = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=html, encoding='utf-8')

        movie_title = "Paradise"  
        movie_synopsis = "An Indian tourist couple arrive in the hill country of crisis ridden Sri Lanka to celebrate their 5th wedding anniversary. But, when things take an unexpected turn, conflicts deepen revealing cracks in their relationship."

        # Extract all text from the response
        page_text = response.text.lower()

        # Check if the movie title, synopsis, or "Paradise" is in the text or URL
        title_match = movie_title.lower() in page_text
        synopsis_match = movie_synopsis.lower() in page_text
        url_match = 'paradise' in response.url.lower()

        # Log results based on conditions
        if title_match or synopsis_match or url_match:
            output = f"Found match on {response.url}\n"
            with open('updated_movies_found.txt', 'a') as f:
                f.write(output)
            yield {
                'url': response.url,
                'title_match': title_match,
                'synopsis_match': synopsis_match,
                'url_match': url_match,
                'verification': 'Title, synopsis, or URL contains "Paradise"',
            }
        else:
            yield {
                'url': response.url,
                'title_match': title_match,
                'synopsis_match': synopsis_match,
                'url_match': url_match,
                'verification': 'No match found',
            }

    def close(self, reason):
        # Close Selenium WebDriver
        self.driver.quit()

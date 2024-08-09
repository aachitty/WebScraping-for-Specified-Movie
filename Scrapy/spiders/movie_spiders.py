from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

domains = ['https://0gomovies.movie/']
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MovieSpider(CrawlSpider):
    name = 'movie_spider'
    
    # List of websites to scrape
    allowed_domains = ['https://0gomovies.movie/']
    start_urls = ['https://0gomovies.movie/']

    rules = (
        Rule(LinkExtractor(allow=(), deny=()), follow=True, callback='parse_item'),
    )
    
    custom_settings = {
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.offsite.OffsiteMiddleware': None,
    }
}

    def parse_item(self, response):
        movie_title = "Paradise"  # Movie to search for
        
        # Extract the title from the webpage and search for the movie
        if movie_title.lower() in response.text.lower():
            output = f"Found {movie_title} in {response.url}\n"
            with open('movies_found.txt', 'a') as f:
                f.write(output)
            yield {
                'url': response.url,
                'title': movie_title,
            }
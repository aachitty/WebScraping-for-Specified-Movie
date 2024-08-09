from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

class MovieSpider(CrawlSpider):
    name = 'updated_movie_spider'
    
    allowed_domains = ['0gomovies.cam']
    start_urls = ['https://0gomovies.cam/movies']
    
    rules = (
        Rule(LinkExtractor(allow=()), follow=True, callback='parse_item'),
    )
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.offsite.OffsiteMiddleware': None,
        },
        
    }

def parse_item(self, response):
        self = Selector(response)
        movie_title = "Paradise"  # Movie to search for
        movie_synopsis = "An Indian tourist couple arrive in the hill country of crisis ridden Sri Lanka to celebrate their 5th wedding anniversary. But, when things take an unexpected turn, conflicts deepen revealing cracks in their relationship."
        
        # Check if the URL is in the /movie section
        if '/movie/' in response.url:
            title_elements = self.xpath('//h1/text() | //h2/text() | //p/text()').extract()  # Search in h1, h2, and p elements
            
            for title in title_elements:
                # Check if the extracted title contains the movie title and synopsis
                if movie_title.lower() in title.lower() and movie_synopsis.lower() in title.lower():
                    
                    output = f"Found {movie_title} in {response.url}\n"
                    with open('updated_movies_found.txt', 'a') as f:
                        f.write(output)
                    yield {
                        'url': response.url,
                        'title': title,
                    }
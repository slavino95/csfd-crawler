import scrapy

class CsfdSpider(scrapy.Spider):
    name = 'csfd'

    start_urls = ['https://www.csfd.cz/filmy-online/']

    def parse(self, response):
    	for movie in response.css('div.name a::attr(href)'):
    		yield response.follow(movie, self.parse_movie)

    	for href in response.css('a.next::attr(href)'):
            yield response.follow(href, self.parse)	

    def parse_movie(self, response):
    	def extract_with_css(query):
            return response.css(query).extract_first().strip()
            
    	yield {
			'movie': extract_with_css('h1::text'),
			'genre': extract_with_css('p.genre::text'),
			'origin': extract_with_css('p.origin::text'),
			'year': extract_with_css('span[itemprop="dateCreated"]::text'),	
			'length': response.css('p.origin::text').extract()[1],
            'rating': extract_rating('h2.average::text'),
    	}

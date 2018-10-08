import scrapy
from csfd.items import CsfdItem

class CsfdSpider(scrapy.Spider):
    name = 'csfd'

    # start_urls = ['http://www.csfd.cz/filmy-online/']
    start_urls = ['https://www.csfd.cz/zebricky/nejlepsi-filmy/?show=complete']

    def parse(self, response):

        for top_movie in response.css('td.film a::attr(href)'):
            yield response.follow(top_movie, self.parse_movie)

        for common in response.css('a.c1::attr(href)'):
            yield response.follow(common, self.parse_movie)

    def parse_movie(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        movie = CsfdItem()
        movie['movie'] = extract_with_css('h1::text')
        movie['genre'] = response.css('p.genre::text').extract_first().split(' / ')
        movie['origin'] = response.css('p.origin::text').extract_first().split(',')[0].split(' / ')
        movie['year'] = extract_with_css('span[itemprop="dateCreated"]::text')
        movie['length'] = response.css('p.origin::text').extract()[1].split(' ')[1]
        movie['rating'] = extract_with_css('h2.average::text').split('%')[0]
        movie['director'] = extract_with_css('span[itemprop="director"] a::text')

        yield movie

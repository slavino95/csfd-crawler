import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from csfd.items import CsfdItem


class CsfdSpider(CrawlSpider):
    name = 'csfd'

    #start_urls = ['http://www.csfd.cz/filmy-online/']

    start_urls = ['https://www.csfd.cz/zebricky/nejlepsi-filmy/?show=complete',
                  'https://www.csfd.cz/zebricky/nejoblibenejsi-filmy/?show=complete',
                  'https://www.csfd.cz/zebricky/nejrozporuplnejsi-filmy/?show=complete',
                  'https://www.csfd.cz/zebricky/nejhorsi-filmy/?show=complete',
                  'http://www.csfd.cz/filmy-online/']

    allowed_domains = ['csfd.cz']
    rules = (
        Rule(LinkExtractor(allow=r'/film/([^/]+)/$',), callback='parse_movie', follow=True),
        Rule(LinkExtractor(allow=r'/filmy-online/([^/]+)/$',), callback='parse_page', follow=True),
    )

    def parse_page(self, response):

        for href in response.css('a.next::attr(href)').extract():
            yield response.follow(href, self.parse)

        """for top_movie in response.css('td.film a::attr(href)'):
            yield response.follow(top_movie, self.parse_movie)

        for common in response.css('a.c1::attr(href)'):
            yield response.follow(common, self.parse_movie)
        """

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
        movie['image'] = extract_with_css('img.film-poster::attr(src)')
        movie['tags'] = response.css('div.tags a::text').extract()
        movie['plot'] = response.xpath('//*[@id="plots"]/div[2]/ul/li[1]/div[1]/text()[2]').extract_first().strip()
        movie['actors'] = response.xpath('//*[@class="creators"]/div[6]/span[1]/a/text()').extract()[:5]

        """
        Actors div doesn't have class or id and it's position may vary.
        Extracting only first five actors from list.
        """
        if not movie['actors']:
            movie['actors'] = response.xpath('//*[@class="creators"]/div[5]/span[1]/a/text()').extract()[:5]
            if not movie['actors']:
                movie['actors'] = response.xpath('//*[@class="creators"]/div[4]/span[1]/a/text()').extract()[:5]

        yield movie

import scrapy
from Scraper.quotes_scraper.items import AuthorItem


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        authors = {}
        for quote in response.css('div.quote'):
            author = quote.css('span small::text').get()
            if author not in authors:
                authors[author] = True
                yield scrapy.Request(url=f"http://quotes.toscrape.com/author/{author}/",
                                     callback=self.parse_author)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author = AuthorItem()
        author['name'] = response.css('h3.author-title::text').get()
        author['born_date'] = response.css('span.author-born-date::text').get()
        author['born_location'] = response.css('span.author-born-location::text').get()
        author['description'] = response.css('div.author-description::text').get()
        yield author

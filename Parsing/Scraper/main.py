from scrapy.crawler import CrawlerProcess
from quotes_scraper.spiders.quotes_spider import QuotesSpider
from quotes_scraper.spiders.authors_spider import AuthorsSpider


def run_crawlers():
    process_authors = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json'
    })
    process_quotes = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json'
    })
    process_authors.crawl(AuthorsSpider)
    process_quotes.crawl(QuotesSpider)

    process_authors.start()
    process_quotes.start()


if __name__ == '__main__':
    run_crawlers()

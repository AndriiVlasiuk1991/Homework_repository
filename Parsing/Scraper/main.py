from scrapy.crawler import CrawlerProcess
from quotes_scraper.spiders.quotes_spider import QuotesSpider
from quotes_scraper.spiders.authors_spider import AuthorsSpider


def run_crawlers():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json'
    })
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()


if __name__ == '__main__':
    run_crawlers()

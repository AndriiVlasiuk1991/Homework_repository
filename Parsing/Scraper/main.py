from scrapy.crawler import CrawlerProcess
from quotes_scraper.spiders.quotes_spider import QuotesSpider
from quotes_scraper.spiders.authors_spider import AuthorsSpider


# Запуск краулера для цитат
def run_quotes_crawler():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json'
    })
    process.crawl(QuotesSpider)
    process.start()


# Запуск краулера для авторів
def run_authors_crawler():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json'
    })
    process.crawl(AuthorsSpider)
    process.start()


if __name__ == '__main__':
    run_quotes_crawler()
    run_authors_crawler()

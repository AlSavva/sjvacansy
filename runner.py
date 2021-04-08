from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from sjvacancy import settings
from sjvacancy.spiders.SJvacancy import SjvacancySpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(SjvacancySpider)

    process.start()
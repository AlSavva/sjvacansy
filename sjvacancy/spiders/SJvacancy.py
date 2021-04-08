import scrapy
from scrapy.http import HtmlResponse
from sjvacancy.items import SjvacancyItem
from scrapy.loader import ItemLoader
from datetime import datetime


class SjvacancySpider(scrapy.Spider):
    name = 'SJvacancy'
    allowed_domains = ['superjob.ru']
    start_urls = []
    config = {
        'keywords': [
            "стажер", "ученик", "junior", "intern", "trainee", "интерн ",
            "начинающий", "младший", "студент",
            "ассистент", "стажир", "практика"]
    }

    to_model = True  # если False -возвращается стандартный item scrapy

    def __init__(self):
        super(SjvacancySpider, self).__init__()
        self.keywords = self.config.get('keywords')
        for word in self.keywords:
            self.start_urls.append(
                f'https://www.superjob.ru/vacancy/search/?keywords={word}&geo%5Bt%5D%5B0%5D=13&geo%5Bt%5D%5B1%5D=73&geo%5Bt%5D%5B2%5D=12&geo%5Bt%5D%5B3%5D=55&geo%5Bt%5D%5B4%5D=146&geo%5Bt%5D%5B5%5D=25&geo%5Bt%5D%5B6%5D=33')

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            '//span[contains(@class, "f-test-text-company-item-salary")]/..//a/@href')
        temp_selector_list = response.xpath(
            '//span[contains(@class, "f-test-text-company-item-salary")]/..//a')
        vacancy_name = [''.join(x.xpath(".//text()").extract()) for x in
                        temp_selector_list]
        # отфильтровываем выкансии с ключевыми словами в названии
        if links:
            for link, name in zip(links, vacancy_name):
                for keyword in self.keywords:
                    if keyword in name.lower():
                        yield response.follow(link, callback=self.parse_page,
                                              cb_kwargs={'position': name})
                        break
        next_page = response.css(
            'a.f-test-button-dalshe::attr("href")').extract_first()
        if next_page:
            yield response.follow(next_page,
                                  callback=self.parse)

    def parse_page(self, response: HtmlResponse, position):
        loader = ItemLoader(item=SjvacancyItem(), response=response)
        loader.add_value('position', position)
        loader.add_xpath('summary_1',
                         '//div[contains(@class, "UGN79")]//script//text()')
        loader.add_xpath('summary_2',
                         '//div[contains(@class, "UGN79")]/preceding-sibling::div/script//text()')
        loader.add_xpath('summary_3',
                         '//div[contains(@class, "f-test-vacancy-base-info")]//span[contains(@class, "f-test-badge")]//text()')
        loader.add_xpath('summary_4',
                         '//div[contains(@class, "f-test-address")]/following-sibling::div//text()')
        loader.add_xpath('salary',
                         '//div[contains(@class, "UGN79")]//span[contains(@class, "PlM3e")]//text()')
        loader.add_value('source', 'superjob')
        loader.add_value('country', 'Россия')
        loader.add_value('date', datetime.now(tz=None))
        loader.add_value('link', response.url)
        loader.add_value('id', response.url)

        yield loader.load_item()

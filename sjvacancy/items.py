# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

# извлекаем ID вакансии из ссылки
def process_id(value):
    value = value.replace('.', '-').split('-')
    return value[-2]


class SjvacancyItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field(output_processor=TakeFirst(),
                      input_processor=MapCompose(process_id))
    source = scrapy.Field(output_processor=TakeFirst())
    tag = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field(output_processor=TakeFirst())
    company = scrapy.Field()
    remote = scrapy.Field()
    relocate = scrapy.Field()
    parttime = scrapy.Field()
    inhouse = scrapy.Field()
    modified = scrapy.Field()
    date = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    position = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field()
    specialization = scrapy.Field()
    no_experience = scrapy.Field()
    no_cv = scrapy.Field()
    summary_1 = scrapy.Field(output_processor=TakeFirst())
    summary_2 = scrapy.Field(output_processor=TakeFirst())
    summary_3 = scrapy.Field(output_processor=TakeFirst())
    summary_4 = scrapy.Field()

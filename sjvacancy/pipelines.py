# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json


class JobModel(BaseModel):
    id: str = None
    source: str = None  #
    tag: str = None  #
    city: str = None
    country: str = None
    company: str = None  #
    remote: Optional[bool] = None
    relocate: Optional[bool] = None
    parttime: Optional[bool] = None
    inhouse: Optional[bool] = None
    modified: datetime = None  #
    date: datetime = None  #
    link: str = None  #
    position: str = None  #
    salary: Optional[str] = None
    specialization: str = None  #
    no_experience: Optional[bool] = None
    no_cv: Optional[bool] = None


class SjvacancyPipeline:
    tags = {'IT, Интернет, связь, телеком': 'it',
            'Кадры, управление персоналом': 'hr',
            'Маркетинг, реклама, PR': 'marketing',
            'Дизайн': 'design',
            'Бухгалтерия, финансы, аудит': 'economics',
            'Банки, инвестиции, лизинг': 'economics',
            'Юриспруденция': 'jurisprudence'
            }
    jobmodel = JobModel()

    def process_item(self, item, spider):
        item['id'] = item['id']
        item['source'] = item['source']
        summary_2 = json.loads(item['summary_2'])
        summary_1 = json.loads(item['summary_1'])
        item['tag'], item['specialization'] = self.process_tags(summary_2)
        item['salary'] = self.process_salary(item['salary'])
        try:
            item['summary_3'] = item['summary_3']
        except:
            item['summary_3'] = []
        try:
            item['no_experience'], item['no_cv'], item['remote'], item[
                'relocate'], item['parttime'], item[
                'inhouse'] = self.process_flags(
                summary_3=item['summary_3'], summary_4=item['summary_4'],
                parttime=summary_1.get('employmentType'))
        except:
            item['no_experience'], item['no_cv'], item['remote'], item[
                'relocate'], item['parttime'], item[
                'inhouse'] = self.process_flags(summary_3=item['summary_3'],
                                                summary_4=item['summary_4']
                                                )
        item['city'], item['company'] = self.process_employer(summary_1)
        item['modified'] = self.process_date(summary_1.get("datePosted"))
        del item['summary_1']
        del item['summary_2']
        del item['summary_3']
        del item['summary_4']
        if spider.to_model:
            item = self.process_model(item)

        return item

    def process_tags(self, summary_2):
        specialization = summary_2.get('itemListElement')[2].get('item').get(
            'name')
        tag = self.tags.get(specialization, '')
        return tag, specialization

    def process_salary(self, salary):
        if 'По договорённости' in salary:
            return 'По договорённости'
        while '\xa0' in salary:
            salary.remove('\xa0')
        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u' ')
        return ' '.join(salary[i] for i in range(len(salary)))

    def process_flags(self, **kwargs):
        flags_dict = {'no_experience': None, 'no_cv': None, 'remote': None,
                      'relocate': None, 'parttime': None,
                      'inhouse': True}
        no_experience = None
        no_cv = None
        remote = None
        relocate = None
        parttime = None
        inhouse = True

        if kwargs['parttime']:
            parttime = True if kwargs.get('parttime') == 'PART_TIME' else None
        else:
            for word in kwargs.get('summary_4'):
                if 'неполн' in word.lower():
                    parttime = True
                    break
        flags_dict.update({'parttime': parttime})
        if kwargs.get('summary_3'):
            if 'Отклик без резюме' in kwargs.get('summary_3'):
                no_cv = True
            if 'Опыт не нужен' in kwargs.get('summary_3'):
                no_experience = True
            if 'Удаленная работа' in kwargs.get('summary_3'):
                remote = True
                inhouse = None
            if 'Вахта' in kwargs.get('summary_3'):
                relocate = True
        flags_dict.update(
            {'no_experience': no_experience, 'no_cv': no_cv, 'remote': remote,
             'relocate': relocate, 'parttime': parttime, 'inhouse': inhouse})
        return flags_dict.get('no_experience'), flags_dict.get(
            'no_cv'), flags_dict.get('remote'), flags_dict.get(
            'relocate'), flags_dict.get('parttime'), flags_dict.get('inhouse')

    def process_employer(self, summary):
        city = summary.get('jobLocation').get('address').get('addressLocality')
        company = summary.get('hiringOrganization').get('name')
        return city, company

    def process_date(self, created_at):
        created_at = created_at.replace('T', ' ')[:-6]
        return datetime.strptime(created_at,
                                 '%Y-%m-%d %H:%M:%S')

    def process_model(self, item):
        item = self.jobmodel.parse_obj(item)
        return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if not spider.to_model:
            line = json.dumps(ItemAdapter(item).asdict())
        else:
            line = item.json()
        self.file.write(line + '\n')
        return item

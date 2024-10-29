# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitmentCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # Ten cong viec
    job_title = scrapy.Field()
    # Mo ta cong viec
    job_description = scrapy.Field()
    # Luong
    job_salary = scrapy.Field()
    # Dia diem lam viec
    job_location = scrapy.Field()
    # Level dau vao(intern, fresher,...)
    job_yoe = scrapy.Field()
    # Lich lam viec
    job_schedule = scrapy.Field()
    # Link dan den trang web
    job_link = scrapy.Field()
    # Ten cong ty tuyen dung
    job_company = scrapy.Field()
    # Ngay het han tuyen dung
    job_expire_date = scrapy.Field()


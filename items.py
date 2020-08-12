# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 自定义一个类名wangye_mysql
class wangye(scrapy.Item):
    # define the fields for your item here like:
    # 构造（创建）
    title = scrapy.Field()
    detail = scrapy.Field()
    url = scrapy.Field()
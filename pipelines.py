# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
# 导入json模块
import json

class WangyiPipeline(object):
    # 初始化函数，创建json文件，指定编码格式
    def __init__(self):
        self.filename = codecs.open('wangyinews.json', 'w', encoding='utf-8')

    # 将item写入，在结尾增加换行符
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filename.write(content)
        # 解析一个存一个，返回item继续跟进
        return item

    # 爬问后就把文件关了，释放资源
    def spider_close(self, spider):
        self.filename.close()
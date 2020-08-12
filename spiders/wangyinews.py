# -*- coding: utf-8 -*-
import scrapy,re
from wangyi.biaotou import biaotou       #导入自定义UserAgent包
from wangyi.items import wangye


class WangyinewsSpider(scrapy.Spider):
    name = 'wangyinews'
    allowed_domains = ['news.163.com']

    # 初始化
    def start_requests(self):

        # 输入页数
        ye=int(input('请输入页数：'))

        # 循环页数
        for i in range(1,ye+1):

            if i == 1:

                url='http://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback'

            else:

                if i <10:

                    i='0'+str(i)

                url='http://temp.163.com/special/00804KVA/cm_guonei_{}.js?callback=data_callback'.format(i)

            # 添加报头
            header={
                "User-Agent":biaotou(),
            }

            # 用get发送请求
            req=scrapy.Request(url=url,callback=self.nextyemian,headers=header)

            # 将循环的请求全部存到yield里并且发送下一个函数
            yield  req

    # 将返回的信息遍历出内容页的地址url
    def nextyemian(self,response):
        # 定义一个列表存放items
        items = []
        # response是返回值，进行用GBK转码，请注意如果查看他的编码时是发现它是cp1252的编码格式
        html = response.body.decode('GBK')

        # 返回的格式：'data_callback([{.....}])'我们需要把它的字母干掉，只剩元组'([{.......}])'
        req = html.replace("data_callback", "")

        # 将它的字符串干掉
        req = eval(req)

        # 添加报头
        header = {
            "User-Agent": biaotou(),
        }
        # 把处理完的进行循环遍历
        for i in req:
            item = wangye()
            # 拿出需要的url路径
            item['url'] = i['docurl']
            items.append(item)

        for item in items:
            # 发送一个get请求
            yield scrapy.Request(url=item['url'],meta={'meta': item}, callback=self.parse_details,headers=header)


    def parse_details(self,response):

        # 先获取parse函数解析的结果
        item = response.meta['meta']
        # 使用xpath匹配出标题
        item['title'] = response.xpath('//*[@id="epContentLeft"]/h1/text()').extract_first()
        # 使用xpath匹配到内容
        item['detail'] = response.xpath('//*[@id="endText"]/p/text()').extract()

        # 将实例化发送到pipelines.py
        yield item


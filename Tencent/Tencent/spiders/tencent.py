# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    # start_urls = ['http://hr.tencent.com/position.php?&start=0#a']
    base_url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [base_url + str(offset)]



    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for each in node_list:
            item = TencentItem()
            # 提取每个职位的信息，并将每个字段编码为utf-8
            item['name'] = each.xpath('./td[1]/a/text()').extract()[0].encode("utf-8")  # 此为unicode编码  extract()将对象转为字符串
            item['detailLink'] = each.xpath('./td[1]/a/@href').extract()[0].encode("utf-8")

            if len(each.xpath('./td[2]/text()')):
                item['positionInfo'] = each.xpath('./td[2]/text()').extract()[0].encode("utf-8")
            else:
                item['positionInfo'] = ""

            item['peopleNumber'] = each.xpath('./td[3]/text()').extract()[0].encode("utf-8")
            item['workLocation'] = each.xpath('./td[4]/text()').extract()[0].encode("utf-8")
            item['publishTime'] = each.xpath('./td[5]/text()').extract()[0].encode("utf-8")

            yield item
        if self.offset<2190:
            self.offset += 10
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url,callback = self.parse)
        # pass

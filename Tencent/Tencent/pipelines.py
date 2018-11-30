# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# 编码类
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)


class TencentPipeline(object):
    def __init__(self):
        self.f = open("tencent.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),cls=MyEncoder,ensure_ascii = False) + ",\n"

        self.f.write(content)
        return item

    def close_spider(self,spider):
        self.f.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from datetime import datetime
from itemadapter import ItemAdapter


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        today = datetime.today().strftime("%Y%m%d")
        self.file = open(f"data/{today}.jl", "w", encoding="utf8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

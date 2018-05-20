# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql





class DangdangPipeline(object):
    def process_item(self, item, spider):
        # ========================================================================================
        # Mysql connect
        conn = pymysql.connect(host="",
                               user="root",
                               password="",
                               db="dangdang",
                               charset="utf8")
        cur = conn.cursor()
        # ========================================================================================
        for i in range(len(item['title'])):
            title = item["title"][i]
            Comment_Num = item["Comment_Num"][i][:-3]
            price = item["price"][i][1:]
            link = item["link"][i]
            sql = "INSERT INTO books(title,link,comment_num,price) VALUES ('"+title+"','"+link+"','"+Comment_Num+"','"+price+"')"
            sta = cur.execute(sql)
            conn.commit()
        cur.close()
        conn.close()
        return item

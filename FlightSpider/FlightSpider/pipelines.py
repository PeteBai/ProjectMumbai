# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import uuid

class FlightspiderPipeline:

    def __init__(self):
        self.db = pymysql.connect(
        # self.db = pymysql.connect(
        #     host='localhost',  # IP，MySQL数据库服务器IP地址
        #     port=3306,  # 端口，默认3306，可以不输入
        #     user='root',  # 数据库用户名
        #     password='123',  # 数据库登录密码
        #     database='flightdata',  # 要连接的数据库
        #     charset='utf8')  # 字符集，注意不是'utf-8')
        self.insertPattern = '''
        insert into flightrawdata 
        (rec_uuid,flight_dt,qry_dt,line,dep_tm,dep_ap,dep_ct,arr_tm,arr_ap,arr_ct,plane_type,price,discount) 
        values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",{},"{}");
        '''
        self.cursor = self.db.cursor()

    def open_spider(self, spider):
        spider.logger.warn("开启数据库连接")

    def close_spider(self, spider):
        spider.logger.warn("关闭数据库连接")
        self.db.close()

    def process_item(self, item, spider):
        # print(item)
        spider.logger.warn("[写数据库] {} | {}->{}".format(item['qry_dt'],item['dep_ap'],item['arr_ap']))
        query = self.insertPattern.format(uuid.uuid4(),item['flight_dt'],item['qry_dt'],item['line'],item['dep_tm'],item['dep_ap'],item['dep_ct'],item['arr_tm'],item['arr_ap'],item['arr_ct'],item['plane_type'],item['price'],item['discount'])
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as e:
            spider.logger.error(e)
            print(e)
        return item

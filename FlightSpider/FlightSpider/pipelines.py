# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class FlightspiderPipeline:

    def __init__(self):
        self.db = pymysql.connect(
        host = '106.54.70.122',  # IP，MySQL数据库服务器IP地址
        port = 3306,  # 端口，默认3306，可以不输入
        user = 'Xyl',  # 数据库用户名
        password = '3.14159zsyzl',  # 数据库登录密码
        database = 'flight',  # 要连接的数据库
        charset = 'utf8')  # 字符集，注意不是'utf-8')
        self.insertPattern = '''
        insert into flightrawdata 
        (qry_dt,line,dep_tm,dep_ap,arr_tm,arr_ap,type,price,discount) 
        values("{}","{}","{}","{}","{}","{}","{}","{}","{}");
        '''
        self.cursor = self.db.cursor()

    def open_spider(self, spider):
        spider.logger.info("开启数据库连接")

    def close_spider(self, spider):
        spider.logger.info("关闭数据库连接")
        self.db.close()

    def process_item(self, item, spider):
        # print(item)
        query = self.insertPattern.format(item['qry_dt'],item['line'],item['dep_tm'],item['dep_ap'],item['arr_tm'],item['arr_ap'],item['plane_type'],item['price'],item['discount'])
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as e:
            spider.logger.info(e)
        spider.logger.info("写入数据库")
        return item

# -*- coding: utf-8 -*-
import scrapy
from ..items import FlightspiderItem
import json
import datetime
import time
from .City import city

class FlispiderSpider(scrapy.Spider):
    name = 'FliSpider'
    url = 'https://www.lsjpjg.com/getthis.php'
    cities = ["重庆","厦门"]
    startDate = "2020-03-13"
    length = 30
    delta = datetime.timedelta(days=1)

    def start_requests(self):
        c = city()
        arrvCities = c.getAllName()
        date = datetime.datetime.strptime(self.startDate, '%Y-%m-%d').date()
        for i in range(self.length):
            for dept in self.cities:
                for arrv in arrvCities:
                    if dept != arrv:
                        formData = {
                            'dep_ct': dept,
                            'arr_ct': arrv,
                            'dep_dt': str(date)
                        }
                        time.sleep(30)
                        date = date + self.delta
                        yield scrapy.FormRequest(self.url, method="POST", formdata=formData, callback=self.Process)
                        self.logger.info("开始下一次请求")

    def Process(self, response):
        res = json.loads(response.body)
        self.logger.info(res)
        if len(res) == 0:
            self.logger.warn("请求数据为空")
        else:
            for flightInfo in res:
                if flightInfo['line'] == 'noflight':
                    continue
                item = FlightspiderItem()
                item['qry_dt'] = flightInfo["qry_dt"]
                item['line'] = flightInfo["line"]
                item['dep_tm'] = flightInfo["dep_tm"]
                item['dep_ap'] = flightInfo["dep_ap"]
                item['arr_tm'] = flightInfo["arr_tm"]
                item['arr_ap'] = flightInfo["arr_ap"]
                item['plane_type'] = flightInfo["type"]
                item['price'] = flightInfo["price"]
                item['discount'] = flightInfo["discount"]
                yield item

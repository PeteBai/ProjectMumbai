# -*- coding: utf-8 -*-
from urllib.parse import parse_qs
import scrapy
from ..items import FlightspiderItem
import json
import datetime
import time
from .City import city


class FlispiderSpider(scrapy.Spider):
    name = 'FliSpider'
    url = 'https://www.lsjpjg.com/getthis.php'
    cities = ["西安","厦门","西宁","银川","扬州","郑州","珠海"]
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
                        yield scrapy.FormRequest(self.url, method="POST", formdata=formData, callback=self.Process)
                        self.logger.warn("请求[{}] {}->{}".format(date,dept,arrv))
            date = date + self.delta

    def Process(self, response):
        _query = parse_qs(response.request.body.decode('utf-8'),encoding='utf-8')
        res = json.loads(response.body)
        self.logger.warn(res)
        if len(res) == 0:
            self.logger.warn("请求数据为空")
        else:
            for flightInfo in res:
                if flightInfo['line'] == 'noflight':
                    self.logger.warn("没有航线")
                    continue
                item = FlightspiderItem()
                item['flight_dt'] = _query['dep_dt'][0]
                item['qry_dt'] = flightInfo["qry_dt"]
                item['line'] = flightInfo["line"]
                item['dep_tm'] = flightInfo["dep_tm"]
                item['dep_ap'] = flightInfo["dep_ap"]
                item['dep_ct'] = _query['dep_ct'][0]
                item['arr_tm'] = flightInfo["arr_tm"]
                item['arr_ap'] = flightInfo["arr_ap"]
                item['arr_ct'] = _query['arr_ct'][0]
                item['plane_type'] = flightInfo["type"]
                item['price'] = flightInfo["price"]
                item['discount'] = flightInfo["discount"]
                yield item

# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/26
# @version 1.0
# @desc: Get histroy data from tencent server.

import sys
from datetime import datetime

from stock.common.price import Price, PriceList
from stock.common.stock import Stock

from stock.web.base.web_base import WebSource

class WebSourceTencentHistory(WebSource):
    """ Get stock history data from tencent server.
    
        To get data several years ago from now.
    
    Attributes:
        years_from_now: the years count ago from now
    """
    def __init__(self, years_from_now):
        super(WebSourceTencentHistory, self).__init__()
        if not isinstance(years_from_now, int):
            raise ValueError("%s : the years_from_now must be an int type data!"%(self.__class__.__name__))
        if years_from_now < 0:
            raise ValueError("%s : the years_from_now must be greater or equal to 0!"%(self.__class__.__name__))
        self.years_from_now = years_from_now
        self.years = []
        year_now = datetime.today().year
        for i in range(-years_from_now, 1):
            self.years.append(year_now + i)
        self.is_history = True
    
    def get_years(self):
        return self.years

    def get_stock_url(self, stock, year):
        if not isinstance(stock, Stock):
            raise ValueError("function %s: the input parameter 'stock' must be a Stock object!"%(sys._getframe().f_code.co_name))
        url = "http://data.gtimg.cn/flashdata/hushen/"
        str_year = str(year)
        if len(str_year) == 4:
            str_year = str_year[2:]
        url =  url + "daily/" + str_year + "/" + stock.code +".js?visitDstTime=1"
        return url
    
    def append_data(self, stock, text):
        super(WebSourceTencentHistory, self).append_data(stock, text)

        if not text.startswith( "daily_data_"):
            print("function %s: the 'text': %s from web does not start with 'daily_data_' !"%(sys._getframe().f_code.co_name, stock.code))
            return
        
        src_data = text.split("\n")[1:]
        src_data.pop()
        pl = []
        for i in range(len(src_data)):
            src_data[i] = src_data[i].rstrip(src_data[i][-3:])
            one_row = src_data[i].split(" ")
            time = one_row[0]
            
            if int(time[0:2]) > int(str(datetime.today().year)[2:]):
                time = str(int(str(datetime.today().year)[0:2]) - 1) +time
            else:
                time = str(int(str(datetime.today().year)[0:2])) + time
            price_value = float(one_row[2])
            pr = Price(price_value, datetime.strptime(time, "%Y%m%d"))
            pr.open = float(one_row[1])
            pr.high = float(one_row[3])
            pr.low = float(one_row[4])
            pr.volumn = float(one_row[5])
            pl.append(pr)

        if hasattr(stock, 'history_prices'):
            for ele in pl:
                stock.history_prices.append(ele)
        else:
            stock.history_prices = PriceList(pl)
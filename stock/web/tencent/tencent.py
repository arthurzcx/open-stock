# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/26
# @version 1.0
# @desc: Web data source tencent.

import sys
import datetime

from stock.common.stock import Stock
from stock.common.price import Price
from stock.web.base.web_base import WebSource

class WebSourceTencent(WebSource):
    """ The class implements pull data from tencent url.

    Attributes can refter to the base class: WebSource.            
    """
    def __init__(self):
        super(WebSourceTencent, self).__init__()
        self.base_url = "http://qt.gtimg.cn/q="

    def get_stock_url(self, stock):
        if not isinstance(stock, Stock):
            raise ValueError("function %s: the input parameter 'stock' must be a Stock object!"%(sys._getframe().f_code.co_name))
        return super(WebSourceTencent, self).get_stock_url( stock)
        
    def append_data(self, stock, text):
        # Use super class interface to check if the input parameters valid
        super(WebSourceTencent, self).append_data(stock, text)

        data_list = str(text).split("~")
        data_len = len(data_list)
        
        if data_len < 47:
            raise ValueError("function %s: the response 'text' doesn't have enough data!"%(sys._getframe().f_code.co_name))
        
        stock.name = data_list[1]
        dtime = datetime.datetime.strptime(data_list[30], "%Y%m%d%H%M%S")
        stock.price = Price(float(data_list[3]), dtime)
        stock.price_yesterday = Price(float(data_list[4]), dtime)
        stock.price_today_begin = Price(float(data_list[5]), dtime)
        stock.trade_hands = float(data_list[6])
        stock.outer_plate = float(data_list[7])
        stock.inner_plate = float(data_list[8])
        stock.gain_loss = float(data_list[31])
        stock.gain_loss_ratio = float(data_list[32])
        stock.pe_ratio = float(data_list[39])
        stock.circulating_market_value = float(data_list[44])
        stock.total_market_cap = float(data_list[45])
        stock.pb_ratio = float(data_list[46])

def test():
    print("==============================================")
    print("Testing WebSourceTencent......")
    wst = WebSourceTencent()
    st = Stock("sh600104", "上汽集团")
    st2 = Stock("sh600116", "三峡水利")
    wst.fetch_stocks_data([st, st2])
    for st in wst.get_all_stocks():
        print("-----------------------------------------------------------------------")
        st.print()
    print("Finished testing WebSourceTencent......")
    print("==============================================")
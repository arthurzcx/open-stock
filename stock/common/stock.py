# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/24
# @version 1.0
# @desc: Class Stock implementation.

import sys
import xlrd
import xlwt
import inspect

from stock.common.price import Price, PriceList

class Stock:
    """ A Class to describe a STOCK!
    
        A Class should have a variety of infomation, such as: code, name, current price, history price, P/E ratio and so on.
    
    Attributes:
        code: the stock code in market, such as : sh600500, sz300400  
        name: the real name of a stock
        price: the current price
        history_prices: history price 
        trade_hands: trade times today 
        outer_plate: outer stock market
        inner_plate: inner stock market
        gain_loss_ratio: gain/loss ratio, %
        pe_ratio: P/E ratio, Price Earnings Ratio
        circulating_market_value: Circulation Market Value
        total_market_cap: total market capitalization
        pb_ratio: P/B ratio, Price-To-Book, PBR
    """

    def __init__(self, code, name):
        self.code = code
        self.name = name

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        if not isinstance(value, str):
            raise ValueError("function %s(): 'code' must be a str!" %
                             (sys._getframe().f_code.co_name))
        self.__code = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("function %s(): 'name' must be a str!" %
                             (sys._getframe().f_code.co_name))
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, Price):
            raise ValueError("function %s(): 'price' must be a Price object!" % (
                sys._getframe().f_code.co_name))
        self.__price = value

    @property
    def history_prices(self):
        return self.__history_prices

    @history_prices.setter
    def history_prices(self, prices):
        if not isinstance(prices, PriceList):
            raise ValueError("function %s(): 'prices' must be PriceList type!" % (
                sys._getframe().f_code.co_name))
        self.__history_prices = prices

    @property
    def price_yesterday(self):
        return self.__price_yesterday

    @price_yesterday.setter
    def price_yesterday(self, value):
        if not isinstance(value, Price):
            raise ValueError("function %s(): 'value' must be a Price object!" % (
                sys._getframe().f_code.co_name))
        self.__price_yesterday = value

    @property
    def price_today_begin(self):
        return self.__price_today_begin

    @price_today_begin.setter
    def price_today_begin(self, value):
        if not isinstance(value, Price):
            raise ValueError("function %s(): 'value' must be a Price object!" % (
                sys._getframe().f_code.co_name))
        self.__price_today_begin = value

    @property
    def trade_hands(self):
        return self.__trade_hands

    @trade_hands.setter
    def trade_hands(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a int or float type!" % (
                sys._getframe().f_code.co_name))
        self.__trade_hands = value

    @property
    def outer_plate(self):
        return self.__outer_plate

    @outer_plate.setter
    def outer_plate(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a int or float type!" % (
                sys._getframe().f_code.co_name))
        self.__outer_plate = value

    @property
    def inner_plate(self):
        return self.__inner_plate

    @inner_plate.setter
    def inner_plate(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a int or float type!" % (
                sys._getframe().f_code.co_name))
        self.__inner_plate = value

    @property
    def gain_loss(self):
        return self.__gain_loss

    @gain_loss.setter
    def gain_loss(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a float type!" % (
                sys._getframe().f_code.co_name))
        self.__gain_loss = value

    @property
    def gain_loss_ratio(self):
        return self.__gain_loss_ratio

    @gain_loss_ratio.setter
    def gain_loss_ratio(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a float type!" % (
                sys._getframe().f_code.co_name))
        self.__gain_loss_ratio = value

    @property
    def pe_ratio(self):
        return self.__pe_ratio

    @pe_ratio.setter
    def pe_ratio(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a float type!" % (
                sys._getframe().f_code.co_name))
        self.__pe_ratio = value

    @property
    def circulating_market_value(self):
        return self.__circulating_market_value

    @circulating_market_value.setter
    def circulating_market_value(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a float type!" % (
                sys._getframe().f_code.co_name))
        self.__circulating_market_value = value

    @property
    def total_market_cap(self):
        return self.__total_market_cap

    @total_market_cap.setter
    def total_market_cap(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a float type!" % (
                sys._getframe().f_code.co_name))
        self.__total_market_cap = value

    @property
    def pb_ratio(self):
        return self.__pb_ratio

    @pb_ratio.setter
    def pb_ratio(self, value):
        if not isinstance(value, float):
            raise ValueError("function %s(): 'value' must be a float type!" % (
                sys._getframe().f_code.co_name))
        self.__pb_ratio = value

    def get_class_attrs(self):
        """ Get attrs of a cls_name.
        """
        attrs =  inspect.getmembers(Stock, lambda a: not inspect.isfunction(a))
        attrs = list(filter(lambda x: not x[0].startswith('__'), attrs))
        attrs = [ele[0] for ele in attrs]
        return attrs

    def local_print(self, indent="  ", depth=1):
        print(depth*indent + "Stock: ", self.code, self.name)
        depth_incr = depth + 1
        if hasattr(self, "price"):
            print(depth_incr*indent + "price: ")
            self.price.local_print(indent, depth_incr + 1)
        if hasattr(self, "history_prices"):
            print(depth_incr*indent + "history_prices: ")
            self.history_prices.local_print(indent, depth_incr)
        if hasattr(self, "trade_hands"):
            print(depth_incr*indent + "trade_hands: %s" % (self.trade_hands))

    def write(self, xl_sheet, row, col_dict):
        """ Write stock data into xl_sheet.
        The row and column of data is defined in the row interger and col_dict.
                
        Args:
            xl_sheet: the xlwt lib defined sheet 
            row: the data should be written into the row, an integer type
            col_dict: the dict which defines column of data, a dict , the key is name of attribute ,the value is column number         
        """
        if not isinstance(col_dict, dict):
            raise ValueError("function %s: the 'col_dict' paramenter must be a dict type!" % (
                sys._getframe().f_code.co_name))
        for column in col_dict.values():
            if not isinstance(column, int):
                raise ValueError("function %s: the value in col_dict must be an interger to describe the column number" % (
                    sys._getframe().f_code.co_name))
        if not isinstance(row, int):
            raise ValueError("function %s: the 'row' paramenter must be a int type!" % (
                sys._getframe().f_code.co_name))
        
        # print(col_dict)
        for item in col_dict.items():
            if item[0] == 'time':            
                xl_sheet.write(row, item[1], label=self.price.dtime.strftime("%Y-%m-%d %H:%M:%S"))
            elif hasattr(self, item[0]):
                if item[0] == 'price':
                    xl_sheet.write(row, item[1], label=self.price.value)
                elif item[0].startswith("price"):
                    xl_sheet.write(row, item[1], label=getattr(self, item[0]).value)
                else:
                    xl_sheet.write(row, item[1], label=getattr(self, item[0]))

    def write_history(self,  xl_sheet):
        if not hasattr(self, 'history_prices'):
            raise ValueError("function %s: the object does not has history data!" % (
                sys._getframe().f_code.co_name))

        self.history_prices.sort()

        xl_sheet.write(0, 0, 'code')
        xl_sheet.write(0, 1, 'name')
        xl_sheet.write(0, 2, 'date')
        xl_sheet.write(0, 3, 'open')
        xl_sheet.write(0, 4, 'close')
        xl_sheet.write(0, 5, 'high')
        xl_sheet.write(0, 6, 'low')
        xl_sheet.write(0, 7, 'volume')

        counter = 1
        for p in self.history_prices.data:
            xl_sheet.write(counter, 0, label=self.code)
            xl_sheet.write(counter, 1, label=self.name)
            xl_sheet.write(counter, 2, label=p.dtime.strftime("%Y%m%d"))
            xl_sheet.write(counter, 3, label=str(p.open))
            xl_sheet.write(counter, 4, label=str(p.value))
            xl_sheet.write(counter, 5, label=str(p.high))
            xl_sheet.write(counter, 6, label=str(p.low))
            xl_sheet.write(counter, 7, label=str(p.volumn))
            counter = counter + 1


def test():
    print("===========================================")
    print("Testing class Stock......")
    st = Stock("sz002926", "华西证券")
    from datetime import datetime
    st.price = Price(5.5, datetime.strptime(
        "2022-03-24 10:00:00", "%Y-%m-%d %H:%M:%S"))
    pl = PriceList([st.price, st.price])
    st.history_prices = pl
    st.local_print()
    print("Finished calss Stock test......")
    print("===========================================")

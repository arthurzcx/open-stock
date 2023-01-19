# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/23
# @version 1.0
# @desc: define Stock price, with attributes: value(float), dtime(datetime)

import sys
from datetime import datetime

import stock.common.attributes as cattr

class Price:
    """ A class to describe the price of a stock. 
    A Price object should has a float value and a datetime attribute.           
    For example:
    obj = Price()
    obj.value = 5.5
    print(obj.value)

    obj.dtime = datetmie.strptime("2022-03-23 10:00:00", "%Y-%M-%D %H:%M:%S")
    
    Attributes:
        value: the stock price, float data type 
        dtime: the price occurs at the exact time , datetime data type 
    """
    def __init__(self, value, dtime):
        self.value = value
        self.dtime = dtime
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, val):
        if not isinstance(val, float):
           raise  ValueError("function %s: value must be a float!"%(sys._getframe().f_code.co_name))
        self.__value = val
    
    @property
    def dtime(self):
        return self.__dtime
    
    @dtime.setter
    def dtime(self, dtime):
        if not isinstance(dtime, datetime):
            raise ValueError("function %s: dtime must be a datetime object!"%(sys._getframe().f_code.co_name))
        self.__dtime = dtime

    @property
    def open(self):
        return self.__open
    
    @open.setter
    def open(self, val):
        if not isinstance(val, float):
           raise  ValueError("function %s: 'open' must be a float!"%(sys._getframe().f_code.co_name))
        self.__open = val
    
    @property
    def high(self):
        return self.__high
    
    @high.setter
    def high(self, val):
        if not isinstance(val, float):
           raise  ValueError("function %s: 'high' must be a float!"%(sys._getframe().f_code.co_name))
        self.__high = val
    
    @property
    def low(self):
        return self.__low
    
    @low.setter
    def low(self, val):
        if not isinstance(val, float):
           raise  ValueError("function %s: 'low' must be a float!"%(sys._getframe().f_code.co_name))
        self.__low = val
    
    @property
    def volume(self):
        return self.__volumn
    
    @volume.setter
    def volume(self, val):
        if not isinstance(val, float):
           raise  ValueError("function %s: 'volume' must be a float!"%(sys._getframe().f_code.co_name))
        self.__volume = val

    def local_print(self, indent="  ", depth=1):
        print(depth*indent + "value:", str(self.__value), ", dtime:", self.__dtime)

class PriceList:
    """ Price list, store a list of Price objects.

    The class prodives append(obj) and sort() interfaces etc.
    The sort() interface just sort the Price object by datetime from 'ago' to 'now'.    
    
    Attributes:
        data: the list of Price objects , list data type
    """
    def __init__(self, data):
        self.data = data
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, dlist):
        if not isinstance(dlist, list):
            raise ValueError("data must be a 'list' type!")
        for d in dlist:
            if not isinstance(d, Price):
                raise ValueError("funciton %s: The element in data must be Price obejct!"%(sys._getframe().f_code.co_name))
        self.__data = dlist

    def append(self, element):
        """ Add a Price object  into the tail of PriceList class object.
        
        Args:
            element: a Price object
        
        Raises:
           If the element is not a Price object, the ValueError will be rasied.
        """
        if isinstance(element, Price):
            self.__data.append(element)
        else:
            raise ValueError("function %s: The element is not a Price object!"%(sys._getframe().f_code.co_name))
    
    def sort(self):
        """ Sort the price list data by datetime, from 'ago' to 'now'.        
        """
        self.__data.sort(key = lambda price : price.dtime)

    def local_print(self, indent="  ", depth=1):
        for element in self.__data:
            element.print(indent, depth + 1)

def test():
    print("===========================================================")
    print("Testing Price class ......")
    print("New a Price object: p")
    p = Price(5.5, datetime.strptime("2022-02-23 10:00:00", "%Y-%m-%d %H:%M:%S"))
    print("Price value: ", p.value)
    print("Price dtime: ", p.dtime)
    p.print()
    print("Finished Price class test......")
    print("===========================================================")
    print(" ")
    print("===========================================================")
    print("Testing PriceList class......")
    dlist = []
    dlist.append(p)
    p1 = Price(6.5, datetime.strptime("2022-02-23 10:00:00", "%Y-%m-%d %H:%M:%S"))
    p2 = Price(16.5, datetime.strptime("2022-02-23 11:00:00", "%Y-%m-%d %H:%M:%S"))
    p3 = Price(26.5, datetime.strptime("2022-02-23 12:00:00", "%Y-%m-%d %H:%M:%S"))
    p4 = Price(36.5, datetime.strptime("2022-02-23 15:00:00", "%Y-%m-%d %H:%M:%S"))
    p5 = Price(46.5, datetime.strptime("2022-02-23 16:00:00", "%Y-%m-%d %H:%M:%S"))
    p6 = Price(56.5, datetime.strptime("2022-02-23 17:00:00", "%Y-%m-%d %H:%M:%S"))
    dlist.append(p4)
    dlist.append(p5)
    dlist.append(p6)
    dlist.append(p1)
    dlist.append(p2)
    dlist.append(p3)

    pl = PriceList(dlist)
    pl.append(p)
    pl.sort()
    pl.print()
    print("Finished PriceList class test......")
    print("===========================================================")
    
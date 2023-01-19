# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/25
# @version 1.0
# @desc: The class WebSource is the base of a variety of classes which can get data from web.

import asyncio, aiohttp, sys
from stock.common.price import Price
from stock.common.stock import Stock

async def fetch(session, stock, url_source, semaphore):
    async with semaphore:
        url = url_source.get_stock_url(stock)
        print("url: ", url)
        async with session.get(url) as res:    
            if res.status == 200:
                text = await res.text()
                url_source.append_data(stock, text)
            else:
                print("url request status error: %d  %s"%(res.status, url))

async def fetch_history(session, stock, url_source, year, semaphore):
    async with semaphore:
        url = url_source.get_stock_url(stock, year)
        async with session.get(url) as res:    
            if res.status == 200: 
                text = await res.text()
                url_source.append_data(stock, text)
            else:
                print("url request status error: %d  %s"%(res.status, url))

def fetch_web_data(url_source, stocks):    
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(500)
    session = aiohttp.ClientSession()
    tasks = []
    if not hasattr(url_source, 'is_history'):
        tasks = [asyncio.ensure_future(fetch(session, stock, url_source, semaphore)) for stock in stocks ]
    else:
        years = url_source.get_years()
        for year in years:
            for stock in stocks:
                tasks.append(asyncio.ensure_future(fetch_history(session, stock, url_source, year, semaphore)))
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
    loop.run_until_complete(session.close())
    loop.run_until_complete(asyncio.sleep(3))
    loop.close()

class WebSource():
    """ Base class to get data from web.
    
        The class use asyncio mode to get data from web fastly.
    
    Attributes:
        base_url: the web data base url. 
        stocks: a list to store stock code and name 
    """
    def __init__(self):
        self.base_url = ""
        self.stocks = []

    def get_stock_url(self, stock):
        """ Get the stock url by grouping the base_url and stock information.
        
            Need to override it in every child class.
        """
        if not isinstance(stock, Stock):
            raise ValueError("function %s: The input 'stock' paramater must be a Stock object!"%(sys._getframe().f_code.co_name))
        return self.base_url + str(stock.code)

    def append_data(self, stock, text):
        """ Please implements the interface in ervery clild class.
        
            The interface used to parse text which are from response of web request.
            Different web server, differernt response text, so differerent parser interface.
            But the result of parser should be same, the parser data should store in the Stock class object: stock.
        
        Args:
            stock : the Stock class object, the parsed data will be stored into the object. 
            text: the response text from special web server. 
        
        Raises:
           ValueError: if the input stock is not a Stock class object, it's a ValueError.
           text: if the response text of web request is not str or empty, it's a ValueError.
        """
        if not isinstance(stock, Stock):
            raise ValueError("function %s: the input parameter 'stock' must be a Stock class object!"%(sys._getframe().f_code.co_name))
        elif not isinstance(text, str):
            raise  ValueError("function %s: the input parameter 'text' must be str type!"%(sys._getframe().f_code.co_name))
        elif len(text) < 1:
            raise  ValueError("function %s: the input parameter 'text' must be NOT empty!"%(sys._getframe().f_code.co_name))

    def fetch_stocks_data(self, stocks):
        for st in stocks:
            if not isinstance(st, Stock):
                raise ValueError("function %s: The element in 'stocks' input parameter must be Stock objects!"%(sys._getframe().f_code.co_name))        
        fetch_web_data(self, stocks)    
        self.stocks = stocks
    
    def get_all_stocks(self):
        return self.stocks

# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/29
# @version 1.0
# @desc: Draw utils interfaces.

from stock.draw import dfplot
from stock.common import stock
from stock.common.message import print_error
from stock.data import reader
from stock.local.china import china_stocks

def draw_one_stock_today(stock_code_or_name):
    """ Draw one stock today.
    """
    try:
        cs = china_stocks.ChinaStocks()    
        st = cs.get_st_by_info(stock_code_or_name)    
        pd = reader.DataReader().read_today(st)
        dfplot.DfPlot().draw_one_stock_today(pd, st)
    except Exception as e:
        print_error(str(e))
        return

def draw_one_stock_history(stock_code_or_name):
    """ Draw one stock history.
    """
    try:
        cs = china_stocks.ChinaStocks()
        st = cs.get_st_by_info(stock_code_or_name)
        pd = reader.DataReader().read_history(st)
        dfplot.DfPlot().draw_one_stock_history(pd, st)
    except Exception as e:
        print_error(str(e))
        return

def draw_candle(stock_code_or_name):
    """ Draw one stock candle.
    """
    try:
        cs = china_stocks.ChinaStocks()
        st = cs.get_st_by_info(stock_code_or_name)
        pd = reader.DataReader().read_history(st)
        dfplot.DfPlot().draw_candle_history(pd, st)
    except Exception as e:
        print_error(str(e))
        return
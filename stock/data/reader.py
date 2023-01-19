# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/28
# @version 1.0
# @desc: Read xls files to DataFrame type data.

import pandas as pd
import sys, os

from stock.data.utils import UitlsDataDirectory

from stock.common.stock import Stock
from stock.common.message import print_warning


class DataReader():
    """ Read data from .xls files, and coverted to DataFrame type data.
    
        read_history(stock): read history data of a stock    
    """
    def __init__(self):
        pass

    def read_history(self, stock):
        if not isinstance(stock, Stock):
            raise ValueError("function %s(): the 'stock' parameter must be a Stock object!"%(sys._getframe().f_code.co_name))
        dir_history = UitlsDataDirectory().dir_history()
        file_path = os.path.join(dir_history, stock.code + ".xls")
        if not os.path.exists(file_path):
            raise ValueError("function %s(): the file %s does not exist!"%(sys._getframe().f_code.co_name, file_path))
        pdata = pd.read_excel(file_path, parse_dates = ['date'])
        return pdata

    def read_today(self, stock):
        if not isinstance(stock, Stock):
            raise ValueError("function %s(): the 'stock' parameter must be a Stock object!"%(sys._getframe().f_code.co_name))

        dir_today = os.path.join(UitlsDataDirectory().root_path, 'today')        
        dirlist = os.listdir(dir_today)        
        dirlist.sort()        
        if len(dirlist) < 1:
            raise ValueError("function %s(): the dir %s have no data int it!"%(sys._getframe().f_code.co_name, dir_today))        
        
        # find out the lastest price
        latest_dir = None
        for i in range(-1, -len(dirlist), -1):
            dir_cur = os.path.join(dir_today, dirlist[i])
            if os.listdir(dir_cur):
                latest_dir = dir_cur
                break
        if latest_dir is None:
            raise ValueError("function %s(): the dir %s have no latest data!"%(sys._getframe().f_code.co_name, dir_today))    

        file_path = os.path.join(latest_dir, stock.code + ".xls")
        if not os.path.exists(file_path):
            raise ValueError("function %s(): the file %s does not exist!"%(sys._getframe().f_code.co_name, file_path))
        # file_path = UitlsDataDirectory().file_today(stock)
        # if not os.path.exists(file_path):
        #     raise ValueError("function %s(): the file %s does not exist!"%(sys._getframe().f_code.co_name, file_path))
        pdata = pd.read_excel(file_path, parse_dates = ['time'])
        return pdata
    
    def today_price(self, stock):
        if not isinstance(stock, Stock):
            raise ValueError("function %s(): the 'stock' parameter must be a Stock object!"%(sys._getframe().f_code.co_name))
        file_path = UitlsDataDirectory().file_today(stock)
        if not os.path.exists(file_path):
            raise ValueError("function %s(): the file %s does not exist!"%(sys._getframe().f_code.co_name, file_path))
        pdata = pd.read_excel(file_path, parse_dates = ['time'])
        return float(pdata.at[pdata.shape[0] - 1, 'price'])

    def lates_price(self, stock):
        """ Get the latest price of a stock.
        Sometime, such as Staturday or Sunday, there is no today_price, so we shoule use the latest price.
        
        Args:
            stock: a Stock class object. 
        """
        if not isinstance(stock, Stock):
            raise ValueError("function %s(): the 'stock' parameter must be a Stock object!"%(sys._getframe().f_code.co_name))        
        dir_today = os.path.join(UitlsDataDirectory().root_path, 'today')        
        dirlist = os.listdir(dir_today)        
        dirlist.sort()        
        if len(dirlist) < 1:
            raise ValueError("function %s(): the dir %s have no data int it!"%(sys._getframe().f_code.co_name, dir_today))        
        
        # find out the lastest price
        latest_dir = None
        for i in range(-1, -len(dirlist), -1):
            dir_cur = os.path.join(dir_today, dirlist[i])
            if os.listdir(dir_cur):
                latest_dir = dir_cur
                break
        if latest_dir is None:
            raise ValueError("function %s(): the dir %s have no latest data!"%(sys._getframe().f_code.co_name, dir_today))    

        file_path = os.path.join(latest_dir, stock.code + ".xls")
        if not os.path.exists(file_path):
            raise ValueError("function %s(): the file %s does not exist!"%(sys._getframe().f_code.co_name, file_path))
        pdata = pd.read_excel(file_path, parse_dates = ['time'])
        return pdata.iloc[pdata.shape[0] - 1] # data in a row

    def read_all_section(self, with_complete_file_path=False):
        '''
        读取所有板块的列表
        板块的列表存在与data/setion目录下，该目录下的每个xls文件的名称即是板块名称

        Args:
            with_complete_file_path: 默认False, 返回板块列表； 如果设置为True，则返回所有板块文件的完整路径
        '''
        dir_section = UitlsDataDirectory().dir_section()
        files = os.listdir(dir_section)
        ret_list = []
        for file in files:
            if with_complete_file_path==True:
                ret_list.append(os.path.join(dir_section, file))
            else:
                ret_list.append(os.path.splitext(os.path.basename(file))[0])
        return ret_list
    
    def read_section(self, section_name):
        '''
        读取某个板块内所有的股票代码和名称
        
        Args:
            section_name 板块名称，对应data/sectors目录下某个板块文件
        '''
        dir_section = UitlsDataDirectory().dir_section()
        path_file = os.path.join(dir_section, section_name + '.xls')
        if not os.path.exists(path_file):
            print_warning("板块文件可能不存在， 文件位置为：" + path_file)
            return
        data = pd.read_csv(path_file, sep='\t', encoding='gbk', error_bad_lines=False)
        stocks = []
        for index,row in data.iterrows():
            st = Stock(row["代码"].lower(),row["名称"])
            stocks.append(st)        
        return stocks

    def read_market_value_latest(self):
        '''
        读取当前最新的市值文件数据，也就是data/market_value目录下最近日期的文件数据
        
        @return 
            返回DataFrame格式的最新市值数据，数据rows和coulumns与market_value文件数据内容保持一致
        '''
        dir_market_value = UitlsDataDirectory().dir_market_vaule()
        files = os.listdir(dir_market_value)
        files.sort(reverse=True) # 按照字母降序排列，最新的在第一个
        
        # 最新的市值文件
        if len(files) < 1:
            print_warning("data/market_value目录为空，市值数据文件不存在")
        file_latest = files[0]
        path_latest = os.path.join(dir_market_value, file_latest)
        
        # 读取最新市值数据文件
        data = pd.read_excel(path_latest)
        return data
    
    def read_broad_cap_index_latest(self):
        '''
        读取最新的大盘指数文件
        
        Returns:
            返回padans.DataFrame格式的最新市值数据
        '''
        dir_broad_cap_index = UitlsDataDirectory().dir_broad_cap_index()
        files = os.listdir(dir_broad_cap_index)
        files.sort(reverse=True) # 按照字母降序排列，最新的在第一个
        
        # 最新的市值文件
        if len(files) < 1:
            print_warning(
                "data/broad_cap_index目录为空，大盘指数数据文件不存在")
        file_latest = files[0]
        path_latest = os.path.join(dir_broad_cap_index, file_latest)
        
        # 读取最新大盘指数数据文件
        data = pd.read_excel(path_latest)
        return data        
        

def test_read_to_dataframe_type_data():
    print("====================================================")
    print("Testing DataReader() class interfaces......")
    dr = DataReader()
    from local.china.china_stocks import ChinaStocks    
    stock = ChinaStocks().stocks_a()[-1]
    print("DataFrame data: ", dr.read_history(stock))
    print("Finished testing DataReader() class interfaces......")
    print("====================================================")
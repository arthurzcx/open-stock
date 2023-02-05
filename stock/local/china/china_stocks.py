# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/26
# @version 1.0
# @desc: China stocks.

import json
import os
import sys

from stock.common.stock import Stock
from stock.common.message import print_info, print_warning, print_error, Color, Style, Message

import pandas as pd


class ChinaStocks():
    """ Get all stocks in China market.    
    
    Attributes:
        stocks_shanghai: stocks in Shanghai market 
        stocks_shenzhen: stocks in Shenzhen market
        stocks_beijing: stocks in Beijing , not support now 2022/03/28
    """

    def __init__(self):
        self.root_path = os.path.join(os.getcwd(), 'stock', 'local', 'china')
        self.stocks_shanghai = self.__stocks("shanghai")
        self.stocks_shenzhen = self.__stocks("shenzhen")
        self.stocks_kechuang = self.__stocks("kechuang")
        self.stocks_chuangye = self.__stocks("chuangye")
        self.stocks_all = self.stocks_shanghai + self.stocks_shenzhen + \
            self.stocks_kechuang + self.stocks_chuangye

    def __stocks(self, name):
        """ 
        Get all stocks in Shanghai market. 
        """
        file_path = os.path.join(self.root_path, 'stocks_' + name + '.json')

        stocks = []
        with open(file_path, 'r', encoding='utf-8') as f:
            sts = json.load(f)
            for ele in sts.items():
                stocks.append(Stock(ele[1], ele[0]))
            f .close()
        if name == "shanghai":
            stocks.append(Stock("sh000001", "上证指数"))
            stocks.append(Stock("sh000688", "科创50"))
            stocks.append(Stock("sh000016", "上证50"))
        elif name == "shenzhen":
            stocks.append(Stock("sz399001", "深证成指"))
            stocks.append(Stock("sz399006", "创业板指"))
            stocks.append(Stock("sz399300", "沪深300"))
        return stocks
    
    def broad_cap_index(self):
        '''
        获取大盘指数对应Stock对象
        
        Returns:
            Stock对象表示的大盘指数
        '''
        stocks = []
        stocks.append(Stock("sh000001", "上证指数"))
        stocks.append(Stock("sh000688", "科创50"))
        stocks.append(Stock("sh000016", "上证50"))
        stocks.append(Stock("sz399001", "深证成指"))
        stocks.append(Stock("sz399006", "创业板指"))
        stocks.append(Stock("sz399300", "沪深300"))
        return stocks
    
    def stocks_sh(self):
        """ 
        Get all stocks in Shanghai markets.
        """
        return self.stocks_shanghai

    def stocks_sz(self):
        """ 
        Get all stocks in Shenzhen markets.
        """
        return self.stocks_shenzhen

    def stocks_kc(self):
        return self.stocks_kechuang

    def stocks_cy(self):
        return self.stocks_chuangye     

    def stocks_bj(self):
        """ 
        Get all stocks in Beijing markets.
        """
        return None

    def stocks_a(self):
        """ 
        Get all stocks in China markets.
        """
        return self.stocks_all

    def count_stocks_shanghai(self):
        """ Get number of stocks in shanghai market.
        """
        if hasattr(self, 'stocks_shanghai'):
            return len(self.stocks_shanghai)
        else:
            raise ValueError("function %s(): can not get stocks_shanghai information!" % (
                sys._getframe().f_code.co_name))

    def count_stocks_shenzhen(self):
        """ Get number of stocks in shenzhen market.
        """
        if hasattr(self, 'stocks_shenzhen'):
            return len(self.stocks_shenzhen)
        else:
            raise ValueError("function %s(): can not get stocks_shenzhen information!" % (
                sys._getframe().f_code.co_name))

    def count_stocks_a(self):
        """ Get number of stocks in China stocks market.
        """
        if hasattr(self, 'stocks_all'):
            return len(self.stocks_all)
        else:
            raise ValueError("function %s(): can not get stocks_all information!" % (
                sys._getframe().f_code.co_name))

    def find_a_stock(self, stock_code_or_name):
        """ 
        Find the exact code and name of your input incomplete code or name.
        
        For example: if you type "004",  the function will search "004" in all stocks' code and name. Then print them.
        
        Args:
            stock_code_or_name:  incomplete code or name. 
        """
        found_list = []
        for st in self.stocks_all:
            if stock_code_or_name in st.code or stock_code_or_name in st.name:
                found_list.append(st)
        if len(found_list) == 0:
            print_warning("Sorry, can not find the stock which contains the str you type: %s"%(stock_code_or_name))
        else:
            print_info("Found stocks which code or name contains the str you type '%s' as follows:"%(stock_code_or_name))
            for st in found_list:
                print(" %s %s"%(st.code, st.name))
        return found_list

    def get_st_by_info(self, st_code_or_name):
        """ Get the stock object by code or name.
        
        Args:
            st_code_or_name: should be the exact code or name, complete infomation.

        Raises:
           value error: if the stock does not exist, raise a ValueError
        """
        for st in self.stocks_all:
            if st_code_or_name == st.code or st_code_or_name == st.name:
                return st
        raise ValueError("function %s(): can not get stock by the input parameter '%s', may be it is not exact code or name!" % (
            sys._getframe().f_code.co_name, st_code_or_name))

class ChinaOfficialConvertToJson():
    """ Convert official xls files (from official web page) to json files.
    """

    def __init__(self):
        self.official_path = os.path.join(
            os.getcwd(), 'local', 'china', 'official_xls')
        self.file_official_kechuang = os.path.join(
            self.official_path, 'kechuang.xls')
        self.file_official_shanghai = os.path.join(
            self.official_path, 'shanghai.xls')
        self.file_official_chuangye = os.path.join(
            self.official_path, 'chuangye.xlsx')
        self.file_official_shenzhen = os.path.join(
            self.official_path, 'shenzhen.xlsx')

        self.json_path = os.path.join(os.getcwd(), 'local', 'china')
        self.json_kechuang = os.path.join(
            os.getcwd(), 'local', 'china', 'stocks_kechuang.json')
        self.json_shanghai = os.path.join(
            os.getcwd(), 'local', 'china', 'stocks_shanghai.json')
        self.json_chuangye = os.path.join(
            os.getcwd(), 'local', 'china', 'stocks_chuangye.json')
        self.json_shenzhen = os.path.join(
            os.getcwd(), 'local', 'china', 'stocks_shenzhen.json')

        self.convert_kechuang()
        self.convert_shanghai()
        self.convert_chuangye()
        self.convert_shenzhen()

    def convert_kechuang(self):
        """ 
        Convert official file 'local/official_xls/kechaung.xls' from official web to json file.
        """
        df = pd.read_excel(self.file_official_kechuang)
        dict_kc = {}
        rows = df.shape[0]

        for i in range(0, rows):
            dict_kc[df.iloc[i, 1]] = "sh" + str(df.iloc[i, 2])

        with open(self.json_kechuang, "w", encoding='utf-8') as f:
            js = json.dumps(dict_kc, ensure_ascii=False, indent=4)
            f.write(js)
            f.close()

    def convert_shanghai(self):
        """ 
        Convert official file 'local/official_xls/shanghai.xls' from official web to json file.
        """
        df = pd.read_excel(self.file_official_shanghai)
        dict_sh = {}
        rows = df.shape[0]

        for i in range(0, rows):
            dict_sh[df.iloc[i, 1]] = "sh" + str(df.iloc[i, 2])

        with open(self.json_shanghai, "w", encoding='utf-8') as f:
            js = json.dumps(dict_sh, ensure_ascii=False, indent=4)
            f.write(js)
            f.close()

    def convert_chuangye(self):
        """ 
        Convert official file 'local/official_xls/chuangye.xlsx' from official web to json file.
        """        
        df = pd.read_excel(self.file_official_chuangye)
        dict_cy = {}
        rows = df.shape[0]

        for i in range(0, rows):
            dict_cy[df.iloc[i, 5]] = "sz" + str(df.iloc[i, 4]).rjust(6, '0')

        with open(self.json_chuangye, "w", encoding='utf-8') as f:
            js = json.dumps(dict_cy, ensure_ascii=False, indent=4)
            f.write(js)
            f.close()

    def convert_shenzhen(self):
        """ 
        Convert official file 'local/official_xls/shenzhen.xlsx' from official web to json file.
        """            
        df = pd.read_excel(self.file_official_shenzhen)
        dict_sz = {}
        rows = df.shape[0]

        for i in range(0, rows):
            dict_sz[df.iloc[i, 5]] = "sz" + str(df.iloc[i, 4]).rjust(6, '0')

        with open(self.json_shenzhen, "w", encoding='utf-8') as f:
            js = json.dumps(dict_sz, ensure_ascii=False, indent=4)
            f.write(js)
            f.close()


def test():
    print("============================================================")
    print("Testing ChinaStock class......")
    cs = ChinaStocks()
    print("------------------------------------------------------------------------------------------------")
    print("All stocks in Shanghai market: ")
    for st in cs.stocks_sh():
        st.local_print()
    print("\n------------------------------------------------------------------------------------------------")
    print("All stocks in Shenzhen market: ")
    for st in cs.stocks_sz():
        st.local_print()

    print("\n------------------------------------------------------------------------------------------------")
    print("All stocks in China market: ")
    for st in cs.stocks_a():
        st.local_print()
    print("Finished testing ChinaStock......")
    print("============================================================")

    # ChinaOfficialConvertToJson()
    print("shanghai: %d"%(len(cs.stocks_sh())))
    print("shenzhen: %d"%(len(cs.stocks_sz())))
    print("kechuang: %d"%(len(cs.stocks_kc())))
    print("chuangye: %d"%(len(cs.stocks_cy())))

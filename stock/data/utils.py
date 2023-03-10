# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/26
# @version 1.0
# @desc: Utils class to manage data.

import os, sys
from datetime import datetime

from stock.common.stock import Stock

class UitlsDataDirectory():
    """ Manage data directories.
    file_current():  data/current/current.xls;

    dir_history(): data/history;

    dir_test(): data/test;
    
    Attributes:
        root_path: data path 
    """
    def __init__(self):
        self.root_path =  os.path.join(os.getcwd(), 'data')        

    def file_current(self):
        """ Get current.xls complete path.
        The directory will be created automaticall in this function.
        """
        dir_path = os.path.join(self.root_path, "current")
        file_path = os.path.join(dir_path, "current.xls")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return file_path

    def dir_today(self):
        """ Get directory path of todaty data.
        
            The directory stores everyday stock data, which will be very large. 
        """
        dir_path = os.path.join(self.root_path, "today", datetime.today().strftime("%Y-%m-%d"))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path
    
    def file_today(self, stock):
        """ Get the file fo a stock, that the file stores the today data.
        """
        if not isinstance(stock, Stock):
            raise ValueError("function %s(): tht parameter 'stock' must be a Stock object!" % (
                sys._getframe().f_code.co_name))
        return os.path.join(self.dir_today(), stock.code  + ".xls")

    def dir_history(self):
        """ Get history complete directory path.
        The directory will be created automatically in this function.
        """
        dir_path = os.path.join(self.root_path, "history")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def dir_market_vaule(self):
        '''
        ????????????????????????????????????????????????????????????????????????????????????
        
        @return: ???????????????????????????????????????????????????
        '''
        dir_path = os.path.join(self.root_path, "market_value")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path
    
    def dir_broad_cap_index(self):
        '''
        ????????????????????????????????????????????????????????????????????????????????????????????????
        
        Returns:
            ??????????????????????????????
        '''
        dir_path = os.path.join(self.root_path, "broad_cap_index")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path        

    def dir_test(self):
        """ Get test complete directory path.
        The directory will be created automatically in this function.
        """
        dir_path = os.path.join(self.root_path, "test")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path
    
    def dir_section(self):
        '''
        ??????????????????
        '''
        dir_path = os.path.join(self.root_path, "sectors")
        if not os.path.exists(dir_path):
            print(dir_path)
            raise ValueError("????????????data/section?????????!")
        return dir_path
    
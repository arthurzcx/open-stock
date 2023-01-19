# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/26
# @version 1.0
# @desc: Utils interfaces for data updating.

import xlrd, xlwt
from xlutils.copy import copy
import datetime
import os, sys
import asyncio
import time

from stock.local.china.china_stocks import ChinaStocks
from stock.web.tencent.tencent import WebSourceTencent
from stock.web.tencent.tencent_history import WebSourceTencentHistory

from stock.data.utils import UitlsDataDirectory
from stock.common.dtime import UtilDateTime
from stock.common.message import print_error, print_warning, print_info
# from common.attributes import get_class_attrs
from stock.common.stock import Stock

class UtilsUpdateData():
    """ Wrapper for web utils interfaces.
    
        functions:
        1) Current data updating: update_current() for current stock prices updating;
        2) History data updating: update_history() for history stock prices updating;


    """
    def __init__(self):
        self.exit_update_today = False
    
    def exit_update(self):
        self.exit_update_today = True
    
    def is_market_open(self, market="China"):
        """ Is stocks market open or not
        """
        if market == "China":
            beijing_now = UtilDateTime.now_beijing()           
            now = beijing_now.strftime("%H%M")
            return ((now >= "0930" and now <= "1130") or (now >= "1300" and now <= "1500"))
        
        return False
    
    def is_market_closed(self, market="China"):
        """ Whether the market has closed or not.
        """
        utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        if market == "China":
            beijing_now = utc_now.astimezone(datetime.timezone(datetime.timedelta(hours=8), name='Asia/Shanghai',))
            now = beijing_now.strftime("%H%M")
            return ( now > "1500")
        
        return False
    
    def update_current(self):
        """
        Update current stock prices.
        Save file to "data/current/current.xls".
        """
        cs = ChinaStocks()
        stocks = cs.stocks_a()
        wsth = WebSourceTencent()
        wsth.fetch_stocks_data(stocks)
        stocks = wsth.get_all_stocks()

        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet('stocks_china')
        col_dict = {"code":0, "name":1, "time":2, "price":3, "gain_loss_ratio":4, "total_market_cap":5}
        for item in col_dict.items():
            sheet.write(0, item[1], item[0])

        for i in range(0, len(stocks)):
            stocks[i].write(sheet, i +1, col_dict)
                
        xlpath = UitlsDataDirectory().file_current()
        if os.path.exists(xlpath):
            os.remove(xlpath)
        wb.save(xlpath)
        print("The current data file: %s"%(xlpath))
        print("Finished updating current stocks price ......")
    
    def update_history(self, years=1):
        """ Update history stocks prices.
        Save files to "data/history/[code].xls".        
        
        Args:
            years: how many years history data to get, default 4 years 
        """
        if isinstance(years, str):
            years = int(years)
        print("history data directory: ", UitlsDataDirectory().dir_history())
        cs = ChinaStocks()
        stocks = cs.stocks_a()
        wsth = WebSourceTencentHistory(years)
        wsth.fetch_stocks_data(stocks)
        stocks = wsth.get_all_stocks()

        data_dir = UitlsDataDirectory().dir_history()
        print("history data directory: ", data_dir)
        for st in stocks:
            wb = xlwt.Workbook(encoding='utf-8')
            sheet = wb.add_sheet('stocks_history')        
            st.write_history(sheet)
            
            xlpath = os.path.join(data_dir,  st.code + ".xls")
            if os.path.exists(xlpath):
                os.remove(xlpath)
            wb.save(xlpath)
        print("Stored data into directory: %s"%(data_dir))
        print("Finished updating history data...")
    
    def update_today(self, period_seconds=300):
        """ Update today data preiodically.
        
            The data will be stored into 'data/today/yyyy-mm-dd/[stock_code].xls
        
        Args:
            period_seconds:  period, unit: seconds
        """
        weekday = UtilDateTime.weekday(UtilDateTime().now_beijing())
        if weekday > 5:
            print_warning("It's weekend today. The market is not open.")
            return

        while True:
            if self.exit_update_today == True:
                print("update_today() has exited......")
                return
            if self.is_market_closed("China"):
                print("function %s(): the Chinese stocks market has closed today!" % (
                    sys._getframe().f_code.co_name))
                return
            if not self.is_market_open("China"):
                time.sleep(5)
                continue
            begin = time.time()
            #  run
            cs = ChinaStocks()
            stocks = cs.stocks_a()
            wsth = WebSourceTencent()
            wsth.fetch_stocks_data(stocks)
            stocks = wsth.get_all_stocks()

            # col_dict = {"code":0, "name":1, "time":2, "price":3, "gain_loss_ratio":4}
            st_class_attrs = stocks[0].get_class_attrs()
            col_dict = {}
            for i in range(0, len(st_class_attrs)):
                col_dict[st_class_attrs[i]] = i

            col_dict['time'] = len(st_class_attrs)
            
            for st in stocks:
                file_path = UitlsDataDirectory().file_today(st)
                if not os.path.exists(file_path):
                    # write header
                    wb = xlwt.Workbook(encoding='utf-8')
                    sheet = wb.add_sheet('price_today')                    
                    for item in col_dict.items():
                        sheet.write(0, item[1], item[0])
                    wb.save(file_path)

                #write data
                rd_xls = xlrd.open_workbook(file_path)
                rows = rd_xls.sheets()[0].nrows
                wt_xls = copy(rd_xls)
                ws = wt_xls.get_sheet(0)
                st.write(ws, rows, col_dict)
                wt_xls.save(file_path)

            end = time.time()
            cost = end - begin
            
            if cost < period_seconds:
                time.sleep(period_seconds - cost)
    
    def update_market_value(self):
        '''
        每日更新市值数据，目录为data/market_value, 注意每日产生一个以当天日期命名的文件
        @attention: 如果当日文件已经存在，则覆盖；理论上每天只需要更新一次. 定时更新任务请在外部实现！
        '''        
        dt_today = UtilDateTime.now_beijing().strftime("%Y-%m-%d")
        file_path_market_value = os.path.join(UitlsDataDirectory().dir_market_vaule(), dt_today + ".xls")
        
        cs = ChinaStocks()
        stocks = cs.stocks_a()
        wsth = WebSourceTencent()
        wsth.fetch_stocks_data(stocks)
        stocks = wsth.get_all_stocks()

        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet('stocks_china')
        col_dict = {"code":0, "name":1, "time":2, "price":3, "gain_loss_ratio":4, "total_market_cap":5}
        for item in col_dict.items():
            sheet.write(0, item[1], item[0])

        for i in range(0, len(stocks)):
            stocks[i].write(sheet, i +1, col_dict)
                
        wb.save(file_path_market_value)
        print("市值文件路径: %s"%(file_path_market_value))
        print("已完成市值数据文件的更新 ......")      
    
    def update_broad_cap_index(self):
        '''
        更新大盘指数数据
        产生的文件为：data/broad_cap_index/yyyy-mm-dd.xls
        '''
        dt_today = UtilDateTime.now_beijing().strftime("%Y-%m-%d")
        file_path_broad_cap_index = os.path.join(UitlsDataDirectory().dir_broad_cap_index(), dt_today + ".xls")
        
        cs = ChinaStocks()
        stocks = cs.broad_cap_index()
        wsth = WebSourceTencent()
        wsth.fetch_stocks_data(stocks)
        stocks = wsth.get_all_stocks()

        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet('stocks_china')
        col_dict = {"code":0, "name":1, "time":2, "price":3, "gain_loss_ratio":4,"gain_loss":5, "total_market_cap":6}
        for item in col_dict.items():
            sheet.write(0, item[1], item[0])

        for i in range(0, len(stocks)):
            stocks[i].write(sheet, i +1, col_dict)
                
        wb.save(file_path_broad_cap_index)
        print("大盘指数文件路径: %s"%(file_path_broad_cap_index))
        print("已完成大盘指数数据文件的更新 ......")      
        
def thread_update_market_value(trigger_hour=17):
    '''
    每日更新市值的定时任务
    Args:
        trigger_hour 触发线程的每日时间，比如17代表下午5点
    '''  
    # weekday = UtilDateTime.weekday(UtilDateTime.now_beijing())
    dtime_beijing = UtilDateTime.now_beijing()
    if UtilDateTime.is_valid_trade_day(dtime_beijing) is False:
        print_warning("非交易日，不更新市值数据!")
        return
    
    while True:
        hour = UtilDateTime.now_beijing().hour
        if hour >= trigger_hour:
            UtilsUpdateData().update_market_value()
            return
        else:
            time.sleep(600)

def thread_update_broad_cap_index(trigger_hour=17):
    '''
    每日更新大盘指数的线程任务
    '''
    dtime_beijing = UtilDateTime.now_beijing()
    if UtilDateTime.is_valid_trade_day(dtime_beijing) is False:
        print_warning("非交易日，不更新大盘指数数据!")
        return
    
    while True:
        hour = UtilDateTime.now_beijing().hour
        if hour >= trigger_hour:
            UtilsUpdateData().update_broad_cap_index()
            return
        else:
            time.sleep(600)

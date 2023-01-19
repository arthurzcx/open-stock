# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/27
# @version 1.0
# @desc: Extra complex test about China market stocks is here.

from stock.local.china.china_stocks import ChinaStocks
from stock.data.reader import DataReader, UitlsDataDirectory
from stock.local.china import china_stocks
from stock.common import stock
from stock.common.dtime import UtilDateTime
from stock.common.message import print_info
from _datetime import datetime
import _datetime,os
import pandas as pd

class TestChina():
    """
     Test China market stocks class.
    """

    def __init__(self):
        pass
    
    def test_counter_stocks(self):
        cs = ChinaStocks()
        print("Number of stocks:")
        print("  all: %d"%(cs.count_stocks_a()))
        print("  Shanghai: %d"%(cs.count_stocks_shanghai()))
        print("  Shenzhen: %d"%(cs.count_stocks_shenzhen()))

    def test_read_all_section_list(self):
        data_reader = DataReader()
        list_section = data_reader.read_all_section(with_complete_file_path=False)
        list_section_file = data_reader.read_all_section(True)
        print("list of sections: ============")
        print(list_section)
        print("list of seciton files:===========")
        print(list_section_file)
        
    def test_read_on_section(self):
        '''
        测试读取某个板块文件内容
        '''
        data_reader = DataReader()
        list_section = data_reader.read_all_section(with_complete_file_path=False)
        print("板块：" + list_section[0])
        data_reader.read_section(section_name=list_section[0])
        
    def create_market_value_data_from_history(self):
        '''
        由于缺少连续的市值数据用于实际计算，暂时使用该函数接口从history和当前最新的market_value数据文件反推
        假的、连续的市值文件，产生的数据仅用于当前的测试，真实的投资决策依赖该数据可能会存在偏差
        '''
        ca = china_stocks.ChinaStocks()
        stocks_all = ca.stocks_a()
        
        # data reader init
        reader = DataReader()
        
        # 存储市值数据的目录
        dir_market_value = UitlsDataDirectory().dir_market_vaule()
        
        # 读取历史数据
        data_history = {}
        for stock in stocks_all:
            data_history[stock.code] = reader.read_history(stock)
        
        # 读取市值数据
        data_market_value = reader.read_market_value_latest()
        print_info("全部数据已经读入...")
        
        # 向前计算天数N，先生成不包括周末的合法时间
        days_N = 60
        days = []
        now_dt = UtilDateTime().now_beijing() #当前时间
        for i in range(0,days_N):
            day_temp = now_dt + _datetime.timedelta(days=-i)
            weekday = UtilDateTime().weekday(day_temp)
            if weekday > 5:
                continue
            days.append(day_temp)
        
        # 遍历所有合法时间
        for day in days:
            dt_history = day.strftime("%Y%m%d")
            dt_market_value = day.strftime("%Y-%m-%d")
            
            data_day = {}
            codes = []
            values = []
            for code in data_market_value["code"]:
                df = data_history[code]
                try:
                    price_day = float(df[df['date'] == dt_history]['close'].iloc[0])
                    price_market_value = float(data_market_value[data_market_value["code"] == code]["price"].iloc[0])
                    market_cap_latest = float(data_market_value[data_market_value["code"] == code]["total_market_cap"].iloc[0])
                    market_cap_day = market_cap_latest*price_day/price_market_value
                    codes.append(code)
                    values.append(market_cap_day)
                except Exception as e:
                    continue
            data_day = {"code":codes, "total_market_cap":values}
            
            # 存储文件
            path_save_file = os.path.join(dir_market_value, dt_market_value + ".xls")
            df_save = pd.DataFrame(data_day)
            df_save.to_excel(path_save_file)
        print_info("已经生成连续的市值数据文件！注意这些文件只能参考，不能作为实际投资的实际数据。")
            
        
            
    
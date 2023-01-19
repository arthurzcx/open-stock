from stock.data.reader import DataReader
from stock.data.utils import UitlsDataDirectory

import os, pandas
import stock.common.message as Message
from stock.common.dtime import UtilDateTime
from stock.analyzer.analyzer_average_continous import AnalyzerAverageContinous 
from _datetime import datetime
import _datetime

class UtilsDataSector():
    """
    实用类用于处理行业板块数据
    """
    
    def __init__(self):
        self.reader = DataReader()
        self.udd = UitlsDataDirectory()
    
    def read_sector_day(self, sector, dtime):
        """
        读取某个日期、某个行业板块中的市值数据
        
        Args:
        @sector 行业板块的名称，例如5G，应该与data/sectors目录下文件同名，不需要后缀
        @dtime 日期, 传入的参数应为datetime 对象
        """
        path_market_value = os.path.join(self.udd.dir_market_vaule(), dtime.strftime("%Y-%m-%d") + ".xls")
        if not os.path.exists(path_market_value):
            Message.print_error("市值数据文件缺失:" + path_market_value)
            return None
        
        # 读取板块内股票列表和对应日志的市值数据
        stocks = self.reader.read_section(sector)
        if len(stocks) < 1:
            Message.print_error("没有读取到板块内的股票列表!")
            return None
        
        data_mv = pandas.read_excel(path_market_value)
        
        # 计算板块总市值
        total_mv = 0.0
        for st in stocks:
            df = data_mv[data_mv['code'] == st.code]
            if df.empty:
                continue
            mv = float(df["total_market_cap"].iloc[0])
            total_mv += mv
        
        # 非法市值，可能放假
        if total_mv < 0.1: 
            return None
        return total_mv
        
    def read_sector_continous_days(self, sector, days=30):
        '''
        读取某个行业板块连续多日的市值数据
        
        Args:
        @sector 行业板块名称，与data/sectors下文件名称一致
        @days 连续天数，从当前时间向前推
        '''    
        now = UtilDateTime.now_beijing()
        
        dts = []
        values = []
        for i in range(-1*days, 1):
            dt = now + _datetime.timedelta(days=i)
            if not UtilDateTime.is_valid_trade_day(dt):
                continue
            market_value = self.read_sector_day(sector, dt)
            if market_value is None:
                continue
            dts.append(dt)
            values.append(market_value)
        data = {"date":dts, "market_value":values}
        return pandas.DataFrame(data=data)
    
    def read_sector_continous_days_ma(self, sector, days=30, ma_days=7):
        '''
        读取某行业板块连续多日的移动平均线
        
        Args:
        @sector 行业板块名称
        @days 连续多日的天数，分析数据的总量
        @ma_days 移动平均线的天数， 例如7日移动均线
        '''
        data = self.read_sector_continous_days(sector, days)
        aac = AnalyzerAverageContinous(continous_days=ma_days,total_days=data.shape[0])
        data_ma = aac.analyze(data=[data['date'], data['market_value']])
        return pandas.DataFrame({'date':data_ma[0], 'market_value':data_ma[1]})
        
    
def test_read_sector_day(sector, dtime):
    """
    测试读取某日、某行业板块的总市值
    """
    uds = UtilsDataSector()
    total_market_value = uds.read_sector_day(sector, dtime)
    print(sector +"行业板块在" + dtime.strftime("%Y-%m-%d") + "日的总市值为:" + str(total_market_value) + "亿元")

def test_read_sector_continous_days(sector, days):
    '''
    测试读取某个行业板块连续多日的市值数据
    
    Args:
    @sector 行业板块名称
    @days 从现在的日期向前退的连续天数
    '''
    
    uds = UtilsDataSector()
    data = uds.read_sector_continous_days(sector, days=30)
    print(sector + "板块在连续" + str(days) + "日的市值数据如下：")
    print(data)
    
# -*- coding: utf-8 -*-

from stock.data.utils_sector import UtilsDataSector
from stock.analyzer import analyze_utils
from stock.analyzer.analyzer import Analyzer, AnalyzerConfig

class AnalyzerSectorConfig(AnalyzerConfig): 
    '''
    板块分析的参数配置
    '''
    
    def __init__(self, **kwargs):
        super(AnalyzerSectorConfig,self).__init__(**kwargs)
        self.continous_days = 50 #连续分析的天数, 总是从当前日期向前推
        self.ma_days = 7 #求取移动平均线的天数
        self.increase_continous_days = 3 #近期连续增长多少天，视为入手的信号
        self.decrease_continous_days = 2 #近期联系下跌多少天，视为出手的信号

class AnalyzerSectorResult():
    '''
    板块分析结果类，必须时在AnalyzerSectorConfig的条件下分析出的结果
    '''
    def __init__(self):
        self.sector = None #分析的板块的名称
        self.df_data_order_by_market_value = None #按照市值从大到小排序的板块内各个股票数据
        self.config = AnalyzerSectorConfig() #在什么样的参数配置下产生的结果
        
        self.trigger_increase_continous_days = False # 触发连续增长的入手信号
        self.trigger_decrease_continous_days = False #触发联系下跌的出手信号
        
        self.increase_continous_days = 0 #当连续增长信号触发时，已经连续增长多少天
        self.decrease_continous_days = 0 #当连续下跌信号触发时，已经连续下跌多少天
        
        self.increase_continous_ratio = 0.0 #连续增长的累计百分比
        self.decrease_continous_ratio = 0.0 #连续下跌的累计百分比
                
class AnalyzerSector(Analyzer):
    '''
    板块分析类
    '''
    
    def __init__(self,**kwargs):
        '''
        Arguments:
            config: AnalyzerSectorConfig对象，配置分析参数
            sector: 板块名称
        '''
        super(AnalyzerSector,self).__init__(**kwargs)
        if 'sector' not in kwargs.keys():
            raise Exception("AnalyzerSector构造函数的src_data中缺失sector数据!")
        self.sector = kwargs["sector"]
    
    def run(self):
        '''
        根据配置参数结果和输入的板块数据，分析板块行情
        
        Arguments:
            config和sector已经在构造函数中传入
        
        Return: 
            AnalyzerSectorResult对象表示的分析结果
        '''
        config = self.config
        sector = self.sector

        ma_df_data = UtilsDataSector().read_sector_continous_days_ma(sector, config.continous_days, config.ma_days)
        data_minus = analyze_utils.calc_minus_yesterday(ma_df_data, 'market_value')
        
        result = AnalyzerSectorResult()
        result.config = config
        result.sector = sector
        
        ret_incr = analyze_utils.calc_inc_or_decr_continous_days_and_ratio(data_minus, "minus_yesterday", "market_value")
        if ret_incr["increase"] == True and ret_incr["days"]:
            result.trigger_increase_continous_days = True
            result.increase_continous_days = ret_incr["days"]
            result.increase_continous_ratio = ret_incr["ratio"]
        elif ret_incr["increase"] == False and ret_incr["days"]:
            result.trigger_decrease_continous_days = True
            result.decrease_continous_days = ret_incr["days"]
            result.decrease_continous_ratio = ret_incr["ratio"]
        
        data_minus.sort_values('market_value', ascending=False)
        result.df_data_order_by_market_value = data_minus
        
        self.res = result
        return self.res
        
    
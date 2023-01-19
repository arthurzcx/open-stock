# -*- coding=utf-8 -*-
'''
    实现日k线分析器
'''
from enum import Enum
from stock.getdata.parser_source import DataSourceType
import stock.getdata.tencent_parser as TencentParser
from stock.draw.plot_day import plot_dayk, plot_dayk_compare
from stock.analyzer.days_increase import AnalyzeDaysIncrease
from stock.analyzer.analyzer_average_continous import AnalyzerAverageContinous

class AnalyzerType(Enum):
    by_year = 0
    by_years = 1 

class AnalyzerMethod(Enum):
    '''
    分析方法，确定股票潜力的核心处理方法，每个方法对应一个类
    '''
    by_day_k = 0 #日k线
    by_days_increase = 1 #近日增长法
    by_days_decrease = 2 #近日下跌法
    by_average_continous = 3 #连续多日均线

class DaykAnalyzer:
    '''
    日k数据分析器
    '''

    stock_name = '' # 股票名称    
    stock_code = '' # 股票代码
    year = 2020 #日k数据按年
    years = (1996, 2020) #日k数据按年范围
    analyze_type = AnalyzerType.by_year #按年或多年分析
    soure_type = DataSourceType.from_tencent #定义数据源
    b_compare = False # 是否进行年度比较，仅当进行多年度数据分析时有效

    nanlyze_days_latest = 0 #按照最近天数分析，默认0时分析所有数据，当不为0时按照该值分析

    method = AnalyzerMethod.by_day_k # 分析方法

    # def __init__(self, name, code, year, years, analyze_t=AnalyzerType.by_year,soure_t=DataSourceType.from_tencent, nanlyze_days=0, method_analy=AnalyzerMethod.by_day_k):
    def __init__(self, **kwargs):
        '''
        构造函数
        :param name 股票名称，例如“万科A”
        :param code 股票代码，例如“sz000001"
        :param year 如果按照年度分析日k，则给定该值，例如2020
        :param years 如果按照多个年度分析日k,则给定该值，例如（1996,2020）
        :param analyze_t 按年或多年分析，AnalyzerType枚举类型
        :param soure_t 数据源，getdata.parser_source.DataSourceType枚举类型
        :param nanlyze_days 按照最近天数分析，默认0时分析所有数据，当不为0时按照该值分析
        '''
        for (key, value) in kwargs.items():
            if key == "stock_name":
                self.stock_name = value
            elif key == "stock_code":
                self.stock_code = value
            elif key == "year":
                self.year = value
            elif key == "years":
                self.years = value
            elif key == "analyze_type":
                self.analyze_type = value
            elif key == "soure_type":
                self.soure_type = value
            elif key == "nanlyze_days_latest":
                self.nanlyze_days_latest = value                
            elif key == "method":
                self.method = value

        self.b_compare = False
    
    def __get_data_one_year__(self):
        '''
        获取某一年的数据
        '''
        year_suffix = int(str(self.year)[2:])
        if self.soure_type == DataSourceType.from_tencent:
            return TencentParser.getData(self.stock_code, TencentParser.PeriodChoices.days_by_year, year=year_suffix, just_days_lates=self.nanlyze_days_latest)

    def __get_data_years__(self):
        '''
        获取多年数据
        :return 不进行年度比较时，返回数据为[[x1,x2,...],[y1,y2,...]]多年数据聚合在一起的一个列表；进行年度比较时，返回的时每个年度数据一起组合的列表
        [[[x1,x2,...],[y1,y2,...]],[],...]
        '''
        years = []
        
        for y in range(self.years[0], self.years[1] + 1):
            print(y)
            years.append(int(str(y)[2:]))
        
        if self.b_compare == False:
            x_data = []
            y_data = []

            for y in years:
                ydata = TencentParser.getData(self.stock_code, TencentParser.PeriodChoices.days_by_year, year=y)
                for d in ydata[0]:
                    x_data.append(d)            
                for d in ydata[1]:
                    y_data.append(d)
                        
            return [x_data, y_data]
        else:
            rdata = []
            list_years = []
            for y in years:
                x_data = []
                y_data = []
                ydata = TencentParser.getData(self.stock_code, TencentParser.PeriodChoices.days_by_year, year=y)
                for d in ydata[0]:
                    x_data.append(d)            
                for d in ydata[1]:
                    y_data.append(d)
                
                list_years.append(y)

                rdata.append([x_data, y_data])
                        
            return [rdata, list_years]

    def analyze(self):
        '''
        分析数据，绘图

        '''
        data = []
        if self.analyze_type == AnalyzerType.by_year:
            data = self.__get_data_one_year__()

            if self.method == AnalyzerMethod.by_day_k:
                plot_dayk(data, title_text=self.stock_name, xlabel=str(self.year) + "年日k线", ylabel=u"股价")
            elif self.method == AnalyzerMethod.by_days_increase:
               
                analyzer_by_increase = AnalyzeDaysIncrease(data[1])
                ret = analyzer_by_increase.analyze()
                
                if ret != None:
                    ret["name"] = self.stock_name
                    print(ret)
            elif self.method == AnalyzerMethod.by_average_continous:
                analyzer_averager =  AnalyzerAverageContinous(total_days=50)
                ret = analyzer_averager.analyze(data)
                if ret != None:
                    plot_dayk(ret, title_text=self.stock_name, xlabel=str(self.year) + "均值切片线", ylabel=u"股价")

        elif self.analyze_type == AnalyzerType.by_years:
            if self.b_compare == False:
                data = self.__get_data_years__()
                plot_dayk(data, title_text=self.stock_name, xlabel=u"日k线", ylabel=u"股价")
            else:
                data = self.__get_data_years__()
                plot_dayk_compare(data[0],data[1],title_text=u"年度日k比较", xlabel=u"时间", ylabel=u"股价")

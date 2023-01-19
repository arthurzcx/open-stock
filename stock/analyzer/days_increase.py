# -*- coding:utf-8 -*-
import os, json
from stock.analyzer.analyzer_utils import to_percent
from pandas import DataFrame as pd

class AnalyzeDaysIncrease:
    '''
    近期增长数据分析器
    '''
    increase_target = 0.2 #增长多少视为符合要求的股票
    increase_real = 0.0 # 实际涨幅

    day_rise_sharply = 0 #近期暴涨的天数
    day_rise_ratio_as_sharply = 0.05 #每日涨幅达到该值视为暴涨
    max_rise_ratio = 0.0 #最大涨幅值
    days_increase = 0 #近期上涨的天数

    day_fall_down_sharply = 0 #近期暴跌的天数
    day_fall_down_ratio_as_sharply = -0.05 #每日跌幅达到该值视为暴跌
    max_fall_down_ratio = 0.0 #最大跌幅值
    days_fall_down = 0 #近期下跌的天数

    days_least = 5 # 至少几天的数据才进入分析

    def __init__(self, target=0.2, ratio_as_sharply=0.05, fall_down_ratio_as_sharply=-0.05):
        '''
        近期增长数据分析器构造函数        
        :param target 增长多少视为符合要求的股票
        :param ratio_as_sharply每日涨幅达到该值视为暴涨
        :param fall_down_ratio_as_sharply每日跌幅达到该值视为暴跌
        '''
        self.increase_target = target
        self.day_rise_ratio_as_sharply = ratio_as_sharply
        self.day_fall_down_ratio_as_sharply = fall_down_ratio_as_sharply           

    def analyze(self, df):
        '''
        分析器执行函数
        :param df DataFrame格式数据，{'date':[], 'data':[]}
        '''
        data = df['data']
        print(data)
        
        if len(data) < self.days_least:
            return None
                                
        self.increase_real = (data[pd.last_valid_index] - data[pd.first_valid_index])/data[pd.first_valid_index]        

        print(self.increase_real)

        if self.increase_real <  self.increase_target:
            return None
    
                
        for i in range(len(data) - 2):
            ratio = (data[i+1] - data[i])/data[i]
            b_raise = (data[i+1] - data[i] > 0.0)
            b_fall_down = (data[i+1] - data[i] < 0.0)

            if b_raise == True :
                self.days_increase = self.days_increase + 1
            if b_fall_down == True:
                self.days_fall_down = self.days_fall_down + 1
            if ratio > self.day_rise_ratio_as_sharply:
                self.day_rise_sharply = self.day_rise_sharply + 1
            if ratio < self.day_fall_down_ratio_as_sharply:
                self.day_fall_down_sharply = self.day_fall_down_sharply + 1
            
            if ratio > self.max_rise_ratio:
                self.max_rise_ratio = ratio
            if ratio < self.max_fall_down_ratio:
                self.max_fall_down_ratio = ratio
            
        ret = {}
        ret["实际涨幅"] = to_percent(self.increase_real)
        ret["统计天数"] = self.days_sum
        ret["近期上涨的天数"] = self.days_increase
        ret["近期下跌的天数"] = self.days_fall_down
        ret["近期暴涨天数"] = self.day_rise_sharply
        ret["最大涨幅值"] = to_percent(self.max_rise_ratio)
        ret["近期暴跌的天数"] = self.day_fall_down_sharply
        ret["最大跌幅值"] = to_percent(self.max_fall_down_ratio)
        return ret

            




        

    
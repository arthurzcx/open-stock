# -*- coding:utf-8 -*-
'''
大盘指数分析器

Created on 2022年10月16日

@author: Arthur
@copyright: Jancy Co.,Ltd.
'''

from stock.analyzer.analyzer import Analyzer,AnalyzerConfig
from stock.data.reader import DataReader
import stock.common.html as Html
import stock.common.message as Message

class AnalyzerBroadCapIndex(Analyzer):
    '''
    大盘指数分析器类，实现大盘指数分析功能
    
    Attributes:
        
    '''
    def __init__(self, **kwargs):
        '''
        '''
        super(AnalyzerBroadCapIndex,self).__init__(**kwargs)
        self.dr = DataReader()
        
    def run(self):
        '''
        运行大盘指数分析策略
        '''
        Message.print_info("开始运行大盘指数分析器......")
        df_data = self.dr.read_broad_cap_index_latest()  
        df_data = df_data.rename(columns={"code":"代码", "name":"名称", "price":"点数", "gain_loss_ratio":"涨跌%","gain_loss":"涨跌点数", "total_market_cap":"总市值/亿元"})
        df_data = df_data.drop('time', axis='columns')
        
        self.res = {"index_data_table":df_data}
        Message.print_info("运行大盘指数分析器结束......")
        return self.res
    
    def result_to_html(self):
        '''
        将分析结果转换为html格式字符串
        '''
        html = ""
        
        # 大盘指数表格数据
        html += Html.convert_df_to_html_body(self.res["index_data_table"], title="大盘指数")
        
        return html
        


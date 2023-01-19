# -*- coding:utf-8 -*-
'''
所有板块数据分析器

Created on 2022年10月16日

@author: Arthur
@copyright: Jancy Co.,Ltd.
'''
from stock.analyzer.analyzer import Analyzer, AnalyzerConfig
from stock.analyzer.analyzer_sector import AnalyzerSector
from stock.data.reader import DataReader
import stock.common.message as Message
import stock.common.html as Html
import pandas

class AnalyzerSectorAll(Analyzer):
    '''
    所有板块数据分析器
    
    Attributes:
        
    '''
    def __init__(self, **kwargs):
        super(AnalyzerSectorAll,self).__init__(**kwargs)
        self.dr = DataReader()
    
    
    def run(self):
        '''
        运行分析器策略
        Created on 2022年10月16日
        
        Arguments:
            void
            
        Returns:
            void
        '''
        Message.print_info("开始运行所有板块数据分析器......")
        sectors = self.dr.read_all_section(with_complete_file_path=False)
        Message.print_info("已读取板块列表，板块数量：%d\n"%(len(sectors)))
        
        cols_incr = ["板块名称","连续天数", "累计上涨"]
        cols_decr = ["板块名称","连续天数", "累计下跌"]
        df_increase = pandas.DataFrame(columns=cols_incr)
        df_decrease = pandas.DataFrame(columns=cols_decr)
        
        counter = 0
        for sector in sectors:
            counter += 1
            Message.print_info("第%d个板块：%s"%(counter, sector))
        
            try:
                a_s = AnalyzerSector(config=self.config, sector=sector)
                a_s.run()
                result = a_s.result()
        
                if result.trigger_decrease_continous_days == True:
                    df_temp = pandas.DataFrame([[sector, result.decrease_continous_days, result.decrease_continous_ratio*100.0]], columns=cols_decr)
                    df_decrease = df_decrease.append(df_temp)
                if result.trigger_increase_continous_days == True:
                    df_temp = pandas.DataFrame([[sector, result.increase_continous_days, result.increase_continous_ratio*100.0]], columns=cols_incr)
                    df_increase = df_increase.append(df_temp)
            except Exception as e:
                print(e)
                Message.print_error("异常数据板块:  %s"%(sector))        
        
        print(df_increase)
        print(df_decrease)  
        df_increase = df_increase.sort_values(by="累计上涨", ascending=False)
        df_decrease = df_decrease.sort_values(by="累计下跌")
        
        self.res = {"df_increase":df_increase, "df_decrease":df_decrease}
        Message.print_info("所有板块数据分析器运行结束......")
        return self.res
    
    def result_to_html(self):
        '''
        获取HTML格式的分析器结果
        Created on 2022年10月15日
        
        Arguments:
            void
            
        Returns:
            HTML格式的分析器结果
        '''
        df_increase = self.res["df_increase"]
        df_decrease = self.res["df_decrease"]
        
        html = ""
        html += Html.convert_text_to_html_headline(text="板块涨跌数据分析", headlevel=2)
        if df_increase.shape[0] > 0:          
            html += Html.convert_df_to_html_body(df_increase, title="连续上涨板块")
        else:
            html += Html.convert_text_to_html_headline(text="今日无连续上涨板块", headlevel=3)
        
        html += Html.convert_text_to_p(text="")
        
        if df_decrease.shape[0] > 0:
            html += Html.convert_df_to_html_body(df_decrease, title="连续下跌板块")
        else:
            html += Html.convert_text_to_html_headline(text="今日无连续下跌板块", headlevel=3)
        
        return html
    
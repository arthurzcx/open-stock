# -*- coding:utf-8 -*-
'''
分析器的管理器

Created on 2022年10月16日

@author: Arthur
@copyright: Jancy Co.,Ltd.
'''

from stock.analyzer.analyzer import Analyzer, AnalyzerConfig
from stock.analyzer.analyzer_sector import AnalyzerSectorConfig
from stock.analyzer.analyzer_sector_all import AnalyzerSectorAll
from stock.analyzer.analyzer_broad_cap_index import AnalyzerBroadCapIndex
import stock.common.message as Message

class AnalyzerManagerConfig(AnalyzerConfig):
    '''
    分析器管理器的config类
    
    Attributes:
        analyzer_broad_cap_index_enabled: 使能大盘分析器的bool值
        analyzer_sector_all_enabled: 使能所有板块分析器的bool值
    '''
    def __init__(self, **kwargs):
        super(AnalyzerManagerConfig, self).__init__(**kwargs)
        
        self.name = "analyzer_manager"
        
        self.analyzer_broad_cap_index_enabled = True
        self.analyzer_sector_all_enabled = True
        
        if kwargs != None:
            if "analyzer_broad_cap_index_enabled" in kwargs.keys():
                self.analyzer_broad_cap_index_enabled = kwargs["analyzer_broad_cap_index_enabled"]
            if "analyzer_sector_all_enabled" in kwargs.keys():
                self.analyzer_sector_all_enabled = kwargs["analyzer_sector_all_enabled"]


class AnalyzerManager(Analyzer):
    '''
    分析器的管理器
    
    Attributes:
        
    '''
    def __init__(self, **kwargs):
        '''
        构造函数传入的config用于配置各个子分析器使能与参数
        Created on 2022年10月16日
        
        Arguments:
            analyzers: 子分析器列表
            
        Returns:
            AnalyzerManager类对象
        '''
        super(AnalyzerManager, self).__init__(**kwargs)
        
        self.analyzers = []
        
        # 大盘分析器
        config_broad_cap_index = AnalyzerConfig(enabled=self.config.analyzer_broad_cap_index_enabled)
        self.analyzer_broad_cap_index = AnalyzerBroadCapIndex(config=config_broad_cap_index)
        self.analyzers.append(self.analyzer_broad_cap_index)
        
        # 所有板块分析器
        config_sector_all = AnalyzerSectorConfig(enabled=self.config.analyzer_sector_all_enabled)
        self.analyzer_sector_all = AnalyzerSectorAll(config=config_sector_all)
        self.analyzers.append(self.analyzer_sector_all)
    
    def run(self):
        '''
        运行各个子分析器
        '''
        Message.print_info("分析器管理器开始运行，等待各子分析器运行完毕......")
        self.res = []
        for analyzer_item in self.analyzers:
            if not analyzer_item.config.enabled:
                continue
            analyzer_item.run()
            self.res.append(analyzer_item.result())
        Message.print_info("分析器管理器运行完毕......")
        return self.res
            
    def result(self):
        '''
        分析完成后所有的数据要存储到res变量中，通过该接口获取分析结果
        
        Returns:
            分析结果
        '''
        if self.res is None:
            Message.print_error("名字为%s的分析器没有产生任何分析结果！"%(self.name))
            
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
        html = ""
        for analyzer_item in self.analyzers:
            html += analyzer_item.result_to_html()
        return html
        
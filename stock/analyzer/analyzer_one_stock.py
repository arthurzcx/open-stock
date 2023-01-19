from stock.analyzer.analyzer import Analyzer,AnalyzerConfig
from stock.local.china.china_stocks import ChinaStocks
from stock.data.reader import DataReader
import stock.common.message as Message

'''
实现单个股票的分析器

Created on 2022年11月2日

@author: Arthur
@copyright: Jancy Co.,Ltd.
'''

class AnalyzerOneStockConfig(AnalyzerConfig):
    '''
    单个股票分析器的配置参数类
    
    Attributes:
        
    '''
    def __init__(self):
        pass

class AnalyzerOneStock(Analyzer):
    '''
    单个股票的分析类
    
    Attributes:
        stock 表示传入的股票名称或股票代码
    '''
    def __init__(self, **kwargs):
        super(AnalyzerOneStock,self).__init__(**kwargs)
        if 'stock' not in kwargs.keys():
            raise Exception("需要传入一个stock为key指定的股票代码或者股票名称， 类似stock: sh600***")
        self.stock = kwargs["stock"]
    
    def run(self):
        '''
        根据输入的配置参数和已知数据对单只股票进行分析
        Created on 2022年11月2日
        
        Arguments:
            void
            
        Returns:
            void
        '''
        config = self.config
        stock = ChinaStocks().get_st_by_info(self.stock)
        
        reader = DataReader()
        
        self.res = {}
        
        # 所属板块
        sectors = []
        
        self.res["sectors"] = sectors
        
        # 市值
        df_market_value_all = reader.read_market_value_latest()
        df_mv = df_market_value_all["code"==stock.code]
        self.res["market_value_df"] = df_mv
        
        # 近日连续涨跌分析
        

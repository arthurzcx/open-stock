# -*- coding:utf-8 -*-
from enum import Enum

class DataSourceType(Enum):
    '''
    定义数据来源的枚举值
    '''
    
    from_tencent = 0 #从腾讯获取数据
    from_yahoo = 1 #从雅虎获取数据
    from_sina = 2 #从新浪获取数据
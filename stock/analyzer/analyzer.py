# -*- coding:utf-8 -*-

'''
本文件封装Analyzer基类，用于分析类共有属性、功能和接口的实现，其它的analyzer类继承于该基类。
@author: Arthur Zhang
@contact: arthurzcx@163.com
@copyright: 
'''
import stock.common.message as Message 

class AnalyzerConfig:
    '''
    分析配置参数的基类，所有其它配置类继承该类并进行扩展
    
    Attributes:
        enabled: 是否使能该分析功能， 默认True
    '''

    def __init__(self, **kwargs):
        self.enabled = True
        
        if kwargs != None and "enabled" in kwargs.keys():
            self.enabled = kwargs["enabled"]

class Analyzer:
    '''
    分析基类，封装所有共有变量、功能和接口，其它所有分析类继承该类。
    
    Attributes:
        name: 分析器的名称
        config: 配置参数，AnalyzerConfig类或其子类的对象
        res: 分析结果
    '''
    def __init__(self,**kwargs):
        self.name = "analyzer"
        self.config = None
        self.res = None
        
        if kwargs is None:
            raise Exception("必须向Analyzer或其子类构造函数中传入合法参数!")

        if 'config' in kwargs.keys():
            self.config = kwargs['config']
        else:
            raise Exception("必须向Analyzer或其子类构造函数传入config参数!")
    
    def result(self):
        '''
        分析完成后所有的数据要存储到res变量中，通过该接口获取分析结果
        
        Returns:
            分析结果
        '''
        if self.res is None:
            Message.print_error("名字为%s的分析器没有产生任何分析结果！"%(self.name))
            
        return self.res
    
    def run(self):
        '''
        启动分析器开始进行分析，产生的结果需要通过分析器的result()接口获取
        Created on 2022年10月15日
        
        Arguments:
            void
            
        Returns:
            void
        '''
        pass
    
    def result_to_html(self):
        '''
        获取HTML格式的分析器结果
        Created on 2022年10月15日
        
        Arguments:
            void
            
        Returns:
            HTML格式的分析器结果
        '''
        return None



        
            
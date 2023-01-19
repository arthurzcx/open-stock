# !/usr/bin/python
# -*- encoding:utf-8 -*-

'''
Main entry.

Created on 2022年10月22日

@author: Arthur
@copyright: Jancy Co.,Ltd.
'''

import stock.common.message as Message
import stock.common.email as Email
import stock.common.html as Html

from stock.my.trade import Trade
from stock.my.favorites import Favorite

from stock.draw import dfplot
import stock.draw.utils as draw_utils

from stock.analyzer import analyze_utils,analyzer_sector
from stock.analyzer.analyzer_broad_cap_index import AnalyzerBroadCapIndex 
from stock.analyzer.analyzer_sector_all import AnalyzerSectorAll
from stock.analyzer.analyzer_manager import AnalyzerManager,AnalyzerManagerConfig
from stock.analyzer.analyzer import AnalyzerConfig
from stock.analyzer.analyzer_sector import AnalyzerSectorConfig

from stock.local.china.china_stocks import ChinaStocks
from stock.web.utils.data_update import UtilsUpdateData, thread_update_market_value,thread_update_broad_cap_index

import stock.data.reader as data_reader
from stock.data.utils_sector import test_read_sector_day,test_read_sector_continous_days,UtilsDataSector

from test.test_local.china import TestChina

import argparse, datetime, threading

# matplotlib is not thread safe, so we should use process to solve the issue
from multiprocessing import Process
from cmd import Cmd

class MainCmd(Cmd):
    '''
    主命令入口类
    
    Attributes:
        prompt 输入命令的提示符，位于行的头部
        udu 更新数据类UtilsUpdateData的对象
        cs A股类ChinaStocks的对象
        trade 股票买卖类Trade的对象
        favorite 关注股票类Favorite的对象
    '''

    def __init__(self):
        super(MainCmd, self).__init__()
        self.prompt = "->"
        self.udu = UtilsUpdateData()
        self.cs = ChinaStocks()
        self.trade = Trade()
        self.favorite = Favorite()

    def check_args(self, args, input_list):
        """ 
        检查并解析输入命令行参数
        
        Args:
        @args: 输入的命令行参数，以空格隔开，默认输入字符串 
        @input_list: 多个参数的名称形成的列表，以该列表中的字段为key，生成map类型返回值
        
        @return: 
        map 类型的参数对象      
        
        举例：
        args:  sz600001  3
        input_list:  ["stock_code", "years"]
        返回值为{"stock_code": sz600001, "years":3}  
        """
        args = args.strip().split()
        if len(args) != len(input_list):
            Message.print_warning("请输入 %d 个 与该名称匹配的参数: [%s]" % (
                len(input_list), ", ".join(input_list)))
            Message.print_warning("如果存在默认参数，将以默认参数执行")
            return None
        else:
            ret_args = {}
            for i in range(0, len(args)):
                ret_args[input_list[i]] = args[i]
            return ret_args

    def do_draw_one_stock_today(self, st_code_or_name):
        """ 
        Draw today data of one stock.        
        Arguments:
            args: an exact stock code or name, fo example: sh600004
        """
        try:
            p = Process(target=draw_utils.draw_one_stock_today,
                        args=(st_code_or_name,))
            p.start()
        except Exception as e:
            Message.print_warning(str(e))
            return

    def do_draw_one_stock_history(self, st_code_or_name):
        """ 
        draw history data of one stock.
        Arguments:
            args: an exact stock code or name, for example: sh600004  
        """
        try:
            p = Process(target=draw_utils.draw_one_stock_history,
                        args=(st_code_or_name,))
            p.start()
        except Exception as e:
            Message.print_warning(e)

    def do_draw_candle(self, st_code_or_name):
        """ 
        draw history data candle.
        Arguments:
            args: an exact stock code or name, for example: sh600004  
        """
        try:
            p = Process(target=draw_utils.draw_candle,
                        args=(st_code_or_name,))
            p.start()
        except Exception as e:
            Message.print_warning(e)        

    def do_update_history(self, years):
        """ 
        Update history data of all stocks, just run one time when you need histroy data.
        The process will cost serval minutes, because of the large data.
        See the data files in directory: data/history
        Arguments:
            years: years of histroy data, for example: update_histroy  3 
        """
        try:
            uud = UtilsUpdateData()
            p = Process(target=uud.update_history, args=(years,))
            p.start()
        except Exception as e:
            Message.print_warning(e)

    def do_find_a_stock(self, st_code_or_name):
        """         
        Find the exact code and name of your input incomplete code or name.        
        For example: if you type "004",  the function will search "004" in all stocks' code and name. Then print them.
        """
        try:
            p = Process(target=self.cs.find_a_stock, args=(st_code_or_name,))
            p.start()
            p.join()
        except Exception as e:
            Message.print_warning(e)

    def do_buy(self, line):
        """ Buy a stock.
        Args:
            stock_code_or_name:  the code or name of the stock bought.
            quantity: the numer of this trade.
            price: the price of the stock bought.         
        """
        try:
            args = self.check_args(
                line, ['st_code_or_name', 'quantity', 'price'])
            stock = self.cs.get_st_by_info(st_code_or_name=args["st_code_or_name"])
            self.trade.buy(stock, quantity=args["quantity"], price_value=args["price"])
            Message.print_info("The trade has done!")
        except Exception as e:
            Message.print_warning(e)

    def do_sell(self, line):
        """ Sell a stock.
        Args:
            stock_code_or_name:  the code or name of the stock bought.
            quantity: the numer of this trade.
            price: the price of the stock bought.         
        """
        try:
            args = self.check_args(
                line, ['st_code_or_name', 'quantity', 'price'])
            stock = self.cs.get_st_by_info(st_code_or_name=args['st_code_or_name'])
            self.trade.sell(stock, quantity=args["quantity"], price_value=args["price"])
            Message.print_info("The trade has done!")
        except Exception as e:
            Message.print_warning(e)

    def do_my_positions(self, args):
        """ List all my positions.
        """
        try:
            self.trade.my_positions()
        except Exception as e:
            Message.print_warning(e)

    def do_add_favorite(self, args):
        """ Add a stock to favorite.
        """
        stock = self.cs.find_a_stock(args)
        if stock is not None and len(stock) > 0:
            self.favorite.add_favorite(stock[0])
    
    def do_remove_favorite(self, args):
        """ Remove a stock from favorites.
        """
        stock = self.cs.find_a_stock(args)
        if stock is not None and len(stock) > 0:
            self.favorite.remove_favorite(stock[0])
    
    def do_test_read_broad_cap_index_latest(self,args):
        '''
        测试读取最新的大盘指数数据文件
        '''
        print(data_reader.DataReader().read_broad_cap_index_latest())
        
    def do_test_all_section_list(self,args):
        '''
        测试读取所有板块的名称列表
        '''
        test_china = TestChina()
        test_china.test_read_all_section_list()
    
    def do_test_read_one_section(self, args):
        '''
        测试读取某一个板块的数据
        '''
        test_china = TestChina()
        test_china.test_read_on_section()
    
    def do_test_create_market_value_data_from_history(self,args):
        '''
        测试从当前市值文件和历史数据文件虚假的制造出用于测试的市值文件
        '''
        test_china = TestChina()
        test_china.create_market_value_data_from_history()
    
    def do_test_read_sector_day(self, args):
        """
        读取某日、某行业板块的总市值
        """
        test_read_sector_day(sector="高铁", dtime=datetime.datetime.strptime("2022-09-16", "%Y-%m-%d"))
    
    def do_test_read_sector_continous_days(self, args):
        '''
        测试某行业板块连续多日的市值数据，从当前日期向前推
        '''
        test_read_sector_continous_days(sector="高铁", days=30)
    
    def do_test_draw_sector_continous_days(self, args):
        '''
        测试绘制某行业板块连续多日的市值数据，从当前日期往前推
        '''         
        sector = "高铁"
        days = 30  
        if len(args) > 0:
            ret_args = self.check_args(args, ['sector','days'])
            if ret_args != None:
                sector = ret_args['sector']
                days = int(ret_args['days'])
        df_data = UtilsDataSector().read_sector_continous_days(sector=sector, days=days)
        dfplot.DfPlot().draw_common_data("date", "market_value", df_data, "%s板块市值"%(sector))
    
    def do_test_read_sector_continous_days_ma(self, args):
        '''
        测试绘制某个板块的移动平均线，7日MA
        '''
        sector = "高铁"
        days = 30  
        ma_days = 7 
        if len(args) > 0:
            ret_args = self.check_args(args, ['sector','days'])
            if ret_args != None:
                sector = ret_args['sector']
                days = int(ret_args['days'])
        df_data = UtilsDataSector().read_sector_continous_days_ma(sector=sector, days=days,ma_days=ma_days)
        dfplot.DfPlot().draw_common_data("date", "market_value", df_data, "%s板块市值%s日移动均线"%(sector,str(days)))
    
    def do_test_calc_minus_yesterday(self, args):
        '''
        测试计算求连续多日  当日与前一天的数据差
        这里使用板块数据进行测试
        
        Arguments:
            args 板块名称
        '''
        sector = "云办公"
        days = 30  
        ma_days = 7 
        if len(args) > 0:
            ret_args = self.check_args(args, ['sector'])
            if ret_args != None:
                sector = ret_args['sector']
        df_data = UtilsDataSector().read_sector_continous_days_ma(sector=sector, days=days,ma_days=ma_days)
        data_minus = analyze_utils.calc_minus_yesterday(df_data, 'market_value')
        Message.print_info("%s板块连续%d日移动平均差值数据:"%(sector,ma_days))
        print(data_minus)
    
    def do_test_sector_analyzer(self,args):
        '''
        测试对板块数据的连续涨跌进行分析
        
        Arguments:
            args 板块名称
        '''
        sector = "半导体元件"
        if len(args) > 0:
            ret_args = self.check_args(args, ['sector'])
            if ret_args != None:
                sector = ret_args['sector']
        
        config = analyzer_sector.AnalyzerSectorConfig()
        a_s = analyzer_sector.AnalyzerSector(config=config, sector=sector)
        a_s.run()
        result = a_s.result()
        
        if result.trigger_decrease_continous_days == True:
            print("%s 板块连续下跌，下跌天数 %d, 累计下跌 %.2f%%\n"%(sector,result.decrease_continous_days,result.decrease_continous_ratio*100.0))
        if result.trigger_increase_continous_days == True:
            print("%s 板块连续上涨，上涨天数 %d, 累计上涨 %.2f%%\n"%(sector,result.increase_continous_days,result.increase_continous_ratio*100.0))
    
    def do_test_all_sectors(self, args):
        '''
        分析所有的板块数据，找出连续增长的股票
        '''
        analyzer = AnalyzerSectorAll(config=AnalyzerSectorConfig())
        analyzer.run()
        html = Html.assembel_html(analyzer.result_to_html())
        
        Email.send_default_email(content_html=html, subject="板块涨跌分析")
    
    def do_test_broad_cap_index_analyze(self,args):
        '''
        大盘指数分析，以邮件方式通知
        '''
        analyzer = AnalyzerBroadCapIndex(config=AnalyzerConfig())
        analyzer.run()
        html = Html.assembel_html(analyzer.result_to_html())
        
        Email.send_default_email(content_html=html, subject="大盘指数")
    
    def do_analyzer_manager(self, args):
        '''
        运行分析器管理器
        '''
        am = AnalyzerManager(config=AnalyzerManagerConfig())
        am.run()
        html_body = am.result_to_html()
        html = Html.assembel_html(html_body)
        Email.send_default_email(content_html=html, subject="A股分析")
    
    def do_exit(self, args):
        """ 
        Exit the main process, just type in: exit. 
        The process will close serval child threads or childs process, so you should wait serval minutes.
        """
        self.udu.exit_update()
        exit(0)

def print_app_info():
    from stock.common.appinfo import AppInfo
    app_info = AppInfo()
    Message.print_msg_list(msg_list=app_info.info_list, color=Message.Color.yellow, style=Message.Style.highlight,
                   alignment=Message.Alignment.center, align_width=app_info.msg_max_width)

if __name__ == "__main__":
    print_app_info()

    parser = argparse.ArgumentParser(
        description="The main entry to enjoy your stock trip......")
    parser.add_argument("--update_current", "-c", action="store_true",
                        help="update current stock data from web")
    parser.add_argument("--update_history", "-u",
                        action='store_true', help="update history data from web")

    parser.add_argument("--test_stocks_counter", "-n", action="store_true",
                        help="test counter of stocks in China stocks market")

    parser.add_argument("--test_read_dataframe_data", "-d", action="store_true",
                        help="test to read xls data, converted to DataFrame type data")

    parser.add_argument("--test_plot_df_on_stock_history", "-p", action="store_true",
                        help="test to draw one stock history data in DataFrame type")

    args = parser.parse_args()
    if args.update_current:
        UtilsUpdateData().update_current()
    elif args.update_history:
        UtilsUpdateData().update_history()
    elif args.test_stocks_counter:
        TestChina().test_counter_stocks()
    elif args.test_read_dataframe_data:
        data_reader.test_read_to_dataframe_type_data()
    elif args.test_plot_df_on_stock_history:
        dfplot.test_draw_one_stock_history()

    else:
        print("Main cmd loop starts ......")
        mc = MainCmd()
        
        ##################################################################
        # 配置
        enable_update_realtime = False # 是否使能实时数据更新
        enable_update_market_value = True # 是否使能更新每日市值数据
        enable_update_broad_cap_index = True # 是否使能更新每日大盘指数数据
        
        
        ##################################################################
        
        ## 每日实时数据更新线程，按照设定秒数更新一次所有股票实时数据
        if enable_update_realtime is True:
            Message.print_info(
                "更新当日实时数据的线程已经启动...")
            seconds_update_today = 300 # 更新实时数据的间隔时间，单位秒
            tud = threading.Thread(target=mc.udu.update_today, args=(seconds_update_today,))
            tud.start()
        else:
            Message.print_warning(
                "已禁止更新每日实时数据!")
        
        ## 每日更新市值数据，这是进行行业板块分析的基础数据，必须做
        if enable_update_market_value is True:
            Message.print_info(
                "更新市值的线程已经启动...")
            hour_trigger_update_market_vaule = 9 # 触发更新市值数据的时间，17表示下午5点
            t = threading.Thread(target=thread_update_market_value, args=(hour_trigger_update_market_vaule,))
            t.start()
        else:
            Message.print_warning(
                "已禁止更新每日市值数据!")
        
        ## 每日更新大盘指数数据，这是所有分析可能要依据的基础数据，必须做
        if enable_update_broad_cap_index  is True:
            Message.print_info(
                "更新当日大盘指数数据的线程已经启动...")
            hour_trigger_update_broad_cap_index = 9 # 触发更新大盘指数数据的时间
            t = threading.Thread(target=thread_update_broad_cap_index, args=(hour_trigger_update_broad_cap_index,))
            t.start()
        else:
            Message.print_warning(
                "已禁止更新每日大盘指数数据!")
        
        ##################################################################
        Message.print_info("Please type in 'help' to list all commands supported.")
        mc.cmdloop(intro="Welcom to  stock simulator! Earning money!!!")

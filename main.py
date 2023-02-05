# !/usr/bin/python
# -*- encoding:utf-8 -*-

"""
Main Entry.

Created on 2023-02-05

@author: Arthur
@copyright: Jancy Co.,Ltd. 2023-2033

"""

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
    Main entry class.
    
    Attributes:
    ----------
        prompt: string. 
            Command prompt ->.
        udu: 
            UtilsUpdateObject data class object.
        cs: 
            Chinese stock (A-share) class object (ChinaStocks).
        trade: 
            Trade class object.
        favorite: 
            Favorite class object for user favorite stocks.
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
        Check and parse command arguments that user inputs.
        
        Parameters:
        -----------
        args: string
            The command arguments that user input, seperated by space, and the default format is string. 
        input_list: List
            A list for name of input arguments, which element as the key of  return Map.
        
        Returns:
        ---------- 
        A map with keys from "input_list" and values from "args".     
        
        For example:
        ----------
        args:  
            sz600001  3
        input_list:  
            ["stock_code", "years"]
        Return value is {"stock_code": sz600001, "years":3}.  
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
        Draw today's data of a stock.
        
        Parameters:
        ---------------
        st_code_or_name: string
            The code or name of a stock.
        
        Returns:
        --------------
        NoneType.
        
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
        Draw history data of one stock.
        
        Parameters:
        ---------------
        st_code_or_name: string
            The code or name of one stock.
        
        Returns:
        --------------
        NoneType.
        """
        try:
            p = Process(target=draw_utils.draw_one_stock_history,
                        args=(st_code_or_name,))
            p.start()
        except Exception as e:
            Message.print_warning(e)

    def do_draw_candle(self, st_code_or_name):
        """
        Draw history data candle figure of one stock.
        
        Parameters:
        ---------------
        st_code_or_name: string
            The code or name of one stock.
        
        Returns:
        --------------
        NoneType.
        """
        try:
            p = Process(target=draw_utils.draw_candle,
                        args=(st_code_or_name,))
            p.start()
        except Exception as e:
            Message.print_warning(e)        

    def do_update_history(self, years):
        """
        Update history data of all stocks, and run one time when you need history data.
        The function will call a process, and this will cost several minutes, depends on the quantity of data.
        The data will be stored in directory: data/history.
        
        Parameters:
        ---------------
        years: int
            Years of history data.
        
        Returns:
        --------------
        NoneType.
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
        For example: if you type "004",  the function will search "004" in all stocks' code and name.
        Then print a list of them.
        
        Parameters:
        ---------------
        st_code_or_name: string
            The incomplete code or name of one stock.
        
        Returns:
        --------------
        NoneType.
        """        
        try:
            p = Process(target=self.cs.find_a_stock, args=(st_code_or_name,))
            p.start()
            p.join()
        except Exception as e:
            Message.print_warning(e)

    def do_buy(self, input_args):
        """
        Buy a stock.
        
        Parameters:
        ---------------
        input_args: string
            The arguments that contains "st_code_or_name", "quantity" and "price".
            "st_code_or_name" means the code or name of the stock that you want to buy.
            "quantity" means the quantity of stock that you want to buy.
            "price" means the price of stock that you want to buy.
            
        Returns:
        --------------
        NoneType.
        """
        try:
            args = self.check_args(
                input_args, ['st_code_or_name', 'quantity', 'price'])
            stock = self.cs.get_st_by_info(st_code_or_name=args["st_code_or_name"])
            self.trade.buy(stock, quantity=args["quantity"], price_value=args["price"])
            Message.print_info("The trade has done!")
        except Exception as e:
            Message.print_warning(e)

    def do_sell(self, input_args):
        """ 
        Sell a stock.
        
        Parameters:
        ---------------
        input_args: string
            The arguments that contains "st_code_or_name", "quantity" and "price".
            "st_code_or_name" means the code or name of the stock that you want to sell.
            "quantity" means the quantity of stock that you want to sell.
            "price" means the price of stock that you want to sell.  
                        
        Returns:
        --------------
        NoneType.    
        """
        try:
            args = self.check_args(
                input_args, ['st_code_or_name', 'quantity', 'price'])
            stock = self.cs.get_st_by_info(st_code_or_name=args['st_code_or_name'])
            self.trade.sell(stock, quantity=args["quantity"], price_value=args["price"])
            Message.print_info("The trade has done!")
        except Exception as e:
            Message.print_warning(e)

    def do_my_positions(self, args):
        """
        List all my positions.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        try:
            self.trade.my_positions()
        except Exception as e:
            Message.print_warning(e)

    def do_add_favorite(self, args):
        """
        Add one stock to your favorites.
        
        Parameters:
        ---------------
        args: string
            The code or name of the stock that you want to add to your favorites.
        
        Returns:
        --------------
        NoneType.
        """
        stock = self.cs.find_a_stock(args)
        if stock is not None and len(stock) > 0:
            self.favorite.add_favorite(stock[0])
    
    def do_remove_favorite(self, args):
        """
        Remove one stock from your favorites.
        
        Parameters:
        ---------------
        args: string
            The code or name of the stock that you want to remove from you favorites.
        
        Returns:
        --------------
        NoneType.
        """
        stock = self.cs.find_a_stock(args)
        if stock is not None and len(stock) > 0:
            self.favorite.remove_favorite(stock[0])
    
    def do_read_broad_cap_index_latest(self,args):
        """
        Read latest broad cap index data.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        print(data_reader.DataReader().read_broad_cap_index_latest())
        
    def do_all_section_list(self,args):
        """
        Test for all section list, and print them.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        test_china = TestChina()
        test_china.test_read_all_section_list()
    
    def do_read_one_section(self, args):
        """
        Test to read data of a section.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        test_china = TestChina()
        test_china.test_read_on_section()
    
    def do_create_market_value_data_from_history(self,args):
        """
        Create market value data form history data.
        Please notice: the created data maybe not inaccurate.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        test_china = TestChina()
        test_china.create_market_value_data_from_history()
    
    def do_read_sector_day(self, args):
        """
        Test reading data of a certain section on a certain day.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        test_read_sector_day(sector="高铁", dtime=datetime.datetime.strptime("2022-09-16", "%Y-%m-%d"))
    
    def do_read_sector_continous_days(self, args):
        """
        Test reading market value data of a sector for several continous days, 
        and the date pushed forward from current date.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        test_read_sector_continous_days(sector="高铁", days=30)
    
    def do_draw_sector_continous_days(self, args):
        """
        Test drawing market value data of a certain sector for several continous days,
        and the date pushed forward from the current date.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """         
        sector = "高铁"
        days = 30  
        if len(args) > 0:
            ret_args = self.check_args(args, ['sector','days'])
            if ret_args != None:
                sector = ret_args['sector']
                days = int(ret_args['days'])
        df_data = UtilsDataSector().read_sector_continous_days(sector=sector, days=days)
        dfplot.DfPlot().draw_common_data("date", "market_value", df_data, "%s板块市值"%(sector))
    
    def do_read_sector_continous_days_ma(self, args):
        """
        Test reading the moving average of a certain sector data.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
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
    
    def do_calc_minus_yesterday(self, args):
        """
        Test and calculate the data difference between the current day and the previous day 
        for several consecutive days.
        Here, we use sector data for testing
        
        Parameters:
        ---------------
        args: string
            Should be a name of a certain sector in sector list.
        
        Returns:
        --------------
        NoneType.
        """
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
        """
        Test analyzing the continuous rise and fall of sectors data.
        
        Parameters:
        ---------------
        args: string
            Must be a sector name from sectors list.
        
        Returns:
        --------------
        NoneType.
        """
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
        """
        Analyze all sector data to find stocks with continuous growth.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        analyzer = AnalyzerSectorAll(config=AnalyzerSectorConfig())
        analyzer.run()
        html = Html.assembel_html(analyzer.result_to_html())
        
        Email.send_default_email(content_html=html, subject="板块涨跌分析")
    
    def do_broad_cap_index_analyze(self,args):
        """
        Analysis of market index and notification by email.
        
        Parameters:
        ---------------
        args: string
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        analyzer = AnalyzerBroadCapIndex(config=AnalyzerConfig())
        analyzer.run()
        html = Html.assembel_html(analyzer.result_to_html())
        
        Email.send_default_email(content_html=html, subject="大盘指数")
    
    def do_analyzer_manager(self, args):
        """
        Run analyzer manager.
        
        Parameters:
        ---------------
        args: string.
            Should be empty.
        
        Returns:
        --------------
        NoneType.
        """
        am = AnalyzerManager(config=AnalyzerManagerConfig())
        am.run()
        html_body = am.result_to_html()
        html = Html.assembel_html(html_body)
        Email.send_default_email(content_html=html, subject="A股分析")
    
    def do_exit(self, args):
        """ 
        Exit the main process, just type in: exit. 
        The process will close several child threads or child processes, so maybe you should wait several minutes.
        """
        self.udu.exit_update()
        exit(0)

def print_app_info():
    """
    Print information of this application.
    """
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
        print("Main command loop starts ......")
        mc = MainCmd()
        
        ##################################################################
        """
            Config parameters
        """
        enable_update_realtime = False # Enable real-time data updating or not
        enable_update_market_value = True # Enable daily market value data updating or not
        enable_update_broad_cap_index = True # Enable daily broad index updating or not
        
        
        ##################################################################
        
        """
            The daily real-time data updating thread updates the real-time data of all stocks 
            once according to the set number of seconds
        """
        if enable_update_realtime is True:
            Message.print_info(
                "The thread for updating the real-time data of the current day has started...")
            seconds_update_today = 300 # 更新实时数据的间隔时间，单位秒
            tud = threading.Thread(target=mc.udu.update_today, args=(seconds_update_today,))
            tud.start()
        else:
            Message.print_warning(
                "Updating of daily real-time data has been disabled! Please config enable_update_realtime = True to enable.")
        
        """
            Update market value data every day, which is the basic data for sector analysis.
        """
        if enable_update_market_value is True:
            Message.print_info(
                "The thread to update the market value has started...")
            hour_trigger_update_market_vaule = 9 # 触发更新市值数据的时间，17表示下午5点
            t = threading.Thread(target=thread_update_market_value, args=(hour_trigger_update_market_vaule,))
            t.start()
        else:
            Message.print_warning(
                "Update of daily market value data is disabled! Please config enable_update_market_value = True to enable.")
        
        ## 每日更新大盘指数数据，这是所有分析可能要依据的基础数据，必须做
        if enable_update_broad_cap_index  is True:
            Message.print_info(
                "The thread for updating the market index data of the current day has started...")
            hour_trigger_update_broad_cap_index = 9 # 触发更新大盘指数数据的时间
            t = threading.Thread(target=thread_update_broad_cap_index, args=(hour_trigger_update_broad_cap_index,))
            t.start()
        else:
            Message.print_warning(
                "Update of daily market index data is disable! Please config enable_update_broad_cap_index = True to enable.")
        
        ##################################################################
        Message.print_info("Please type in 'help' to list all commands supported.")
        mc.cmdloop(intro="Welcome to  stock simulator! Earning money!!!")

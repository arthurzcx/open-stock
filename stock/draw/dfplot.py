# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/28
# @version 1.0
# @desc: Use plot libs to plot DataFrame data .

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.axes as axes
import seaborn as sns
import mplfinance as mpf
import sys
import pandas as pd

# Show Chinese Characters, you should install Chinese TrueType Font into specified directory
plt.rcParams['font.sans-serif'] = ['SimHei', 'URW Palladio L',
                                   'Manjari Bold']

# Show normal minuse simbol
plt.rcParams['axes.unicode_minus'] = False

# sns.set_context("talk")
# sns.set_palette("muted")

class DfPlot():
    def __init__(self):
        pass

    def draw_one_stock_history(self, df, stock):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("function %s(): the 'df' parameter must be a pandas.DataFrame object!" % (
                sys._getframe().f_code.co_name))
        print(df.columns)
        df.plot(x='date', y='close', style="--")
        
        plt.xlabel("date")
        plt.ylabel("price")
        plt.title(u"%s %s" % (stock.code, stock.name))
        plt.show()

    def draw_one_stock_today(self, df, stock):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("function %s(): the 'df' parameter must be a pandas.DataFrame object!" % (
                sys._getframe().f_code.co_name))
        df.plot(x='time', y='price', style="--")
        
        plt.xlabel("time")
        plt.ylabel("price")
        plt.title(u"%s %s" % (stock.code, stock.name))
        plt.show()

    def draw_candle_history(self,df, stock):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("function %s(): the 'df' parameter must be a pandas.DataFrame object!" % (
                sys._getframe().f_code.co_name))
                
        df.rename(columns={'date':'DateTime'}, inplace=True)
        df.set_index(['DateTime'], inplace=True)
        
        mpf.plot(df.iloc[-100:, :], 
        type="candle", 
        title=stock.code + " "+stock.name, 
        ylabel="price(RMB)", 
        style='binance',
        # volume=True,
        # ylabel_lower="volume(shares)"
        )
    
    def draw_common_data(self, x_column, y_column, df_data, title):
        '''
        通用的二维数据绘制接口函数
        
        Args:
        @x_column: x坐标轴对应df_data中的数据列名称
        @y_column: y坐标对应df_data中的数据列名称
        @df_data: DataFrame类型数据
        @title: 绘图标题
        '''
        if not isinstance(df_data, pd.DataFrame):
            raise ValueError("function %s(): 参数df_data必须是pandas.DataFrame格式数据!" % (
                sys._getframe().f_code.co_name))
        df_data.plot(x=x_column, y=y_column, style="--")
        
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(u"%s" % (title))
        plt.show()
    
    
def test_draw_one_stock_history():
    print("==============================================================")
    print("Testing draw_one_stock_history......")
    from data.reader import DataReader
    from local.china.china_stocks import ChinaStocks
    stock = ChinaStocks().stocks_a()[-1]
    data = DataReader().read_history(stock)
    dfp = DfPlot()
    dfp.draw_one_stock_history(data, stock)
    print("Finished testing draw_one_stock_history......")
    print("==============================================================")

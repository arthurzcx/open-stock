# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/03/30
# @version 1.0
# @desc: Implemet my stock positions trade.

import os, sys
import pandas as pd
from pandas import DataFrame
from datetime import datetime

from stock.common.stock import Stock
from stock.common.price import Price
from stock.common.message import print_info, print_warning, print_error, Message, center_msg, Color, Style

from stock.data.reader import DataReader

class Trade():
    """ A class to implement my stock position trade.
    
        The class describe a trade: a stock bought price(value, datetime) and sold(value, datetime), earn or loss.
    """

    def __init__(self):
        self.position_path = os.path.join(os.getcwd(), 'my', 'positions')

    def buy(self, stock, quantity, price_value):
        """  Buy the stock.        
        Args:
            stock: the sotck bought
            quantity: the quantity of stocks bought.
            price_value: the price value when bought.
        """
        self.__trade(stock, quantity, price_value, True)

    def sell(self, stock, quantity, price_value):
        """  Sell the stock.        
        Args:
            stock: the sotck sold
            quantity: the quantity of stocks sold.
            price_value: the price value when sold.
        """
        self.__trade(stock, quantity, price_value, False)

    def __trade(self, stock, quantity, price_value, trade=True):
        """  Sell the stock.        
        Args:
            stock: the sotck sold
            quantity: the quantity of stocks sold.
            price_value: the price value when sold.
            trade: buy True, sell False
        """
        q = abs(int(quantity))
        if not trade:
            q *= -1

        dtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = os.path.join(self.position_path, stock.code + ".xls")
        df = DataFrame(columns=('dtime', 'code', 'name', 'quantity', 'price'))
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        df = df.append(DataFrame({'dtime':dtime, 'code':stock.code, 'name':stock.name, 'quantity':q, "price":price_value}, index=[0]))
        sum_quantity = df['quantity'].sum()
        if not trade and sum_quantity <= 0 and os.path.exists(file_path):
            os.remove(file_path)
            print_warning("The stock %s(%s) has been sold out..."%(stock.code, stock.name))
        else:
            df.to_excel(file_path, index=False)
            
    def my_positions(self):
        """ List all positions now.     
        """
        filelist = os.listdir(self.position_path)
        total_money = 0
        total_earn = 0

        align_msg_len = 16
        columns = ["name",  "code",  "quantity",  "current_price",  'today_ratio', "earn_or_loss"]
        data_return ={'name':[], 'code':[], "quantity":[],  "current_price":[],  'today_ratio':[], "earn_or_loss":[]}
        msg = center_msg(columns, align_msg_len)
        Message(Color.yellow, Style.highlight).local_print(" ".join(msg))
        counter = 0 
        for filename in filelist:
            if filename.startswith("."):
                continue
            if filename.endswith(".xls"):
                df = pd.read_excel(os.path.join(self.position_path, filename))
                sum_quantity = df['quantity'].sum()
                latest_info = DataReader().lates_price(Stock(df.at[0,'code'], df.at[0,'name']))                
                current_price = latest_info['price']
                df['trade_money'] = df['quantity']*df['price']
                earn_or_loss = df['quantity'].sum()*current_price - df['trade_money'].sum()
                total_earn = total_earn + earn_or_loss
                
                msg = [df.at[0,'code'], df.at[0, 'name'], "%d"%(sum_quantity), "%.2f%%"%(latest_info['gain_loss_ratio']), "%.2f"%(current_price), "%.2f"%(earn_or_loss)]
                msg = center_msg(msg, align_msg_len)
                Message(Color.blue, Style.default).local_print(" ".join(msg))

                total_money = total_money + df['quantity'].sum()*current_price
                counter = counter + 1
                
                data_return['code'].append(df.at[0,'code'])
                data_return['name'].append(df.at[0,'name'])
                data_return['quantity'].append(sum_quantity)
                data_return['current_price'].append(current_price)
                data_return['today_ratio'].append(latest_info['gain_loss_ratio'])
                data_return['earn_or_loss'].append(earn_or_loss)

        print_info("total_money: %.2f"%(total_money))
        print_info("total_earn: %.2f"%(total_earn))

        return {'df': DataFrame(data=data_return, columns=columns), 'total_money':total_money, 'total_earn':total_earn}
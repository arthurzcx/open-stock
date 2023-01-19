# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/09
# @version 1.0
# @desc: Manage you favorite stocks.

import os, sys, json

from stock.common.stock import Stock
from stock.common.message import print_info

class Favorite():
    """ Manage you favorite stocks.
    
    Attributes:
        favorites_stocks:  a list of favorites stocks (Stock class object).
        b: 
    """
    def __init__(self):
        self.favorite_dir =  os.path.join(os.getcwd(), 'my', 'favorites')
        self.favorite_path = os.path.join(self.favorite_dir, 'favorites.json')

        if not os.path.exists(self.favorite_dir):
            os.makedirs(self.favorite_dir)
        
        self._read_favorites_()
        
    def _read_favorites_(self):
        self.favorites_stocks = []
        if os.path.exists(self.favorite_path):
            with open(self.favorite_path, 'rt', encoding='utf-8') as f:
                favorites =  json.load(f)
                f.close()
                if len(favorites) < 1:
                    return
                for item in favorites.items():
                    self.favorites_stocks.append(Stock(item[0], item[1]))

    def add_favorite(self, stock):
        """ Add a stock to favorite json.        
        """
        self.favorites_stocks.append(stock)

        content = {}
        for st in self.favorites_stocks:            
            content[st.code] = st.name

        with open(self.favorite_path, "wt", encoding='utf-8') as f:
            js = json.dumps(content, ensure_ascii=False, indent=4)
            f.write(js)
            f.close()
        print_info("add stock(%s, %s) into favorites."%(stock.code, stock.name))
    
    def remove_favorite(self, stock):
        """ Remove a stock from favorite json.
        """
        for st in self.favorites_stocks:
            if st.code == stock.code:
                self.favorites_stocks.remove(st)
                break
        
        content = {}
        for st in self.favorites_stocks:
            content[st.code] = st.name

        with open(self.favorite_path, "wt", encoding='utf-8') as f:
            js = json.dumps(content, ensure_ascii=False, indent=4)
            f.write(js)
            f.close()
        print_info("remove stock(%s, %s) from favorites."%(stock.code, stock.name))

# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/09
# @version 1.0
# @desc: The widget to show board.

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from pandas import DataFrame

from stock.common.stock import Stock
from stock.common.qt.widget_button_info import WidgetButtonInfo
from stock.common.qt.color import UiColor
from stock.local.china.china_stocks import ChinaStocks
from stock.local.qt.widget_search_stock import WidgetSearchStock
from stock.local.qt.widget_line_edit_search import LineEditSearch
from stock.data.reader import DataReader
from stock.draw.candle import Candle

class WidgetBoard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WidgetBoard, self).__init__(parent)

        self.cs = ChinaStocks()

        self.layout_v = QtWidgets.QVBoxLayout()
        self.layout_h1 = QtWidgets.QHBoxLayout()
        self.layout_h1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_h2 = QtWidgets.QHBoxLayout()
        self.layout_h2.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_h3 = QtWidgets.QHBoxLayout()
        self.layout_h3.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_h4 = QtWidgets.QHBoxLayout()
        self.layout_h4.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout_v.addLayout(self.layout_h1)
        self.layout_v.addLayout(self.layout_h2)
        self.layout_v.addLayout(self.layout_h3)
        self.layout_v.addLayout(self.layout_h4)
        self.layout_v.addStretch()
        self.layout_v.setSpacing(20)
        self.setLayout(self.layout_v)

        self._layout_h1_()
        self._layout_h2_()
        self._layout_h3_()

    def _layout_h1_(self):
        line_edit_search = LineEditSearch(self)
        self.layout_h1.addWidget(line_edit_search)          
    
    def _layout_h2_(self):
        codes = ["sh000001", "sz399001"]
        for code in codes:
            st = self.cs.find_a_stock(code)[0]
            df = DataReader().read_history(st)

            now = float(df.iloc[-1].get('close'))
            last_day = float(df.iloc[-2].get('close'))
            minus = now - last_day
            ratio = "%.2f    %.2f%%"%(minus, 100.0*(minus)/last_day)

            color = UiColor.red
            if minus < 0:
                color = UiColor.green
            button = WidgetButtonInfo([st.name, str(now), ratio], color=color, slot=self._draw_candle_, df=df)            
            self.layout_h2.addWidget(button)

        self.layout_h2.setSpacing(20)
        self.layout_h2.addStretch()        

    def _layout_h3_(self):
        codes = ["sz399006", "sh000688", "sh000016", "sz399300"]
        for code in codes:
            st = self.cs.find_a_stock(code)[0]
            df = DataReader().read_history(st)

            now = float(df.iloc[-1].get('close'))
            last_day = float(df.iloc[-2].get('close'))
            minus = now - last_day
            ratio = "%.2f    %.2f%%"%(minus, 100.0*(minus)/last_day)

            color = UiColor.red
            if minus < 0:
                color = UiColor.green
            button = WidgetButtonInfo([st.name, str(now), ratio], color=color, slot=self._draw_candle_, df=df)       
            self.layout_h3.addWidget(button)

        self.layout_h3.setSpacing(20)
        self.layout_h3.addStretch()              

    def _draw_candle_(self, **kwargs):
        if 'df' not in kwargs.keys():
            return
        
        candle = Candle(kwargs['df'])
        candle.refresh()
        candle.exec_()

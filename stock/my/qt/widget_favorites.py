# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/09
# @version 1.0
# @desc: SHow your favorites stocks.

from PyQt5 import QtWidgets, QtCore, QtGui

from pandas import DataFrame
import pandas as pd

from stock.data.reader import DataReader
from stock.my.favorites import Favorite
from stock.draw.utils import draw_one_stock_today

class WidgetFavorites(QtWidgets.QWidget):
    """ Widget to show favorite stocks.    
    """
    def __init__(self, parent=None):
        super(WidgetFavorites, self).__init__(parent)

        self.layout_v = QtWidgets.QVBoxLayout()
        self.layout_v.setSpacing(20)

        self.tableModel = QtGui.QStandardItemModel()
        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.tableModel)
        self.layout_v.addWidget(self.tableView)

        self.tableView.doubleClicked.connect(self._slot_draw_a_stock_)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # self.layout_v.addStretch()
        self.setLayout(self.layout_v)

    def showEvent(self, event):
        QtWidgets.QWidget.showEvent(self, event)

        if self.isVisible():
            stocks =  Favorite().favorites_stocks
            reader = DataReader()

            df = None            
            data_list = []
            for i in range(0, len(stocks)):
                stock = stocks[i]
                data_list.append(reader.lates_price(stock))
            df = pd.DataFrame(data_list, index=None)
            df = df.dropna(axis=1)
            df.index = range(0, len(df))
            df = df.drop(columns='time')
            cols = df.columns.tolist()
            cols = ['code'] + [ele for ele in cols if ele != 'code']
            cols = ['name'] + [ele for ele in cols if ele != 'name']
            
            df = df[cols]

            self._init_table_view_(df)

    def _init_table_view_(self, df):

        if df is None:
            return

        self.tableModel.clear()
        
        self.tableModel.setHorizontalHeaderLabels(df.columns)
        
        for i in range(0, df.shape[0]):
            items = []
            for header_name in df.columns.tolist():
                value = df.iloc[i][header_name]
                if isinstance(value, float):
                    value = '%.2f'%(value)
                elif not isinstance(value, str):
                    value = str(value)
                if header_name == 'gain_loss_ratio':
                    value = '%s%%'%(value)
                items.append(QtGui.QStandardItem(value))
            self.tableModel.appendRow(items)

    def _slot_draw_a_stock_(self, table_index):
        index = table_index.row() 
        st_code = self.tableModel.item(index, 1).text()
        if st_code is None:
            return
        draw_one_stock_today(st_code)

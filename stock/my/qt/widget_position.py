# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/09
# @version 1.0
# @desc: Widget to show positions in hand.

from PyQt5 import QtWidgets, QtCore, QtGui
from pandas import DataFrame

from stock.my.trade import Trade
from stock.draw.utils import draw_one_stock_today

class WidgetPositions(QtWidgets.QWidget):
    """ Widget to show positions in hand.
    
        The showEvent() will trigger the table data to refresh.        
    """

    def __init__(self, parent=None):
        super(WidgetPositions, self).__init__(parent)

        self.layout_v = QtWidgets.QVBoxLayout()
        self.layout_v.setSpacing(20)

        self.label = QtWidgets.QLabel(text="")
        self.layout_v.addWidget(self.label)

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
            self._init_table_view_(Trade().my_positions())

    def _init_table_view_(self, positions):

        df = None
        total_money = None
        total_earn = None
        if 'df' in positions.keys():
            df = positions['df']
        if 'total_money' in positions.keys():
            total_money = positions['total_money']
        if 'total_earn' in positions.keys():
            total_earn = positions['total_earn']

        self.label.setText(
            "Total money: %.2f                    Earn: %.2f " % (total_money, total_earn))

        self.tableModel.clear()

        self.tableModel.setHorizontalHeaderLabels(df.columns)
        for i in range(0, df.shape[0]):
            self.tableModel.appendRow([
                QtGui.QStandardItem(df.iloc[i]['name']),
                QtGui.QStandardItem(df.iloc[i]['code']),
                QtGui.QStandardItem('%.2f' % (df.iloc[i]['quantity'])),
                QtGui.QStandardItem('%.2f' % (df.iloc[i]['current_price'])),
                QtGui.QStandardItem('%.2f%%' % (df.iloc[i]['today_ratio'])),
                QtGui.QStandardItem('%.2f' % (df.iloc[i]['earn_or_loss']))
            ])

    def _slot_draw_a_stock_(self, table_index):
        index = table_index.row() 
        st_code = self.tableModel.item(index, 1).text()
        if st_code is None:
            return
        draw_one_stock_today(st_code)
        
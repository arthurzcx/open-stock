# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/06
# @version 1.0
# @desc: Use PyQt5 GUI to show data.

from PyQt5 import QtWidgets, QtGui, QtCore

import sys
from multiprocessing import Process

from common.qt.dlg_input_a_stock import DlgInputAStock
import data.reader as data_reader
from local.china.china_stocks import ChinaStocks
from web.utils.data_update import UtilsUpdateData

from local.qt.ui_find_stock import DlgFindStock
from local.qt.widget_board import WidgetBoard
from my.qt.widget_position import WidgetPositions
from my.qt.widget_favorites import WidgetFavorites
from draw.candle import Candle

class MainWindow(QtWidgets.QMainWindow):
    """ 
    Main window.
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("金融数据分析器")
        self.resize(1024, 720)

        self._init_menu_()
        self._init_central_widget_()

        self.uud = UtilsUpdateData()
    
    def _init_menu_(self):
        self.menu_file = QtWidgets.QMenu("Page")
        self.menuBar().addMenu(self.menu_file)

        # ==============================================
        # Tools menu
        self.menu_tools = QtWidgets.QMenu("Tools")
        self.menuBar().addMenu(self.menu_tools)

        self.action_update_history = QtWidgets.QAction(text="Update history data")
        self.action_update_history.triggered.connect(self._slot_update_history_)
        self.menu_tools.addAction(self.action_update_history)                

        self.action_find_stock = QtWidgets.QAction(text="Find a stock")
        self.action_find_stock.triggered.connect(self._slot_find_stock_)
        self.menu_tools.addAction(self.action_find_stock)

        self.action_candle_a_stock = QtWidgets.QAction(text="Draw candle a stock")
        self.action_candle_a_stock.triggered.connect(self._slot_draw_candle)
        self.menu_tools.addAction(self.action_candle_a_stock)        


        # Tools menu ends
        # ==============================================
    
    def _init_central_widget_(self):
        self.tabs = QtWidgets.QTabWidget(parent=self)
        self.setCentralWidget(self.tabs)

        self.tabBoard = WidgetBoard(self.tabs)
        self.tabs.addTab(self.tabBoard, 'Board')

        self.tabPositions = WidgetPositions(self.tabs)
        self.tabs.addTab(self.tabPositions, 'Positions')

        self.tabFavorites = WidgetFavorites(self.tabs)
        self.tabs.addTab(self.tabFavorites, 'Favorites')
        # layout = QtWidgets.QGridLayout()                
        # self.centralWidget().setLayout(layout)

        # self.btn_update_history = QtWidgets.QPushButton(text='Update history')
        # layout.addWidget(self.btn_update_history)
        # self.btn_update_history.clicked.connect(self._slot_update_history_)

    def _slot_update_history_(self):
        try:
            uud = UtilsUpdateData()
            p = Process(target=uud.update_history, args=(3,))
            p.start()
        except Exception as e:
            print(e)

    def _slot_find_stock_(self):
        dlg = DlgFindStock()
        dlg.exec_()

    def _slot_draw_candle(self):
        dlg = DlgInputAStock()
        if dlg.exec_() :
            st_info = dlg.line_edit.text()
            cs = ChinaStocks()
            st = cs.get_st_by_info(st_info)
            df = data_reader.DataReader().read_history(st)
            
            candle_obj = Candle(df)
            candle_obj.refresh()
            candle_obj.exec_()
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec_())
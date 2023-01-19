from PyQt5 import QtWidgets, QtCore, QtGui

from local.qt.widget_search_stock import WidgetSearchStock

class LineEditSearch(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(LineEditSearch, self).__init__(parent)

    def mousePressEvent(self, event):        
        widget_search_stock = WidgetSearchStock()
        widget_search_stock.exec_()
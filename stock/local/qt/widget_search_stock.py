from PyQt5 import QtWidgets, QtCore, QtGui

from local.china.china_stocks import ChinaStocks

class WidgetSearchStock(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(WidgetSearchStock, self).__init__(parent)

        self.setWindowTitle("搜索")

        self.cs = ChinaStocks()

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.listWidget = QtWidgets.QListWidget(self)

        self.layout_v = QtWidgets.QVBoxLayout(self)
        self.layout_v.addWidget(self.lineEdit)
        self.layout_v.addWidget(self.listWidget)
        self.setLayout(self.layout_v)

        self.lineEdit.textChanged.connect(self._slot_edit_text_changed_)
    
    def _slot_edit_text_changed_(self, text):
        print(text)

        self.listWidget.clear()

        if len(text) <1:
            return
        stocks = self.cs.find_a_stock(text)
        if stocks is None or len(stocks) < 1:
            return
        elif len(stocks) > 10:
            stocks = stocks[0:10]
        
        for st in stocks:
            QtWidgets.QListWidgetItem(st.name, self.listWidget)            


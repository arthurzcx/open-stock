from PyQt5 import QtWidgets, QtCore, QtGui

from stock.local.china.china_stocks import ChinaStocks

class DlgFindStock(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DlgFindStock, self).__init__(parent)

        self.resize(200, 50)
        self.setMinimumWidth(150)
        self.setWindowTitle('Search stock')

        layout = QtWidgets.QHBoxLayout()

        self.line_edit = QtWidgets.QLineEdit()        
        self.btn_confirm = QtWidgets.QPushButton(text='OK')
        self.btn_confirm.clicked.connect(self._slot_find_stock_)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.btn_confirm)

        self.setLayout(layout)

    def _slot_find_stock_(self):
        st_info = self.line_edit.text()
        if len(st_info) < 1:
            return

        cs = ChinaStocks()
        found_list = cs.find_a_stock(st_info)
        if len(found_list) < 1:
            msg_box = QtWidgets.QMessageBox(text='Found nothing! Please comfirm your input.')
            msg_box.setWindowTitle("Found stocks")
            msg_box.exec_()
            return

        str = ''
        for st in found_list:
            str += st.code + " " + st.name + "\n"
        msg_box = QtWidgets.QMessageBox(text=str)
        msg_box.setWindowTitle("Found stocks")
        msg_box.exec_()


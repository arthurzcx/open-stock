# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/07
# @version 1.0
# @desc: A simple dlg to input a stock's information.

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog

class DlgInputAStock(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DlgInputAStock, self).__init__(parent)

        self.resize(200, 50)
        self.setMinimumWidth(150)
        self.setWindowTitle('Stock code or name')

        layout = QtWidgets.QHBoxLayout()

        self.line_edit = QtWidgets.QLineEdit()        
        self.btn_confirm = QtWidgets.QPushButton(text='OK')
        self.btn_confirm.clicked.connect(self._slot_ok_)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.btn_confirm)

        self.setLayout(layout)

    def _slot_ok_(self):
        QDialog.accept(self)
        

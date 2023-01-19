# !/usr/bin/python
# -*- encoding:utf-8 -*-

# @author: Arthurz
# @date: 2022/04/09
# @version 1.0
# @desc: A button to show information, single line or multiple lines.

from PyQt5 import QtWidgets, QtCore, QtGui

from stock.common.qt.color import UiColor

class WidgetButtonInfo(QtWidgets.QPushButton):
    """ The button to show infomation, single line or multiple line.
    
    Please control the length of information in every line.

    Attributes:
        info: should be a list of str or just a single lien string.  
    """
    def __init__(self, info, **kwargs):
        parent = None
        color = None

        if 'parent' in kwargs.keys():
            parent = kwargs['parent']
        if 'color' in kwargs.keys():
            color = kwargs['color']

        super(WidgetButtonInfo, self).__init__(parent)

        if color is not None:
            self.setStyleSheet("background-color: %s;"%(color))

        if  isinstance(info, list):
            text = '\n'.join(info)
            self.setText(text)
        elif isinstance(info, str):
            self.setText(info)
        
        if 'slot' in kwargs.keys():
            self.clicked.connect(lambda: kwargs['slot'](**kwargs))
        

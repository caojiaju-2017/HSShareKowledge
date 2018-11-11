#!/usr/bin/python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *

class MyLabel(QLabel):
    MyLabelPressedSignal = pyqtSignal(int)
    # MyLabelPressedSignal2 = pyqtSignal()

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.MyLabelPressed = 0

        self.statIndex = 0
    '''
    def mouseDoubleClickEvent(self,e):
        print 'mouse double clicked'
    '''

    def mousePressEvent(self, e):
        # print 'mousePressEvent'
        self.MyLabelPressed = 1

    def mouseReleaseEvent(self, e):
        # print 'mouseReleaseEvent'
        if self.MyLabelPressed == 1:
            self.MyLabelPressedSignal.emit(self.statIndex)
            # self.MyLabelPressedSignal2.emit()
            self.MyLabelPressed = 0
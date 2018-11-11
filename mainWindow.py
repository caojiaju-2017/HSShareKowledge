#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


from UIPackage.KnowlegeForm import *
from UIPackage.LoginMainWindow import *
if __name__=='__main__':
    app = QApplication(sys.argv)
    # QApplication.setStyle(u"Fusion")
    window = KnowlegeForm()
    window.show()
    window.initControls()
    sys.exit(app.exec_())


#https://blog.csdn.net/saga1979/article/details/51734001

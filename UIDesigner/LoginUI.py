# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 523)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loginTitle = QtWidgets.QLabel(self.centralwidget)
        self.loginTitle.setGeometry(QtCore.QRect(240, 80, 301, 41))
        self.loginTitle.setObjectName("loginTitle")
        self.loginpannel = QtWidgets.QWidget(self.centralwidget)
        self.loginpannel.setGeometry(QtCore.QRect(170, 220, 431, 61))
        self.loginpannel.setObjectName("loginpannel")
        self.pbLogin = QtWidgets.QPushButton(self.loginpannel)
        self.pbLogin.setGeometry(QtCore.QRect(370, 10, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pbLogin.setFont(font)
        self.pbLogin.setObjectName("pbLogin")
        self.userName = QtWidgets.QLineEdit(self.loginpannel)
        self.userName.setGeometry(QtCore.QRect(10, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.userName.setFont(font)
        self.userName.setObjectName("userName")
        self.userPassword = QtWidgets.QLineEdit(self.loginpannel)
        self.userPassword.setGeometry(QtCore.QRect(200, 10, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.userPassword.setFont(font)
        self.userPassword.setObjectName("userPassword")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loginTitle.setText(_translate("MainWindow", "TextLabel"))
        self.pbLogin.setText(_translate("MainWindow", "GO"))


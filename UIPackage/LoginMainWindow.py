#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from ByPlatform.Base.OutPutHelper import *
import sys
from UIDesigner.LoginUI import Ui_MainWindow
from tinydb import TinyDB, Query
from ByPlatform.Base.TimeHelper import *
# from UIPackage.WaitWindow import WaitWindow
from UIPackage.KnowlegeForm import KnowlegeForm

class LoginMainWindow(QMainWindow,Ui_MainWindow):
    """docstring for myDialog"""
    def __init__(self, arg=None):
        super(LoginMainWindow, self).__init__(arg)
        self.setupUi(self)
        self.setWindowIcon(QIcon(r'Res\logo.png'))

        self.setWindowTitle("超级智慧终端")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(580)

        # 设置登录主界面背景
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(),QBrush(QPixmap(r"Res\loginback.jpg")))
        self.setPalette(window_pale)

        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.setStyleSheet("venus--TitleBar {border-radius:10px;}")
        # 窗口移动
        self.m_flag = False
        self.m_Position = None

        # 初始化标题
        self.initTitle()

        # 初始化按钮
        self.initInputButton()

        # 加载账户信息
        self.accountSet = None
        self.loadAccount()

        self.mainWindow = None

    def loadAccount(self):
        configQuery = Query()

        db = TinyDB('config.json')
        table = db.table('config')

        result = table.all()

        if len(result) <= 0:
            pass
        else:
            self.accountSet = result[0]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


    def initTitle(self):
        # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
        png = QPixmap('Res\wordtitle.png')

        # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        self.loginTitle.setPixmap(png)

        labWd = self.width() * 0.28
        labHd = int(labWd *60/340.0)

        self.loginTitle.setMinimumWidth(labWd)
        self.loginTitle.setMinimumHeight(labHd)

        startX = (self.width() - labWd) / 2
        startY = int(self.height()*0.3)

        self.loginTitle.setGeometry(startX,startY,labWd,labHd)

        self.loginTitle.setScaledContents(True)  # 让图片自适应label大小

        self.pbLogin.clicked.connect(self.LoginSystem)
        pass

    def LoginSystem(self):
        '''
        登陆指令
        :return:
        '''

        self.waitDlg = WaitWindow()

        # // 屏幕居中显示
        frmX = self.waitDlg.width()
        frmY = self.waitDlg.height()

        deskWidth = QDesktopWidget().width()
        deskHeight = QDesktopWidget().height()
        movePoint = QPoint(deskWidth / 2 - frmX / 2, deskHeight / 2 - frmY / 2)
        # movePoint = QPoint(0,0)

        self.waitDlg.move(movePoint)
        # self.waitDlg.setModal(True)
        # self.waitDlg.createLabel()
        self.waitDlg.update()
        self.waitDlg.exec_()

        OutPutHelper.consolePrint("loginsystem")
        userName = self.userName.text()
        userPassword = self.userPassword.text()

        MESSAGE = "账号或密码错误"
        if self.accountSet:
            if userName == self.accountSet["account"] and userPassword == self.accountSet["password"]:
                pass
            else:
                reply = QMessageBox.information(self, "信息", MESSAGE)
                if reply == QMessageBox.Ok:
                    pass
                else:
                    pass
                return
        elif userName == "root" and userPassword == "123456":

            self.accountSet = {"account": userName, "password": userPassword,
                                  "logintime": TimeHelper.getCurrentTime()}

        else:
            reply = QMessageBox.information(self, "信息", MESSAGE)
            if reply == QMessageBox.Ok:
                pass
            else:
                pass
            return

        db = TinyDB('config.json')
        table = db.table('config')
        table.purge()
        table.insert(self.accountSet)

        self.mainWindow = SuperSmartWindow()
        self.mainWindow.show()
        self.hide()

    def initInputButton(self):
        palette = self.palette()

        # palette.setColor(palette.Window, QColor(210, 210, 210))
        #
        # self.loginpannel.setAutoFillBackground(True)
        # self.loginpannel.setPalette(palette)
        self.loginpannel.setWindowOpacity(0.6)
        # setWindowOpacity

        self.loginpannel.setStyleSheet("#loginpannel{border:0px groove gray;border-radius:10px;padding:2px 4px;background-color: #ffffff;color: #000000;}")

        self.pbLogin.setStyleSheet(
            "#pbLogin{border-radius:6px; background:rgba(65, 168, 200,0.8); color:white;}" + "#pbLogin:hover{background:rgb(255,128,64);}")

        self.pbLogin.setCursor(Qt.PointingHandCursor)
        self.userName.setStyleSheet(
            "#userName{border:2px groove gray;border-radius:4px; background:rgba(255, 255, 255,1); color:black;}" + "#userName:hover{background:rgb(255, 255, 255);}")

        self.userPassword.setStyleSheet(
            "#userPassword{border:2px groove gray;border-radius:4px; background:rgba(255, 255, 255,1); color:black;}" + "#userPassword:hover{background:rgb(255, 255, 255);}")


        panelWd = self.loginpannel.width()
        panelHd = self.loginpannel.height()
        startX = (self.width() - panelWd) / 2
        startY = (self.height() - panelHd)*3.0 / 5

        self.loginpannel.setGeometry(startX, startY, panelWd, panelHd)

        self.userName.setText("root")
        self.userPassword.setEchoMode(QLineEdit.Password)
        self.userPassword.setText("123456")



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.pbLogin.click()
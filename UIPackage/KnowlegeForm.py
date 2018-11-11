#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from ByPlatform.Base.OutPutHelper import *
import sys
from tinydb import TinyDB, Query
from WebEngineViewEx import WebEngineViewEx
from PyQt5.QtWidgets import *
from ShareDatas import ShareDatas
import pickle
import threading

from UIDesigner.KnowlegeWin import *
from ByPlatform.StorageHelper.StorageHelper import *
from ByPlatform.LoggerHelper.LoggerHelper import *

class KnowlegeForm(QMainWindow,Ui_MainWindow):
    heightLine = 50
    Version="Version1.4.1"
    def __init__(self, arg=None):
        """

        :rtype: object
        """
        super(KnowlegeForm, self).__init__(arg)

        self.setWindowIcon(QIcon(r'Res\logo.png'))
        self.setWindowTitle("超级智慧终端")

        wd = QApplication.desktop().width()
        hd = QApplication.desktop().height()
        self.setMinimumWidth(wd*0.8)
        self.setMinimumHeight(hd*0.8)

        self.setupUi(self)

        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet("#middleWidget{border-radius:2px; background:rgba(255, 255, 255,1);};border:1px groove gray;")
        # 窗口移动
        self.m_flag = False
        self.m_Position = None

        self.initLogger()
        StorageHelper(ShareDatas.Global_LOGGER, "ns_account")
        StorageHelper(ShareDatas.Global_LOGGER, "ns_knowleges")
        StorageHelper(ShareDatas.Global_LOGGER, "ns_knowlege_map_lab")
        StorageHelper(ShareDatas.Global_LOGGER, "ns_labels")

        return

    # 初始化日志
    def initLogger(sefl):
        OutPutHelper.consolePrint("Init Logger", "ProgramInit")
        Global_LOGGER = LoggerHelper()
        OutPutHelper.consolePrint("Init Logger... ...Ok", "ProgramInit")
    # ===============================================窗体移动==============================================
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

    # ===============================================窗体移动==============================================



    # =======!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!界面初始化=========================================================================================
    def initControls(self):
        self.setBackcolor()
        self.setControlPosition()

        self.setControlStyle()

        self.registerEvent()

        self.registertTray()

    def registertTray(self):
        self.tray = QSystemTrayIcon() #创建系统托盘对象
        self.icon = QIcon('logo_img.png')  #创建图标
        self.tray.setIcon(self.icon)  #设置系统托盘图标
        self.tray.activated.connect(self.TuoPanEvent) #设置托盘点击事件处理函数
        self.tray_menu = QMenu(QApplication.desktop()) #创建菜单
        self.RestoreAction = QAction(u'还原 ', self, triggered=self.show) #添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QAction(u'退出 ', self, triggered=qApp.quit) #添加一级菜单动作选项(退出程序)
        self.tray_menu.addAction(self.RestoreAction) #为菜单添加动作
        self.tray_menu.addAction(self.QuitAction)
        self.tray.setContextMenu(self.tray_menu) #设置系统托盘菜单

    def TuoPanEvent(self):
        pass

    def setControlStyle(self):
        # ===============================头部=============================================================================
        self.topWidget.setStyleSheet(
            "#topWidget{background:rgba(5, 212, 209,0.7);}")

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\logo_img.png').scaled(QSize(maxSize,maxSize ))
        self.orgLogo.setAlignment(Qt.AlignLeft)
        self.orgLogo.setPixmap(png)
        self.orgLogo.setStyleSheet(
            "#orgLogo{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}")
        self.titleName.setText("我的知识仓库")
        self.titleName.setStyleSheet("#titleName{color:rgba(91, 73, 1,1);}")
        self.titleName.setFont(QFont("Timers", 12, QFont.DemiBold))

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\exit.png').scaled(QSize(maxSize - 8,maxSize - 8))
        self.closeLab.resize(QSize(maxSize,maxSize))
        self.closeLab.setAlignment(Qt.AlignCenter)
        self.closeLab.setPixmap(png)
        self.closeLab.setStyleSheet(
            "#closeLab{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" + "#closeLab:hover{background:rgba(255,128,64,0.1);}")
        self.closeLab.setCursor(Qt.PointingHandCursor)
        self.hiddenLab.setToolTip("退出程序")

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\min.png').scaled(QSize(maxSize - 8,maxSize - 8))
        self.hiddenLab.resize(QSize(maxSize,maxSize))
        self.hiddenLab.setAlignment(Qt.AlignCenter)
        self.hiddenLab.setPixmap(png)
        self.hiddenLab.setStyleSheet(
            "#hiddenLab{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" + "#hiddenLab:hover{background:rgba(255,128,64,0.1);}")
        self.hiddenLab.setCursor(Qt.PointingHandCursor)
        self.hiddenLab.setToolTip("最小化")

        # ======================================企业logo=================================================================
        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\copyright_logo.png').scaled(QSize(maxSize*5,maxSize*2))
        self.org_logo.setAlignment(Qt.AlignCenter)
        self.org_logo.setPixmap(png)
        self.org_logo.setStyleSheet(
            "#org_logo{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" )


        # ===============================中间部分==========================================================================
        self.middleWidget.setStyleSheet(
            "#middleWidget{border-radius:4px; background:rgba(255, 255, 255,0);}")

        self.searchText.setStyleSheet(
            "#searchText{border:1px groove gray;border-radius:4px; background:rgba(255, 255, 255,1); color:black;height:%spx}"%(KnowlegeForm.heightLine - 6))
        self.searchText.setFont(QFont("Timers", 18, QFont.Normal) )

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\search.png').scaled(QSize(maxSize,maxSize))
        self.searchBtn.setAlignment(Qt.AlignCenter)
        self.searchBtn.setPixmap(png)
        self.searchBtn.setStyleSheet(
            "#searchBtn{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" + "#searchBtn:hover{background:rgba(255,128,64,0.2);}")
        self.searchBtn.setCursor(Qt.PointingHandCursor)
        self.searchBtn.setToolTip("搜索")
        # self.

        # =========================================================底部================================================
        self.bottomWidget.setStyleSheet(
            "#bottomWidget{border-radius:4px; background:rgba(204, 252, 254,0.7);}")
        self.versionInfo.setStyleSheet(
            "#versionInfo{color:rgba(253, 87, 13,1);}")
        self.versionInfo.resize(QSize(100,50))
        self.versionInfo.setText("版本：%s" % KnowlegeForm.Version)
        self.versionInfo.setFont(QFont("Timers", 10, QFont.Bold))

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\weixinBlue.png').scaled(QSize(maxSize,maxSize))
        self.bindWechat.setAlignment(Qt.AlignCenter)
        self.bindWechat.setPixmap(png)
        self.bindWechat.setStyleSheet(
            "#bindWechat{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" + "#bindWechat:hover{background:rgba(255,128,64,0.2);}")
        self.bindWechat.setCursor(Qt.PointingHandCursor)
        self.bindWechat.setToolTip("绑定微信")

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\login.png').scaled(QSize(maxSize,maxSize))
        self.regOrLogin.setAlignment(Qt.AlignCenter)
        self.regOrLogin.setPixmap(png)
        self.regOrLogin.setStyleSheet(
            "#regOrLogin{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" + "#regOrLogin:hover{background:rgba(255,128,64,0.2);}")
        self.regOrLogin.setCursor(Qt.PointingHandCursor)
        self.regOrLogin.setToolTip("点击账号自动注册")

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\setting.png').scaled(QSize(maxSize,maxSize))
        self.bindPhone.setAlignment(Qt.AlignCenter)
        self.bindPhone.setPixmap(png)
        self.bindPhone.setStyleSheet(
            "#bindPhone{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" + "#bindPhone:hover{background:rgba(255,128,64,0.2);}")
        self.bindPhone.setCursor(Qt.PointingHandCursor)
        self.bindPhone.setToolTip("设置账号信息")

        maxSize = KnowlegeForm.heightLine - 6
        png = QPixmap(r'Res\register.png').scaled(QSize(maxSize,maxSize))
        self.addKnowlege.resize(QSize(100, maxSize))
        self.addKnowlege.setAlignment(Qt.AlignCenter)
        self.addKnowlege.setPixmap(png)
        self.addKnowlege.setStyleSheet(
            "#addKnowlege{border-radius:6px; background:rgba(200, 200, 200,0); color:white;}" + "#addKnowlege:hover{background:rgba(255,128,64,0.2);}")
        self.addKnowlege.setCursor(Qt.PointingHandCursor)
        self.addKnowlege.setToolTip("添加我的知识")


    def setBackcolor(self):
        # 设置登录主界面背景
        window_pale = QPalette()

        qtimage = QPixmap(r"Res\mainback.jpg")
        qtimage = qtimage.scaled(self.size())
        window_pale.setBrush(self.backgroundRole(), QBrush(qtimage))
        self.setPalette(window_pale)

        # self.
        pass
    def setControlPosition(self):

        # 顶部
        # self.topTitle.setGeometry(0,0,self.width(),self.topTitle.height())
        self.topWidget.setGeometry(0, 0, self.width(), KnowlegeForm.heightLine)

        self.org_logo.setGeometry((self.width() - 5*KnowlegeForm.heightLine)/2,self.height()*0.20, KnowlegeForm.heightLine*5 , KnowlegeForm.heightLine*2)

        # 中间左边
        self.middleWidget.setGeometry(self.width()*0.2,self.height()*0.35, self.width()*0.6, KnowlegeForm.heightLine)

        setHd = 10
        # 底部
        self.bottomWidget.setGeometry(0,self.height() - KnowlegeForm.heightLine - setHd, self.width(),KnowlegeForm.heightLine+setHd)
        pass
    # =======!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!界面初始化=========================================================================================

    # =======!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!事件初始化=========================================================================================
    def registerEvent(self):
        self.hiddenLab.MyLabelPressedSignal.connect(self.minWindow)
        self.closeLab.MyLabelPressedSignal.connect(self.closeWindow)
        self.searchBtn.MyLabelPressedSignal.connect(self.seartKnowlege)
        self.bindWechat.MyLabelPressedSignal.connect(self.bindWechartAccount)
        self.regOrLogin.MyLabelPressedSignal.connect(self.loginAccount)
        self.bindPhone.MyLabelPressedSignal.connect(self.bindMyTelphone)
        self.addKnowlege.MyLabelPressedSignal.connect(self.addKnowlegeInfo)

    def minWindow(self):
        self.showMinimized()
        pass

    def closeWindow(self):
        '''
            关闭窗体
            :return:
        '''
        OutPutHelper.consolePrint("关闭窗体")

        QApplication.exit()

    def seartKnowlege(self):
        pass

    def bindWechartAccount(self):
        pass

    def loginAccount(self):
        pass

    def bindMyTelphone(self):
        pass

    def addKnowlegeInfo(self):
        pass

    # =======!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!事件初始化=========================================================================================
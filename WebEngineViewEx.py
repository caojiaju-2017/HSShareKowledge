#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from ByPlatform.Base.OutPutHelper import OutPutHelper
class WebEngineViewEx(QWebEngineView):
    windowList = []
    def __init__(self, *args, **kwargs):
        super(WebEngineViewEx, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}  # 存放cookie字典
        self.now_url = None
        self.__pWnd = None

    def setParentWnd(self, handle):
        self.__pWnd = handle

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里

    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():  # 遍历字典
            cookie_str += (key + '=' + value + ';')  # 将键值对拿出来拼接一下
        return cookie_str  # 返回拼接好的字符串

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineViewEx()
        new_webview.setParentWnd(self.__pWnd)
        self.__pWnd.create_tab(new_webview,-1,labName="SubWeb")


        return new_webview

    def linkHovered(self, url):
        self.now_url=url

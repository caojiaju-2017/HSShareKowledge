#!/usr/bin/python
# -*- coding:utf-8 -*-
import hashlib
from EncryptHelper import EncryptHelper
class LicenseModel(object):
    def __init__(self):
        self.email = None
        self.key = "0cf1fe6e-b043-11e8-97e1-505bc2bf182e"
        self.lisencekey = None

    def validLicense(self):
        result = EncryptHelper.encryMd5(self.email,self.key)
        if result == self.lisencekey:
            return True
        else:
            return False


if __name__ == "__main__":
    model = LicenseModel()
    model.email = "h-sen@foxmail.com"
    result = EncryptHelper.encryMd5(model.email, model.key)
    print (result)
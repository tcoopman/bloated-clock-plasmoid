# -*- coding: utf-8 -*-
from login_monitor_ui import *
from PyQt4.QtGui import *

class LoginMonitorConfig(QWidget, Ui_LoginConfig):
    def __init__(self, parent):
        QWidget.__init__(self,parent)
        self.setupUi(self)
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itemEditor.ui'
#
# Created: Tue Feb 24 10:49:25 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ItemEditor(object):
    def setupUi(self, ItemEditor):
        ItemEditor.setObjectName("ItemEditor")
        ItemEditor.resize(536, 584)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ItemEditor)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(ItemEditor)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.nameEdit = QtGui.QLineEdit(ItemEditor)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.fontChooser = KFontChooser(ItemEditor)
        self.fontChooser.setObjectName("fontChooser")
        self.verticalLayout_2.addWidget(self.fontChooser)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtGui.QLabel(ItemEditor)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.colorButton = KColorButton(ItemEditor)
        self.colorButton.setObjectName("colorButton")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.colorButton)
        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.retranslateUi(ItemEditor)
        QtCore.QMetaObject.connectSlotsByName(ItemEditor)

    def retranslateUi(self, ItemEditor):
        self.label.setText(QtGui.QApplication.translate("ItemEditor", "Item name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ItemEditor", "Font color:", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kdeui import KColorButton
from PyKDE4.kdeui import KFontChooser

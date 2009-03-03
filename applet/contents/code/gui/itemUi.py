# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'item.ui'
#
# Created: Tue Feb 24 15:39:04 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Item(object):
    def setupUi(self, Item):
        Item.setObjectName("Item")
        Item.resize(393, 72)
        self.horizontalLayout = QtGui.QHBoxLayout(Item)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.itemNameLabel = QtGui.QLabel(Item)
        self.itemNameLabel.setObjectName("itemNameLabel")
        self.horizontalLayout.addWidget(self.itemNameLabel)
        self.fontLabel = QtGui.QLabel(Item)
        self.fontLabel.setObjectName("fontLabel")
        self.horizontalLayout.addWidget(self.fontLabel)
        self.fontSizeLabel = QtGui.QLabel(Item)
        self.fontSizeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fontSizeLabel.setObjectName("fontSizeLabel")
        self.horizontalLayout.addWidget(self.fontSizeLabel)
        self.editButton = QtGui.QPushButton(Item)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)

        self.retranslateUi(Item)
        QtCore.QMetaObject.connectSlotsByName(Item)

    def retranslateUi(self, Item):
        Item.setWindowTitle(QtGui.QApplication.translate("Item", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.itemNameLabel.setText(QtGui.QApplication.translate("Item", "Item name", None, QtGui.QApplication.UnicodeUTF8))
        self.fontLabel.setText(QtGui.QApplication.translate("Item", "font", None, QtGui.QApplication.UnicodeUTF8))
        self.fontSizeLabel.setText(QtGui.QApplication.translate("Item", "font size", None, QtGui.QApplication.UnicodeUTF8))
        self.editButton.setText(QtGui.QApplication.translate("Item", "...", None, QtGui.QApplication.UnicodeUTF8))


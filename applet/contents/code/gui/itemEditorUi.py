# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itemEditor.ui'
#
# Created: Tue Feb 24 10:49:25 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyKDE4.kdeui import KColorButton
from PyKDE4.kdeui import KFontChooser
from PyKDE4.kdeui import KDialog

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


class ItemEditorWidget(QtGui.QWidget, Ui_ItemEditor):
    def __init__(self, parent):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        
        self.connect(self.nameEdit, SIGNAL("textChanged(QString)"), self.changed)
        self.connect(self.fontChooser, SIGNAL("fontSelected(QFont)"), self.changed)
        self.connect(self.colorButton, SIGNAL("changed(QColor)"), self.changed)
        
    def changed(self):
        self.emit(SIGNAL("changed(bool)"), True)
       

class ItemEditorDialog(KDialog):
    def __init__(self, parent, item):
        KDialog.__init__(self,parent)
        self.setCaption(i18n("Item editor"))
        self.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel|KDialog.Apply))
        
        w = ItemEditorWidget(self)
        self.setMainWidget(w)
        self.connect(self, SIGNAL("applyClicked()"), self.configAccepted)
        self.connect(self, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(w, SIGNAL("changed(bool)"), self, SLOT("enableButtonApply(bool)"))
            
        self.enableButtonApply(False);
        
        self.item = item
        self.updateUi()
        
    def updateUi(self):
        self.mainWidget().nameEdit.setText(self.item.name)
        self.mainWidget().fontChooser.setFont(self.item.font)
        self.mainWidget().colorButton.setColor(self.item.color)
         
    def configAccepted(self):
        self.item.name = self.mainWidget().nameEdit.text()
        self.item.font = self.mainWidget().fontChooser.font()
        self.item.color = self.mainWidget().colorButton.color()
        self.emit(SIGNAL("configAccepted()"))
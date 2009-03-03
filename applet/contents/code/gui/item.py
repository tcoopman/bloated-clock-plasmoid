'''
Created on Mar 3, 2009

@author: Thomas Coopman
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyKDE4.kdeui import KDialog
from PyKDE4.kdecore import i18n
from ..itemEditorUi import Ui_ItemEditor

class ItemList(QListWidget):
    def __init__(self, parent, im):
        QListWidget.__init__(self)
        self.im = im
        self.initUi()
        
    def initUi(self):
        for item in self.im:
            self.add(item)
            
    def add(self, item):
        ilwi = ItemListWidgetItem(item, self)
        self.addItem(ilwi)
        
    def showEdit(self):
        self.lastItem = self.currentItem().item
        itemEditor = ItemEditorDialog(self, self.lastItem)
        self.takeItem(self.currentRow())
        self.connect(itemEditor, SIGNAL("configAccepted()"), self._updateUi)
        itemEditor.show()
        
    def delete(self):
        del self.im[self.takeItem(self.currentRow()).item]
        
    def _updateUi(self):
        self.add(self.lastItem)
        
class ItemListWidgetItem(QListWidgetItem):
    def __init__(self, item, parent):
        QListWidgetItem.__init__(self,parent)
        self.item = item
        self._updateUi()
        
    def _updateUi(self):
        text = []
        text.append(str(self.item.name))
        text.append(": ")
        text.append(str(self.item.font.family()))
        text.append(" ")
        text.append(str(self.item.font.pointSize()))
        text.append("pt")
        self.setText("".join(text))
        self.setTextColor(self.item.color)
        
        fontSize = QApplication.font().pointSize()
        labelFont = QFont(self.item.font)
        labelFont.setPointSize(fontSize)
        self.setFont(labelFont)
        

class ItemEditorWidget(QWidget, Ui_ItemEditor):
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
        

    
    
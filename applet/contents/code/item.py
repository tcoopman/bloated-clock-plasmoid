# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyKDE4.kdeui import *
from PyKDE4.kdeui import KIcon
from PyKDE4.kdecore import i18n
from PyKDE4.plasma import Plasma


from itemUi import *
from itemEditorUi import *
from gui.item import ItemList
        
class ItemManager():
    def __init__(self):
        self.items = {}
        self._baseName = "item"
        
    def __iter__(self):
        return self.items.values().__iter__()
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items.values().__getitem__(index)
    
    def getList(self):
        return self.items.values()
        
    def getItemByName(self, name):
        try:
            return self.items[name]
        except:
            print "Item not found"
            
    def __delitem__(self, item):
        del self.items[item.name]
            
    def createItem(self, font, color):
        name = self._baseName + str(len(self) + 1)
        item = self.Item(self, name, font, color)
        self.items[name] = item
        return item 
    
    def update(self, oldname, newname):
        if str(newname) != oldname:
            self.items[str(newname)] = self.items[oldname]
            del self.items[oldname]
        
    class Item(object):
        def __init__(self, im, name, font, color):
            self.im = im
            self._name = name
            self.font = font
            self.color = color
                    
        @property
        def name(self):
            return self._name
        
        @name.setter
        def name(self, name):
            name = str(name)
            self.im.update(self.name, name)
            self._name = name
     
     
class ItemListWidget(QWidget):
    def __init__(self, parent, itemManager):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout(self))
        self.im = itemManager
        self.updateUi()
        
    def updateUi(self):
        self.nbItems = 0
        self.itemList = ItemList(self, self.im)
        self.layout().addWidget(self.itemList)
        self._addButtons()
        
    def _addButtons(self):
        self._addButton = QPushButton("add", self)
        self._addButton.setIcon(KIcon("list-add"))
        self.connect(self._addButton, SIGNAL("clicked()"), self._createItem)
        
        self._editButton = QPushButton("edit", self)
        self._editButton.setIcon(KIcon("list-add"))
        self._editButton.setEnabled(False)
        self.connect(self._editButton, SIGNAL("clicked()"), self.itemList.showEdit)
        
        self._deleteButton = QPushButton("delete", self)
        self._deleteButton.setIcon(KIcon("edit-delete"))
        self._deleteButton.setEnabled(False)
        self.connect(self._deleteButton, SIGNAL("clicked()"), self.itemList.delete)
        
        hbox = QHBoxLayout()
        hbox.insertStretch(0)
        hbox.addWidget(self._addButton)
        hbox.addWidget(self._editButton)
        hbox.addWidget(self._deleteButton)
        self.layout().addLayout(hbox)
        
        self.connect(self.itemList, SIGNAL("itemSelectionChanged()"), self._enableButtons)
        
    def _enableButtons(self):
        if self.itemList.currentItem():
            self._editButton.setEnabled(True)
            self._deleteButton.setEnabled(True)
        else:
            self._editButton.setEnabled(False)
            self._deleteButton.setEnabled(False)
            
    def _createItem(self):
        theme = Plasma.Theme.defaultTheme()
        font = theme.font(Plasma.Theme.DefaultFont)
        color = theme.color(Plasma.Theme.TextColor)
        item = self.im.createItem(font, color)
        self.itemList.add(item)
        
    def _deleteItem(self):
        pass
        
class XMLEditWidget(QWidget):
    def __init__(self, parent, xml):
        QWidget.__init__(self, parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.updateUi(xml)
        
    def updateUi(self, xml):
        self.edit = QTextEdit(self)
        self.edit.insertPlainText(xml)
        #self.edit.setAutoFormatting(False)
        self.layout.addWidget(self.edit)
        
    def xml(self):
        return self.edit.toPlainText()


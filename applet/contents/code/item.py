# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyKDE4.kdeui import *
from PyKDE4.kdeui import KIcon, KIconLoader
from PyKDE4.kdecore import i18n
from PyKDE4.plasma import Plasma


from gui.itemUi import Ui_Item
from gui.itemEditorUi import Ui_ItemEditor
        
class ItemManager():
    def __init__(self):
        self.items = {}
        self._baseName = "item"
        
    def __iter__(self):
        return self.items.values().__iter__()
    
    def __len__(self):
        return len(self.items)
    
    def getList(self):
        return self.items.values()
        
    def getItemByName(self, name):
        try:
            return self.items[name]
        except:
            print "Item not found"
            
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
            self.im.update(self.name, name)
            self._name = name
    

class ItemWidget(QWidget, Ui_Item):
    def __init__(self, parent,item):
        QWidget.__init__(self,parent)
        self.item = item
        self.setupUi(self)
        
        self.connect(self.editButton, SIGNAL("clicked()"), self.edit)
        self.itemEditor = None
        
        self._updateUi()
        
    def _updateUi(self):
        brush = QBrush(self.item.color)
        brush.setStyle(Qt.SolidPattern);
        palette = QApplication.palette()
        palette.setBrush(QPalette.WindowText, brush)
        self.itemNameLabel.setPalette(palette)
        self.fontLabel.setPalette(palette)
        self.fontSizeLabel.setPalette(palette)
        self.itemNameLabel.setText(self.item.name)
        
        fontSize = QApplication.font().pointSize()
        labelFont = QFont(self.item.font)
        labelFont.setPointSize(fontSize)
        self.fontLabel.setFont(labelFont)
        self.fontLabel.setText(self.item.font.family())
        self.fontSizeLabel.setText(str(self.item.font.pointSize()) + "pt")
        
    def edit(self):
        if not self.itemEditor:
            self.itemEditor = ItemEditorDialog(self, self.item)
            self.connect(self.itemEditor, SIGNAL("configAccepted()"), self._updateUi)
        self.itemEditor.show()
     
     
class ItemListWidget(QWidget):
    def __init__(self, parent, itemManager):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)
        self.im = itemManager
        self._iconLoader = KIconLoader()
        self._iconLoader.Action
        self.updateUi()
        
    def updateUi(self):
        self.nbItems = 0
        for item in self.im:
            self._addItem(item)
        self._addAddButton()
        
    def _addAddButton(self):
        self._addButton = QToolButton(self)
        self._addButton.setIcon(KIcon("list-add"))
        self.connect(self._addButton, SIGNAL("clicked()"), self._createItem)
        hbox = QHBoxLayout()
        hbox.insertStretch(0)
        hbox.addWidget(self._addButton)
        self.layout.addLayout(hbox)
        
        
    def _createItem(self):
        theme = Plasma.Theme.defaultTheme()
        font = theme.font(Plasma.Theme.DefaultFont)
        color = theme.color(Plasma.Theme.TextColor)
        item = self.im.createItem(font, color)
        self._addItem(item)
            
    def _addItem(self, item):
        itemWidget = ItemWidget(self, item)
        self.grid.addWidget(itemWidget, self.nbItems, 0)
        deleteButton = QToolButton(itemWidget)
        deleteButton.setIcon(KIcon("edit-delete"))
        self.connect(deleteButton, SIGNAL("clicked()"), self._deleteItem)
        self.grid.addWidget(deleteButton, self.nbItems, 1)
        self.nbItems += 1
        
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
'''
Created on Mar 3, 2009

@author: Thomas Coopman
'''

from PyQt4.QtGui import QColor, QListWidget, QListWidgetItem

class ItemList(QListWidget):
    def __init__(self, parent, im):
        QListWidget.__init__(self)
        self.im = im
        self.initUi()
        
    def initUi(self):
        for i in self.im:
            text = []
            text.append(i.name)
            text.append(": ")
            text.append(str(i.font.family()))
            text.append(" ")
            text.append(str(i.font.pointSize()))
            text.append("pt")
            item = QListWidgetItem("".join(text), self)
            item.setTextColor(i.color)
            item.setFont(i.font)
            self.addItem(item)
        

    
    
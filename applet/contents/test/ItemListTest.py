'''
Created on Mar 3, 2009

@author: thomas
'''
import sys
from PyQt4.QtGui import *
sys.path.append("../code/")
from item import ItemManager
from gui.item import ItemList


app = QApplication(sys.argv)

widget = QWidget()
widget.resize(250, 150)

im = ItemManager()
im.createItem(QFont("Helvetica"), QColor("red"))
im.createItem(QFont("Helvetica"), QColor("blue"))
listWidget = ItemList(widget, im)

layout = QVBoxLayout()
layout.addWidget(listWidget)
widget.setLayout(layout)
widget.show()

sys.exit(app.exec_())
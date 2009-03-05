# -*- coding: utf-8 -*-
# Copyright stuff
import re

from PyKDE4 import plasmascript
from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import *
from PyKDE4.plasma import Plasma
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from item import ItemListWidget
from item import XMLEditWidget
from item import ItemManager
from layout import LayoutBuilder
from plugin import PluginLoader


class BloatedClockApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.Square)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        
        self.dialog = None
        self._items()
        self._engines = {}
        self.pluginLoader = PluginLoader(self)
        
        self.x = False
        self.initGui()
        
    def initGui(self):
        self.updateUi()
        self.resize(250,250)
        
    def updateUi(self):
        try:
            xml = self.xmlEdit.xml()
        except:
            xml = """<plugins><clock name="klok1" other="test" bla="koe" /></plugins>
                <body>
                    <line><item1 parser="klok1" align="left">%hh:%mm:%ss</item1><item2 parser="klok1" align="left">after</item2></line>
                </body>"""
        lBuilder = LayoutBuilder(self.im, self.pluginLoader)
        self.l = lBuilder.build(xml)
           
    def showConfigurationInterface(self):
        windowTitle = str(self.applet.name()) + " Settings" #i18nc("@title:window", "%s Settings" % str(self.applet.name()))
        
        if self.dialog is None:
            self.dialog = KPageDialog()
            self.dialog.setFaceType(KPageDialog.List)
            self.dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
            self.dialog.setWindowTitle(windowTitle)
            
            self.connect(self.dialog, SIGNAL("applyClicked()"), self, SLOT("configAccepted()"))
            self.connect(self.dialog, SIGNAL("okClicked()"), self, SLOT("configAccepted()"))
        
            self.createConfigurationInterface(self.dialog)
            
        self.dialog.show()
        
    def createConfigurationInterface(self, parent):
        self.itemList = ItemListWidget(parent, self.im)
        xml = """<clock>
    <line><item1 align="left">text %hh.%mm:%ss</item1><item2 align="right">2de text</item2></line>
    <line><item1 align="center">center</item1></line>
    <line><item2 align="right">right</item2></line>
    </clock>"""
        self.xmlEdit = XMLEditWidget(parent, xml)
        parent.addPage(self.itemList, i18n("List of items"))
        parent.addPage(self.xmlEdit, i18n("Edit the xml"))
        
        #self.ui = LoginMonitorConfig(self.dialog)
        #self.dialog.addPage(self.ui, i18n("Configure provider"))
        #self._fillProviders(self.ui.providerComboBox)
        
        #self.ui.providerComboBox.setCurrentItem(self.config().readEntry(PROVIDER))
        #self.ui.usernameEdit.setText(self.config().readEntry(NAME))
        #self.ui.updateIntervalSpinBox.setValue(self.config().readEntry(UPDATE_INTERVAL, QVariant(0)).toInt()[0])
        
    def _items(self):
        self.im = ItemManager()
        self.im.createItem(QFont("Helvetica"), QColor("red"))
        self.im.createItem(QFont("Helvetica"), QColor("blue"))
        
    @pyqtSignature("configAccepted()")
    def configAccepted(self):
        cg = self.config()
        #self.items = self.itemList.items
        #TODO save items
        self.updateUi()
        
        #cg.writeEntry("provider", self.ui.providerComboBox.currentText())
        #cg.writeEntry("name", self.ui.usernameEdit.text())
        #cg.writeEntry("updateInterval", QVariant(self.ui.updateIntervalSpinBox.value()))
        
        self.emit(SIGNAL("configNeedsSaving()"))

    def paintInterface(self, painter, option, rect):
        self.l.draw(painter,rect)
        pass
        
      
def CreateApplet(parent):
    return BloatedClockApplet(parent)

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
        self.timeFormatter = TimeFormatter()
        
        self.x = False
        self.initGui()
        
        #Plasma.Theme.defaultTheme().connect(Plasma.Theme.defaultTheme(), SIGNAL("themeChanged()"), self, SLOT("slotThemeChanged()"))
    
        self.connectToEngine()
        
    def initGui(self):
        self.updateUi()
        #self.resize(250,250)
        
    def updateUi(self):
        try:
            xml = self.xmlEdit.xml()
        except:
            xml = """<clock>
    <line><item1 align="left">text %hh.%mm:%ss</item1><item2 align="right">2de text</item2></line>
    <line><item1 align="center">center</item1></line>
    <line><item2 align="right">right</item2></line>
    </clock>"""
        lBuilder = LayoutBuilder(self.im)
        self.l = lBuilder.build(xml)

#    @pyqtSignature("slotThemeChanged()")  
#    def themeChanged(self):
#        pass

    def connectToEngine(self):
        self.engine = self.dataEngine("time")
        self.engine.connectSource("Europe/Brussels", self, 333)
        
        
    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        time = data[QString("Time")].toTime()
        date = data[QString("Date")].toDate()
        self.timeFormatter.set(QDateTime(date, time))
        self.update()

        #if self.time.minute() == self.lastTimeSeen.minute() and \
        #self.time.second() == self.lastTimeSeen.second():
            # avoid unnecessary repaints
         #   return
            
          #  self.lastTimeSeen = self.time
           # self.update()
           
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
        self.l.draw(painter,rect, self.timeFormatter)
      
class TimeFormatter():
    reg = re.compile("%[a-zA-Z]+")
    def set(self, time):
        self.time = time
        
    def format(self, scheme):
        found = TimeFormatter.reg.findall(scheme)
        parts = TimeFormatter.reg.split(scheme)
        result = []
        if found == []:
            return parts[0]
        
        for (part, code) in zip(parts,found):
            result.append(str(part))
            result.append(str(self.time.toString(code[1:])))
        return "".join(result)
    
    
      
def CreateApplet(parent):
    return BloatedClockApplet(parent)

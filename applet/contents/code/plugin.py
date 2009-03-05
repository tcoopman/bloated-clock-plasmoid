'''
Created on Mar 5, 2009

@author: thomas
'''
import re
from PyQt4.QtCore import *

class PluginLoader(object):
    def __init__(self,  applet):
        self.plugins = {}
        self.plugins["clock"] = Clock 
        self._applet = applet
        
    def getPluginByName(self, name):
        pluginClass = self.plugins[name]
        plugin = pluginClass()
        plugin.hook = self._applet
        return plugin
        

class Plugin(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._output = "EMPTY"
        self.parseText = ""
        
    def load(self,  options):
        pass
    
    def parse(self, text):
        pass
        
    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        self.updateData(sourceName, data)
        self.hook.update()
        
    def updateData(self,  sourceName, data):
        pass
        
    @property
    def engine(self):
        return self._engine
        
    @engine.setter
    def engine(self,  value):
        self._engine = self.hook.dataEngine(value)
        
        
class Clock(Plugin):
    reg = re.compile("%[a-zA-Z]+")
    
    def __init__(self):
        Plugin.__init__(self)
        self.name = "clock"
        self.info = "this is a clock, you can use all formatting options from QDateTime from Qt4"
        
    def load(self, options):
        #A clock has no options at the moment, we could at regions later.
        #Here we can connect the dataengine
        self.engine = "time"
        print self.engine
        self.engine.connectSource("Europe/Brussels", self, 333)
        
    def parse(self,  text):
        found = Clock.reg.findall(text)
        parts = Clock.reg.split(text)
        result = []
        if found == []:
            return parts[0]
        else:
            for (part, code) in zip(parts,found):
                result.append(str(part))
                result.append(str(self.dateTime.toString(code[1:])))
            return "".join(result)
        
    def updateData(self,  sourceName,  data):
        time = data[QString("Time")].toTime()
        date = data[QString("Date")].toDate()
        self.dateTime = QDateTime(date, time)

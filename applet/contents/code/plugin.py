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
        
    def updateData(self,  sourceName, data):
        pass
        
    @property
    def output(self):
        return self._output
        
    @output.setter
    def output(self,  value):
        self._output = value
        self.hook.update()
        
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
        self.parseText = text
        
    def updateData(self,  sourceName,  data):
        if self.parseText:
            time = data[QString("Time")].toTime()
            date = data[QString("Date")].toDate()
            dateTime = QDateTime(date, time)
            found = Clock.reg.findall(self.parseText)
            parts = Clock.reg.split(self.parseText)
            result = []
            if found == []:
                self.output = parts[0]
            else:
                for (part, code) in zip(parts,found):
                    result.append(str(part))
                    result.append(str(dateTime.toString(code[1:])))
                self.output = "".join(result)

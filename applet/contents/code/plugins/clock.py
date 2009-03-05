import re
import sys
print sys.path
sys.path.append("/home/thomas/Workspace/bloated-clock/src/applet/contents/code/")
import plugin
print(dir(plugin))

class Clock(Plugin):
    reg = re.compile("%[a-zA-Z]+")
    
    def __init__(self):
        self.name = "clock"
        self.info = "this is a clock, you can use all formatting options from QDateTime from Qt4"
        self.engine("time")
        
    def load(self, options):
        #A clock has no options at the moment, we could at regions later.
        #Here we can connect the dataengine
        self.engine.connectSource("Europe/Brussels", self, 333)
        
    def parse(self,  text):
        self.parseText = text
        
    def dataUpdated(self,  sourceName,  data):
        time = data[QString("Time")].toTime()
        date = data[QString("Date")].toDate()
        dateTime = QDateTime(date, time)
        found = TimeFormatter.reg.findall(self.parseText)
        parts = TimeFormatter.reg.split(self.parseText)
        result = []
        if found == []:
            self.output = parts[0]
        
        for (part, code) in zip(parts,found):
            result.append(str(part))
            result.append(str(self.time.toString(code[1:])))
        self.output = "".join(result)

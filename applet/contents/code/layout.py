# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QRectF
from PyKDE4.plasma import Plasma

from xml.etree.cElementTree import XML

class LayoutBuilder():
    def __init__(self, im,  pl):
        self.im = im
        self.pl = pl
        self.plugins = {}
        self.trb = TextRendererBuilder()
        
    def build(self, xml, parent):
        self.tree = XML(self._surround(xml))
        self._readPlugins(self.tree.find("plugins"))
        return self._readBody(self.tree.find("body"),  parent)
            
    def _buildLine(self, element,  parent):
        line = QGraphicsLinearLayout(Qt.Horizontal, parent)
        for e in element:
            line.addItem(self._buildLabel(e))
        return line
            
    def _buildLabel(self, element):
        item = self.im.getItemByName(element.tag)
        plugin = self.plugins[element.get('parser')]
        return self.trb.build(item, plugin, element.text, element.get("align"))
        
    def _readPlugins(self,  xml):
        for element in xml:
            plugin = self.pl.getPluginByName(element.tag)
            self.plugins[element.get("name")] = plugin
            optionKeys = element.keys()
            optionKeys.remove("name")
            options = {}
            for key in optionKeys:
                options[key] = element.get(key)
            plugin.load(options)
            print "LOADED PLUGIN"
            
    def _readBody(self,  xml,  parent):
        layout = QGraphicsLinearLayout(Qt.Vertical, parent)
        for element in xml.getiterator("line"):
            print "parsing line"
            layout.addItem(self._buildLine(element,  layout))
        return layout
        
    
    def _surround(self,  xml):
        print xml
        return "<all>" + xml + "</all>"
    

#class Layout(QGraphicsLinearLayout):
#    def __init__(self, parent):
#        QGraphicsLinearLayout.__init__(self,  parent)
#    
#class VLayout(Layout):
#    def __init__(self,  parent):
#        Layout.__init__(self, parent)
#        self.setOrientation(Qt.Vertical)
#        
##    def _updateRects(self,rect):
##        itemCount = len(self.items)
##        height = rect.height()/ itemCount
##        rect = QRectF(rect.left(), rect.top(), rect.width(), height)
##        self.items[0].setRect(rect)
##        for (item,i) in zip(self.items, range(1,itemCount)):
##            rect = QRectF(rect.left(), rect.bottom(), rect.width(), height)
##            self.items[i].setRect(rect)    
#            
#class HLayout(Layout):
#     def __init__(self,  parent):
#        Layout.__init__(self, parent)
#        self.setOrientation(Qt.Horizontal)
#        
##    def _updateRects(self,rect):
##        itemCount = len(self.items)
##        width = rect.width()/ itemCount
##        rect = QRectF(rect.left(), rect.top(), width, rect.height())
##        self.items[0].setRect(rect)
##        for (item,i) in zip(self.items, range(1,itemCount)):
##            rect = QRectF(rect.right(), rect.top(), width, rect.height())
##            self.items[i].setRect(rect)
            
            
class TextRenderer(Plasma.Label):
    def __init__(self, value):
        Plasma.Label.__init__(self)
        self.value = value
        

class TextRendererBuilder():
    aligndict = {"left":Qt.AlignLeft, "right":Qt.AlignRight, "center":Qt.AlignCenter}
    def build(self, item, parser,  text,  align):
        label = TextRenderer(text)
        #parser.addOutput(label)
        label.setText("dummy")
        label.setStyleSheet(self._buildStyleSheet(item))
        return label
            
    def _buildStyleSheet(self, item):
        result = []
        result.append("color: ")
        result.append(str(item.color.name()))
        result.append(";\n")
        result.append('font-family: "')
        result.append(str(item.font.family()))
        result.append('";\n')
        result.append("font-size: ")
        result.append(str(item.font.pointSize()))
        result.append("pt;\n")
        result.append("font-style: ")
        result.append(str(item.font.style()))
        result.append(";\n")
        result.append("font-weight: ")
        result.append(str(item.font.weight()))
        result.append(";")
        return "".join(result)
        
    def _alignToFlag(self, align):
        return TextRenderer.aligndict[align]
    

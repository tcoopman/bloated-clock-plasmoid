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
        
    def build(self, xml):
        self.tree = XML(self._surround(xml))
        self._readPlugins(self.tree.find("plugins"))
        return self._readBody(self.tree.find("body"))
            
    def _buildLine(self, element):
        line = HLayout()
        for e in element:
            line.addItem(self._buildLabel(e))
        return line
            
    def _buildLabel(self, element):
        item = self.im.getItemByName(element.tag)
        plugin = self.plugins[element.get('parser')]
        plugin.parse(element.text)
        print plugin
        print plugin.parseText
        return TextRenderer(item, plugin, element.get("align"))
        
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
            
    def _readBody(self,  xml):
        layout = VLayout()
        for element in xml.getiterator("line"):
            print "parsing line"
            layout.addItem(self._buildLine(element))
        return layout
        
    
    def _surround(self,  xml):
        print xml
        return "<all>" + xml + "</all>"
    
class LayoutItem:
    def setRect(self, rect):
        self.rect = rect
        
    def draw(self, painter):
        pass
    

class Layout(LayoutItem):
    def __init__(self):
        self.items = []
        
    def addItem(self, item):
        self.items.append(item)
        
    def _updateRects(self,rect):
        pass
    
    def draw(self, painter, rect):
        self._updateRects(rect)
        for item in self.items:
            item.draw(painter, item.rect)
    
class VLayout(Layout):
    def _updateRects(self,rect):
        itemCount = len(self.items)
        height = rect.height()/ itemCount
        rect = QRectF(rect.left(), rect.top(), rect.width(), height)
        self.items[0].setRect(rect)
        for (item,i) in zip(self.items, range(1,itemCount)):
            rect = QRectF(rect.left(), rect.bottom(), rect.width(), height)
            self.items[i].setRect(rect)    
            
class HLayout(Layout):
    def _updateRects(self,rect):
        itemCount = len(self.items)
        width = rect.width()/ itemCount
        rect = QRectF(rect.left(), rect.top(), width, rect.height())
        self.items[0].setRect(rect)
        for (item,i) in zip(self.items, range(1,itemCount)):
            rect = QRectF(rect.right(), rect.top(), width, rect.height())
            self.items[i].setRect(rect)
            
            
class TextRenderer(LayoutItem):
    aligndict = {"left":Qt.AlignLeft, "right":Qt.AlignRight, "center":Qt.AlignCenter}
    def __init__(self, item, parser, align):
        self.item = item
        self.parser = parser
        self.align = self._alignToFlag(align)
        
    def draw(self, painter, rect):
        painter.setPen(self.item.color)
        painter.setFont(self.item.font)
        painter.drawText(rect, (Qt.TextDontClip | self.align), self.parser.output)
        
    def _alignToFlag(self, align):
        return TextRenderer.aligndict[align]

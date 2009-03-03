# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt, QRectF
from PyKDE4.plasma import Plasma

from xml.etree.cElementTree import XML


class LayoutBuilder():
    def __init__(self, im):
        self.im = im
        
    def build(self, xml):
        self.tree = XML(xml)
        layout = VLayout()
        for element in self.tree:
            layout.addItem(self._buildLine(element, layout))
        return layout
            
    def _buildLine(self, element, parent):
        line = HLayout()
        for e in element:
            line.addItem(self._buildLabel(e))
        return line
            
    def _buildLabel(self, element):
        item = self.im.getItemByName(element.tag)
        return TextFormat(item, element.text, element.get("align"))
    
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
    
    def draw(self, painter, rect,timeFormatter):
        self._updateRects(rect)
        for item in self.items:
            item.draw(painter, item.rect, timeFormatter)
    
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
            
            
class TextFormat(LayoutItem):
    aligndict = {"left":Qt.AlignLeft, "right":Qt.AlignRight, "center":Qt.AlignCenter}
    def __init__(self, item, text, align):
        self.item = item
        self.text = text
        self.align = self._alignToFlag(align)
        
    def draw(self, painter, rect, timeFormatter):
        text = timeFormatter.format(self.text)
        painter.setPen(self.item.color)
        painter.setFont(self.item.font)
        painter.drawText(rect, (Qt.TextDontClip | self.align), text)
        
    def _alignToFlag(self, align):
        return TextFormat.aligndict[align]
        
    
class MyLabel(Plasma.Label):
    def __init__(self, text):
        Plasma.Label.__init__(self)
        self.setText(text)
        self._text = text
    
#class LabelBuilder():
#    def build(self, item, text):
#        label = MyLabel(text)
#        label.setStyleSheet(self._buildStyleSheet(item))
#        return label
#            
#    def _buildStyleSheet(self, item):
#        result = []
#        result.append("color: ")
#        result.append(str(item.color.name()))
#        result.append(";\n")
#        result.append('font-family: "')
#        result.append(str(item.font.family()))
#        result.append('";\n')
#        result.append("font-size: ")
#        result.append(str(item.font.pointSize()))
#        result.append("pt;\n")
#        result.append("font-style: ")
#        result.append(str(item.font.style()))
#        result.append(";\n")
#        result.append("font-weight: ")
#        result.append(str(item.font.weight()))
#        result.append(";")
#        return "".join(result)
#          
#            
#        
#if __name__ == "__main__":
#    xml = """<clock>
#    <line><left><item1>text</item1></left></line>
#    <line></line>
#    </clock>"""
#    #layout = QGraphicsLinearLayout()
#    layoutBuilder = LayoutBuilder(None)
#    layoutBuilder.buildLayout(xml)
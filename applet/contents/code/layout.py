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
            
    def _readBody(self,  xml,  parent):
        layout = QGraphicsLinearLayout(Qt.Vertical, parent)
        for element in xml.getiterator("line"):
            print "parsing line"
            layout.addItem(self._buildLine(element,  layout))
        return layout
        
    def _surround(self,  xml):
        print xml
        return "<all>" + xml + "</all>"
            
            
class TextRenderer(Plasma.Label):
    def __init__(self, value):
        Plasma.Label.__init__(self)
        self.value = value
        

class TextRendererBuilder():
    aligndict = {"left":Qt.AlignLeft, "right":Qt.AlignRight, "center":Qt.AlignCenter}
    def build(self, item, parser,  text,  align):
        label = TextRenderer(text)
        parser.addOutput(label)
        label.setText("dummy")
        label.setStyleSheet(self._buildStyleSheet(item))
        label.setAlignment(self._alignToFlag(align))
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
        return TextRendererBuilder.aligndict[align]
    

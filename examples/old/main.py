#!/usr/bin/env python3

import sys
from PySide import QtGui, QtCore

TABLE_X = 480
TABLE_Y = 360
CARD_W = 64
CARD_H = 89

class Card(QtGui.QGraphicsRectItem):
  def __init__(self, pos, face_up=False, parent=None):
    super(Card, self).__init__(parent)
    self.face_up = face_up
    x,y = pos.x(), pos.y()
    self.setBrush(QtGui.QBrush('#FF0000', QtCore.Qt.SolidPattern))
    self.setRect(x, y, CARD_W, CARD_H)

    self.setAcceptDrops(True)
    self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
    self.setCursor(QtCore.Qt.OpenHandCursor)

  def contextMenuEvent(self, event):
    menu = QtGui.QMenu()
    menu.addAction('Flip card', self.flip)
    menu.addAction('Delete card', self.destroy)
    menu.exec_(event.screenPos())

  def bringToFront(self):
    n = max([item.zValue() for item in self.scene().items()])
    self.setZValue(n+.1)

  def mousePressEvent(self, event):
    super(Card, self).mousePressEvent(event)
    self.bringToFront()
    if event.button() == QtCore.Qt.LeftButton:
      self.setCursor(QtCore.Qt.ClosedHandCursor)

  def mouseReleaseEvent(self, event):
    super(Card, self).mouseReleaseEvent(event)
    self.setCursor(QtCore.Qt.OpenHandCursor)

  def flip(self):
    self.face_up = not self.face_up

    if self.face_up:
      self.setBrush(QtGui.QBrush('#FFFFFF', QtCore.Qt.SolidPattern))
    else:
      self.setBrush(QtGui.QBrush('#FF0000', QtCore.Qt.SolidPattern))

  def destroy(self):
    self.setParentItem(None)
    self.scene().removeItem(self)

class Table(QtGui.QGraphicsScene):
  def __init__(self, parent=None):
    super(Table, self).__init__(parent)
    self.setSceneRect(0,0,TABLE_X,TABLE_Y)
    self.setBackgroundBrush(QtGui.QBrush('#004400', QtCore.Qt.SolidPattern))
    self.text = self.addSimpleText("Hello World!")
    self.text.setBrush(QtGui.QColor('#FFFF00'))
    
  def contextMenuEvent(self, event):
    item = self.mouseGrabberItem()
    if item:
      item.ungrabMouse()
      item.contextMenuEvent(event)
    else:
      menu = QtGui.QMenu()
      menu.addAction('Add 1 random card', lambda: self.addCard(event.scenePos()))
      menu.exec_(event.screenPos())

  def addCard(self, scenePos):
    self.addItem(Card(scenePos))

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)

  v = QtGui.QGraphicsView()
  v.setScene(Table())

  w = QtGui.QMainWindow()
  w.setCentralWidget(v)
  w.setWindowTitle("Cards")
  w.statusBar()
  w.show()

  sys.exit(app.exec_())

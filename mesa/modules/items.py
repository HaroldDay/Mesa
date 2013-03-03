from PySide import QtGui, QtCore

class MesaItem(QtGui.QGraphicsPixmapItem):
  ''' base class for all objects '''
  def __init__(self, contextMenu, parent=None, scene=None):
    super(MesaItem, self).__init__(parent, scene)
    self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
    self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
    self.contextMenu = contextMenu

  def contextMenuEvent(self, event):
    self.contextMenu.exec_(event.screenPos())
    self.ungrabMouse()

  def flip(self):
    pass

class Card(MesaItem):
  def __init__(self, (front, back), *args, **kwargs):
    super(Card, self).__init__(*args, **kwargs)
    self.face_up = False
    self.frontPixmap = QtGui.QPixmap(front)
    self.backPixmap = QtGui.QPixmap(back)
    self.update()
    self.setZValue(10)

  def mouseDoubleClickEvent(self, event):
    if event.button() == QtCore.Qt.MouseButton.LeftButton:
      self.flip()

  def flip(self):
    self.face_up = not self.face_up
    self.update()

  def update(self):
    if self.face_up:
      self.setPixmap(self.frontPixmap)
    else:
      self.setPixmap(self.backPixmap)
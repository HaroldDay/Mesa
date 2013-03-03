from PySide import QtGui, QtCore

class Table(QtGui.QGraphicsScene):
  def __init__(self, itemMenu, parent=None):
    super(Table, self).__init__(parent)

    self.itemMenu = itemMenu

  def setBackgroundTile(self, image):
    tile = QtGui.QPixmap(image)
    brush = QtGui.QBrush(tile)
    self.setBackgroundBrush(brush)

  def mousePressEvent(self, event):
    super(Table, self).mousePressEvent(event)

    if event.button() == QtCore.Qt.MouseButton.LeftButton:
      clicked_item = self.mouseGrabberItem()
      if not clicked_item:
        self.sel_rect = SelRect(
          rect=QtCore.QRectF(event.scenePos(), event.scenePos()),
          scene=self,parent=None)

  def mouseMoveEvent(self, event):
    super(Table, self).mousePressEvent(event)

    try:
      self.sel_rect.stretch_to(event.scenePos())
    except AttributeError:
      pass

  def mouseReleaseEvent(self, event):
    super(Table, self).mouseReleaseEvent(event)

    try:
      for item in self.collidingItems(self.sel_rect):
        item.setSelected(True)
      del self.sel_rect
    except AttributeError:
      pass

  def keyPressEvent(self, event):
    super(Table, self).keyPressEvent(event)
    key = event.key()

    try:
      n = int(chr(key))
      self.parent().pick(n)
      return
    except ValueError:
      pass

    shift_pressed = QtGui.QApplication.keyboardModifiers()==QtCore.Qt.ShiftModifier
    action = self.spread if shift_pressed else self.move
    if key == QtCore.Qt.Key_Right:  action( 3, 0)
    elif key == QtCore.Qt.Key_Left: action(-3, 0)
    elif key == QtCore.Qt.Key_Down: action( 0, 3)
    elif key == QtCore.Qt.Key_Up:   action( 0,-3)

  def sorted_selection(self):
    ''' returns items in 'insertion order' ie: last item drawn on top '''
    return [item for item in self.items() if item in self.selectedItems()]

  def bring_to_top(self, item):
    ''' really more of a "put rest under" method... '''
    all_items = self.items()[::-1]
    idx = all_items.index(item)
    for top_item in all_items[idx+1:]:
      top_item.stackBefore(item)

  def move(self, dx, dy):
    for item in self.selectedItems():
      item.moveBy(dx*2, dy*2)

  def spread(self, dx, dy):
    for i, item in enumerate(self.sorted_selection()[::-1]):
      item.moveBy(i*dx, i*dy)

class SelRect(QtGui.QGraphicsRectItem):
  def __init__(self, rect, parent, scene):
    super(SelRect, self).__init__(rect, parent, scene)
    self.origin = self.rect().topLeft()
    self.setZValue(100)

    self.setPen(QtGui.QPen(QtGui.QColor(0,0,255, 100)))
    self.setBrush(QtGui.QBrush(QtGui.QColor(0,0,255,100)))

  def stretch_to(self, point):
    self.setRect(QtCore.QRectF(self.origin, point).normalized())
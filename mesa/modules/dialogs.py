import inspect
from PyQt4 import QtGui, QtCore

import items

class PreviewWidget(QtGui.QWidget):
  def __init__(self):
    super(PreviewWidget, self).__init__()

    self.setLayout(QtGui.QGridLayout())
    self.init_screen()
    self.init_controls()

  def init_screen(self):
    self.scene = QtGui.QGraphicsScene()
    self.scene.setBackgroundBrush(QtGui.QBrush('#AAAAAA', QtCore.Qt.DiagCrossPattern))

    self.view = QtGui.QGraphicsView(self.scene)
    self.view.setMinimumSize(300,300)

    self.layout().addWidget(self.view,0,0,1,-1)

  def init_controls(self):
    self.ITEM_TYPE = QtGui.QComboBox()
    self.ITEM_TYPE.currentIndexChanged.connect()
    for name, item in inspect.getmembers(items, inspect.isclass):
      self.ITEM_TYPE.addItem(name, item)

    self.layout().addWidget(self.ITEM_TYPE)

  def preview(self, path):
    source_pix = QtGui.QGraphicsPixmapItem(path)
    self.scene.clear()
    self.scene.setSceneRect(source_pix.boundingRect())
    self.scene.addItem(source_pix)


class LoadTextureDialog(QtGui.QFileDialog):
  def __init__(self, *args, **kwargs):
    super(LoadTextureDialog, self).__init__(filter="Texture Files (*.png)", *args, **kwargs)
    self.preview_widget = PreviewWidget()
    self.layout().addWidget(self.preview_widget, 0, 10, -1, 1)
    self.currentChanged.connect(self.preview_widget.preview)

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)

  d = LoadTextureDialog()
  d.show()

  sys.exit(app.exec_())

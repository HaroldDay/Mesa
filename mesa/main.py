import random
from PySide import QtGui, QtCore

from lib.items import *
from lib.surfaces import *

SIZE = 200

class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.createActions()
    self.createMenus()
    self.status_bar = self.statusBar()

    self.scene = Table(self.itemMenu, self)
    self.scene.setSceneRect(QtCore.QRectF(0, 0, 500, 500))
    self.scene.selectionChanged.connect(self.show_n_selected)

    self.view = QtGui.QGraphicsView(self.scene)
    self.setCentralWidget(self.view)

    self.setGeometry(100,100,4*SIZE,3*SIZE)
    self.setWindowTitle("Mesa")

  def createActions(self):
    self.selectAllAction= QtGui.QAction("Select All",     self, triggered=self.select_all,shortcut="Ctrl+A", statusTip="Select all")
    self.topAction      = QtGui.QAction("Bring To &Top",  self, triggered=self.top,       shortcut="T",      statusTip="Bring items to top",)
    self.flipAction     = QtGui.QAction("&Flip",          self, triggered=self.flip,      shortcut="F",      statusTip="Flip items")
    self.stackAction    = QtGui.QAction("&Stack",         self, triggered=self.stack,     shortcut="S",      statusTip="Stack like items")
    self.shuffleAction  = QtGui.QAction("Shuffle",        self, triggered=self.shuffle,   shortcut="Shift+S",statusTip="Shuffle like items")
    self.pickAction     = QtGui.QAction("&Pick top...",   self, triggered=self.pick,      shortcut="P",      statusTip="Pick from top of stack")
    self.dropAction     = QtGui.QAction("&Drop bottom...",self, triggered=self.drop,      shortcut="D",      statusTip="Drop from bottom of stack")
    self.dealAction     = QtGui.QAction("Deal",           self, triggered=self.deal,      shortcut="Shift+D",statusTip="Deal items")
    self.deleteAction   = QtGui.QAction("&Delete",        self, triggered=self.delete,    shortcut="Delete", statusTip="Remove object from table")

    self.loadAction     = QtGui.QAction("&Load", self, triggered=self.load, shortcut="Ctrl+O", statusTip="Load textured objects")
    self.exitAction     = QtGui.QAction("E&xit", self, triggered=self.close,shortcut="Ctrl+X", statusTip="Quit")

  def createMenus(self):
    self.fileMenu = self.menuBar().addMenu("&File")
    self.fileMenu.addAction(self.loadAction)
    self.fileMenu.addAction(self.exitAction)

    self.itemMenu = self.menuBar().addMenu("&Item")
    self.itemMenu.addAction(self.selectAllAction)
    self.itemMenu.addAction(self.topAction)
    self.itemMenu.addAction(self.flipAction)
    self.itemMenu.addAction(self.stackAction)
    self.itemMenu.addAction(self.shuffleAction)
    self.itemMenu.addAction(self.pickAction)
    self.itemMenu.addAction(self.dropAction)
    self.itemMenu.addAction(self.dealAction)

  def load(self):
    path = QtGui.QFileDialog.getOpenFileName(self, "Load Texture", '', "Image Files (*.png *.jpg)")[0]
    if not path:
      return

    try:
      source_pix = QtGui.QPixmap(path)
      data = path.split('.')[0].split('/')[-1].split('_')

      item_type = data[0]
      w,h = map(int,data[1].split('x'))
      N = int(data[2])
      Nx = source_pix.width()/w
      Ny = source_pix.height()/h

      assert Nx*w == source_pix.width()
      assert Ny*h == source_pix.height()
      assert Nx*Ny > N

      coords = [(i%Nx*w, (i/Nx)%Ny*h) for i in range(N)]
      pix_list = [source_pix.copy(x,y,w,h) for (x,y) in coords]

      if item_type == 'Card':
        back_idx = int(data[3])-1
        back_pix = pix_list[back_idx]
        for n, pix in enumerate(pix_list):
          if n != back_idx:
            self.scene.addItem(Card((pix,back_pix),self.itemMenu))

    finally:
      pass


  def select_all(self):
    for item in self.scene.items():
      item.setSelected(True)
  
  def top(self):
    for item in self.scene.sorted_selection()[::-1]:
      self.scene.bring_to_top(item)
    self.scene.update()

  def flip(self):
    for item in self.scene.selectedItems():
      item.flip()

  def stack(self):
    for item in self.scene.selectedItems():
      try:
        item.setPos(self.scene.mouseGrabberItem().scenePos())
      except AttributeError:
        item.setPos(self.scene.sorted_selection()[-1].scenePos())

    self.statusBar().showMessage("%i items stacked" % len(self.scene.selectedItems()))

  def shuffle(self):
    item_list = self.scene.sorted_selection()
    random.shuffle(item_list)
    for i, item in enumerate(item_list):
      item.stackBefore(item_list[i-1])
    self.scene.update()
    self.statusBar().showMessage("Items shuffled")

  def pick(self, n=None):
    selected_items = self.scene.sorted_selection()
    self.scene.clearSelection()
    if n==None:
      n, choice = QtGui.QInputDialog.getInteger(self, "Pick items",
                  "Number of items:", 0, 0, len(selected_items))

    for item in selected_items[:n]:
      item.setSelected(True)

  def drop(self, n=None):
    selection = self.scene.sorted_selection()
    if selection: selection[-1].setSelected(False)

  def deal(self):
    if not self.selection_is_stack():
      self.statusBar().showMessage("You must deal from a stack")
      return

    item = self.scene.sorted_selection()[0]
    width = item.boundingRect().width()
    self.scene.bring_to_top(item)
    
    item.moveBy(width,0)
    item.flip()
    item.setSelected(False)

  def delete(self):
    for item in self.scene.selectedItems():
      self.scene.removeItem(item)

  def selection_is_stack(self):
    pos_list = [item.scenePos() for item in self.scene.selectedItems()]
    if pos_list:
      return pos_list.count(pos_list[0])==len(pos_list)

  def show_n_selected(self):
    self.statusBar().showMessage("%i items selected" % len(self.scene.selectedItems()))

def main():
  import sys

  app = QtGui.QApplication(sys.argv)

  m = MainWindow()
  m.show()

  sys.exit(app.exec_())

if __name__ == '__main__':
  from tests import load_img_test as current_test

  current_test.main()
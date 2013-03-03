import sys
import numpy as np
from PySide import QtGui, QtCore

_TITLE = 'MatrixSeeder'
_VERSION = 0.0

class MatrixCanvas(QtGui.QWidget):
  def __init__(self, parent=None):
    super(MatrixCanvas, self).__init__(parent)

    self.mat = np.zeros([50,50])
    self.t = 20
    self.size = QtCore.QSize(*[d*self.t for d in self.mat.shape])

    self.parent().setFixedSize(self.size)

  def paintEvent(self, event):
    painter = QtGui.QPainter(self)

    for (x,y),val in np.ndenumerate(self.mat):

      if val == 1:
        cf = '#4444AA'
        cl = '#444488'

      elif val == 0:
        cf = '#004400'
        cl = '#002200'

      painter.setPen(cl)
      painter.fillRect(x*self.t, y*self.t, self.t, self.t, cf)
      painter.drawRect(x*self.t, y*self.t, self.t, self.t)

  def mousePressEvent(self, event):
    x,y = event.x()/self.t, event.y()/self.t

    self.newval = not self.mat[x,y]
    self.mat[x,y] = self.newval
    self.repaint()
    
  def mouseMoveEvent(self, event):
    x,y = event.x()/self.t, event.y()/self.t
    if x<0 or y<0:
      return

    try:
      self.mat[x,y] = self.newval
    except IndexError:
      return

    self.repaint()


def main():
  app = QtGui.QApplication(sys.argv)

  w = QtGui.QMainWindow()
  w.setWindowTitle("%s %s" % (_TITLE, _VERSION))
  w.show()

  c = MatrixCanvas(w)
  w.setCentralWidget(c)

  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
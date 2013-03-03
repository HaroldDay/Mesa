import res
from PySide import QtGui

if __name__ == '__main__':
  app = QtGui.QApplication([])

  pix = QtGui.QPixmap(':/cars.png')

  w = QtGui.QLabel()
  w.setPixmap(pix)
  w.setGeometry(100,100,100,100)
  w.show()



  app.exec_()

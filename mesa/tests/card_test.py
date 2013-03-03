import sys

sys.path.append('/home/roderic/Desktop/Mesa/mesa/')
from main import *

from PySide.QtGui import *
import card_test_rc


def main():
  app = QApplication(sys.argv)

  m = MainWindow()
  m.scene.setBackgroundTile(':/images/baize.png')
  m.show()

  for i in range(5):
    m.scene.addItem(Card(
    front=':/images/card_front.png',
    back =':/images/card_back.png',
    contextMenu=m.scene.itemMenu))

  sys.exit(app.exec_())
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

  N = 55
  NX = 13
  NY = 5 
  W = 79
  H = 123

  card_image_list = []
  pix = QPixmap('tests/load_img_test.png')
  for i in range(N):
    card_image_list.append(pix.copy(i%NX*W, i/NX%NY*H, W, H))

  for i in range(N-3):
    m.scene.addItem(Card((card_image_list[i], card_image_list[-1]), contextMenu=m.scene.itemMenu))

  sys.exit(app.exec_())
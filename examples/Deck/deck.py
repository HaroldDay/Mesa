import random
import textwrap
from PySide import QtGui

RATIO = 79./123.
SIZE = 300

XSIZE = SIZE*RATIO
YSIZE = SIZE

CSS = '''
QPushButton {
  font-size: 30px;
  color: black;
  background-color: %s;
}
'''
class Card(dict):
  def __init__(self, text, color):
    super(Card, self).__init__()
    self.text = text
    self.color = color

class Deck(QtGui.QWidget):
  def __init__(self):
    super(Deck, self).__init__()
    self.cards = []
    self.discards = []

    self.init_UI()

  def init_UI(self):
    grid = QtGui.QGridLayout()

    self.deal_button = QtGui.QPushButton()
    self.deal_button.setFixedSize(XSIZE,YSIZE)
    self.deal_button.clicked.connect(self.deal)
    grid.addWidget(self.deal_button,1,0)

    self.discard_pile = QtGui.QPushButton()
    self.discard_pile.setFixedSize(XSIZE,YSIZE)
    self.discard_pile.clicked.connect(self.shuffle)
    grid.addWidget(self.discard_pile,1,1)

    self.setLayout(grid)
    self.update_UI()

  def load_cards(self, path):
    with open(path, 'rb') as f:
      for line in f:
        data = line.strip().split(',')
        for _ in range(int(data[0])):
          self.cards.append(Card(*data[1:]))
    random.shuffle(self.cards)
    self.update_UI()

  def update_UI(self):
    if self.cards:
      self.deal_button.setText("%i" % len(self.cards))
    else:
      self.deal_button.setText("Empty")

    if self.discards:
      card = self.discards[-1]
      self.discard_pile.setText(textwrap.fill(card.text, 11))
      self.discard_pile.setStyleSheet(CSS % card.color)
    else:
      self.discard_pile.setStyleSheet(None)
      self.discard_pile.setText("Empty")

  def deal(self, n=1):
    if self.cards:
      self.discards.append(self.cards.pop())

    self.update_UI()

  def shuffle(self):
    question = "Shuffle?"
    reply = QtGui.QMessageBox.question(self, None, question,
                  QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
      self.cards = self.cards+self.discards
      random.shuffle(self.cards)
      self.discards = []

    self.update_UI()        

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)

  deck = Deck()
  deck.load_cards('resources.txt')
  deck.show()

  sys.exit(app.exec_())


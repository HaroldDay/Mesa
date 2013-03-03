import time
import socket
from PySide import QtCore, QtGui, QtNetwork

USER = socket.gethostname()
HOST = QtNetwork.QHostAddress.Broadcast
PORT = 45454

class Chat(QtGui.QWidget):
  def __init__(self):
    super(Chat, self).__init__()
    self.setWindowTitle("Chat")

    self.initUi()
    self.initNetwork()

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_Return:
      self.sendMessage()
      return

    super(Chat, self).keyPressEvent(event)

  def initUi(self):
    QtGui.QGridLayout(self)

    self.textView = QtGui.QTextEdit()
    self.textView.setReadOnly(True)
    self.lineEdit = QtGui.QLineEdit()

    self.layout().addWidget(self.textView)
    self.layout().addWidget(self.lineEdit)

  def sendMessage(self):
    message = self.lineEdit.text().strip()
    ts = time.strftime("%H:%M:%S", time.localtime())

    datagram = "[%s] <b>%s:</b> %s" % (ts, USER, str(message))

    if datagram:
      self.udpSocket.writeDatagram(datagram, HOST, PORT)
      self.lineEdit.clear()
      self.lineEdit.setFocus()

  def listen(self):
    while self.udpSocket.hasPendingDatagrams():
      message, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
      message = str(message)

      if message:
        self.textView.append(message)

  def initNetwork(self):
    self.udpSocket = QtNetwork.QUdpSocket(self)
    self.udpSocket.bind(PORT)
    self.udpSocket.readyRead.connect(self.listen)

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)

  chat = Chat()
  chat.show()

  sys.exit(app.exec_())
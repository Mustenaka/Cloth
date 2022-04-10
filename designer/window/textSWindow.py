from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from designer import TextS


class TextSWindow(QDialog):
 my_signal = pyqtSignal(str)
 def __init__(self):
  QDialog.__init__(self)
  self.setWindowModality(QtCore.Qt.ApplicationModal)
  self.child = TextS.Ui_Dialog()
  self.child.setupUi(self)
  self.child.buttonBox.accepted.connect(self.returnData)
 def returnData(self):
  string=self.child.lineEdit.text()
  self.my_signal.emit(string)

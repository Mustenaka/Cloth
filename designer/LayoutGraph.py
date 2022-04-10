from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsScene,QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
import numpy as np
import cv2
#这是继承QGraphicsScene的自定义类
class LayoutGraph(QtWidgets.QGraphicsView):
    doubleClick = QtCore.pyqtSignal(str)
    Click = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(LayoutGraph, self).__init__(parent)
        self.id=0
        self.img_path=""
        self.ifdelete=0
        self.ctime=0
    def mouseDoubleClickEvent(self,event):
        if(self.ifdelete==1):
            self.Click.emit(self.id)
        else:
            self.doubleClick.emit(self.img_path)

    def mousePressEvent(self, event):
        if(event.buttons() == QtCore.Qt.LeftButton):
            self.Click.emit(self.id)

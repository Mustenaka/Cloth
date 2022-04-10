import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
import numpy as np
import cv2
#这是继承QGraphicsScene的自定义类
class DragGraph(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(DragGraph, self).__init__(parent)
        self.background=None
    def mouseDoubleClickEvent(self,e):
        item = self.itemAt(e.pos())
        if(item!=self.background and self.background!=0):
            if (item):
                rotation=item.rotation()+90
                if(rotation>=360):
                    rotation=rotation-360
                print(item.boundingRect().width(),item.boundingRect().height())
                width=item.boundingRect().width()
                height=item.boundingRect().height()
                item.setRotation(rotation)
                item.setTransformOriginPoint(width//2, height//2)
                print(item.rotation())
                print(item.mapToScene(0,0).x(),item.mapToScene(0,0).y())
            else:
                print("no item!")











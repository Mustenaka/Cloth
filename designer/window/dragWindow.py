import os

import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem

from designer import dragG
from designer import DragGraph


class DragGWindow(QDialog):
 my_signal = pyqtSignal(str)
 value_signal = pyqtSignal(int,int)
 def __init__(self):
  QDialog.__init__(self)
  self.Dir=""
  self.front=""
  self.front2=""
  self.value=0
  self.hat=0
  self.hatValue=0
  self.hatValue2=0
  self.imgSize=[]
  self.frontSize=[]
  self.hatSize=[]
  self.f=1
  self.hat_pos=[]
  self.hat_ori=0
  self.child = dragG.Ui_Dialog()
  #self.child.setFixedSize(MainWindow.width(), MainWindow.height())
  #self.child.myDialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
  self.hatIMG=0
  self.child.graphicsView = DragGraph.DragGraph(self)
  self.child.graphicsView.setGeometry(QtCore.QRect(0, 0, 600, 600))
  #self.child.graphicsView.setMaximumSize(800,600)
  brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
  brush.setStyle(QtCore.Qt.SolidPattern)
  self.child.graphicsView.setBackgroundBrush(brush)
  self.child.graphicsView.setMouseTracking(True)
  self.child.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
  self.child.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
  self.child.graphicsView.setDragMode(QtWidgets.QGraphicsView.NoDrag)
  self.child.graphicsView.setObjectName("graphicsView")
  self.child.setupUi(self)
  self.child.buttonBox.accepted.connect(self.myAccept)

  self.child.graphicsView2 = DragGraph.DragGraph(self)
  self.child.graphicsView2.setGeometry(QtCore.QRect(0, 0, 600, 600))
  brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
  brush.setStyle(QtCore.Qt.SolidPattern)
  self.child.graphicsView2.setBackgroundBrush(brush)
  self.child.graphicsView2.setMouseTracking(True)
  self.child.graphicsView2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
  self.child.graphicsView2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
  self.child.graphicsView2.setDragMode(QtWidgets.QGraphicsView.NoDrag)
  self.child.graphicsView2.setObjectName("graphicsView2")
  self.child.graphicsView2.hide()

  self.child.horizontalSlider = QtWidgets.QSlider(self)
  self.child.horizontalSlider.setGeometry(QtCore.QRect(30, 430, 160, 22))
  self.child.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
  self.child.horizontalSlider.setObjectName("horizontalSlider")
  self.child.horizontalSlider_2 = QtWidgets.QSlider(self.child.myDialog)
  #self.child.horizontalSlider_2.setGeometry(QtCore.QRect(30, 400, 160, 22))
  self.child.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
  self.child.horizontalSlider_2.setObjectName("horizontalSlider_2")
  self.child.horizontalSlider_3 = QtWidgets.QSlider(self.child.myDialog)
  #self.child.horizontalSlider_3.setGeometry(QtCore.QRect(30, 370, 160, 22))
  self.child.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
  self.child.horizontalSlider_3.setObjectName("horizontalSlider_3")
  self.child.horizontalSlider_3.hide()
  self.child.horizontalSlider_2.hide()

  self.child.setupUi(self)
  self.child.buttonBox.accepted.connect(self.myAccept)
  self.child.horizontalSlider.valueChanged['int'].connect(self.valueChange)
  self.child.horizontalSlider_2.valueChanged['int'].connect(self.valueChange2)
  self.child.horizontalSlider_3.valueChanged['int'].connect(self.valueChange3)
 def processIMG(self,string):
  front_path=str(string)+"/front_X.png"
  print(front_path)
  backHat_path=str(string)+"/back_hat_new.png"
  graphview=self.child.graphicsView
  graphview2 = self.child.graphicsView2
  img=cv2.imread(os.path.join(string,"out/bigImage.jpg"),-1)
  front=cv2.imread(front_path,-1)
  if(os.path.exists(backHat_path)):
   self.hat=1
   back=cv2.imread(backHat_path,-1)
   self.hatSize=back.shape
   self.child.myDialog.resize(1200,700)
   graphview2.show()
   self.child.horizontalSlider_2.setEnabled(True)
  else:
   graphview2.hide()
   self.child.horizontalSlider_2.setEnabled(False)
   self.child.horizontalSlider_3.setEnabled(False)
   self.hat=0
  self.imgSize=img.shape
  self.frontSize=front.shape
  img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
  front = cv2.cvtColor(np.array(front), cv2.COLOR_BGRA2RGBA)
  f1=600.0/img.shape[1]
  f2=600.0/img.shape[0]
  self.f=f1 if f1<f2 else f2
  self.f=self.f if self.f<1 else 1
  graphview.setMinimumSize(int(img.shape[1]*self.f),int(img.shape[0]*self.f))
  graphview.setMaximumSize(int(img.shape[1]*self.f),int(img.shape[0]*self.f))
  if(self.hat):
   self.child.graphicsView2.setGeometry(QtCore.QRect(int(img.shape[1]*self.f), 0, int(img.shape[1]*self.f), int(img.shape[0]*self.f)))
  print(self.f)
  tmp=int(img.shape[1]*self.f)
  if(tmp<550):
   tmp=550
  self.child.myDialog.resize(tmp,int(img.shape[0]*self.f)+50)
  if(self.hat):
   self.child.myDialog.resize(int(img.shape[1] * self.f)*2, int(img.shape[0] * self.f) + 50)
  if (img.shape[2] == 4):
   frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
  elif (img.shape[2] == 3):
   frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
  # frame.setScaledSize(QSize(img.shape[1],img.shape[0]))
  pix = QPixmap.fromImage(frame)
  self.background = QGraphicsPixmapItem(pix)  # 创建像素图元
  self.background.setScale(self.f)
  graphview.background = self.background
  # self.item.setFlag(QGraphicsItem.ItemIsMovable)
  graphview.scene = QGraphicsScene()  # 创建场景
  graphview.scene.setSceneRect(0, 0, int(self.imgSize[1]*self.f), int(self.imgSize[0]*self.f))
  graphview.scene.addItem(self.background)


  if (front.shape[2] == 4):
   front[:,:,3]=front[:,:,3]*0.8
   frame = QImage(front, front.shape[1], front.shape[0], front.shape[1] * 4, QImage.Format_RGBA8888)
  elif (img.shape[2] == 3):
   frame = QImage(front, front.shape[1], front.shape[0], front.shape[1] * 3, QImage.Format_RGB888)
  pix = QPixmap.fromImage(frame)
  self.front = QGraphicsPixmapItem(pix)  # 创建像素图元
  self.front.setScale(self.f)
  graphview.background = self.front
  self.front.setY(int((img.shape[0] // 2-(front.shape[0]//2))*self.f))
  self.front.setX(int((img.shape[1] // 2-(front.shape[1]//2))*self.f))
  graphview.background=0
  graphview.scene.addItem(self.front)
  graphview.update()
  graphview.scene.update()
  graphview.setScene(graphview.scene)  # 将场景添加至视图
  #self.child.horizontalSlider_2.hide()
  ####################################hat
  if(self.hat):
   if (img.shape[2] == 4):
    frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
   elif (img.shape[2] == 3):
    frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
   pix = QPixmap.fromImage(frame)
   self.background = QGraphicsPixmapItem(pix)  # 创建像素图元
   self.background.setScale(self.f)
   graphview2.background = self.background

   if (front.shape[2] == 4):
    front[:,:,3]=front[:,:,3]*0.8
    frame = QImage(front, front.shape[1], front.shape[0], front.shape[1] * 4, QImage.Format_RGBA8888)
   elif (img.shape[2] == 3):
    frame = QImage(front, front.shape[1], front.shape[0], front.shape[1] * 3, QImage.Format_RGB888)
   pix = QPixmap.fromImage(frame)
   self.front2 = QGraphicsPixmapItem(pix)  # 创建像素图元
   self.front2.setScale(self.f)
   #graphview2.background = self.front2
   self.front2.setY(int((img.shape[0] // 2 - (front.shape[0] // 2)) * self.f))
   self.front2.setX(int((img.shape[1] // 2 - (front.shape[1] // 2)) * self.f))
   graphview2.scene = QGraphicsScene()  # 创建场景
   graphview2.scene.setSceneRect(0, 0, int(self.imgSize[1]*self.f), int(self.imgSize[0]*self.f))
   graphview2.scene.addItem(self.background)
   graphview2.scene.addItem(self.front2)

   if (back.shape[2] == 4):
    back[:, :, 3] = back[:, :, 3] * 0.8
    frame = QImage(back, back.shape[1], back.shape[0], back.shape[1] * 4, QImage.Format_RGBA8888)
   elif (front.shape[2] == 3):
    frame = QImage(back, back.shape[1], back.shape[0], back.shape[1] * 3, QImage.Format_RGB888)
   # frame.setScaledSize(QSize(img.shape[1],img.shape[0]))
   pix = QPixmap.fromImage(frame)
   self.hatIMG = QGraphicsPixmapItem(pix) # 创建像素图元
   self.hatIMG.setScale(self.f)
   #self.hatIMG.setFlag(QGraphicsItem.ItemIsMovable)

   #self.hatIMG.setY(int((self.imgSize[0] // 2) * self.f))
   #self.hatIMG.setX(int((self.imgSize[1] // 2 )*self.f))
   self.hat_ori = self.hatIMG.mapToScene(0,0).x()
   self.hatIMG.setFlag(QGraphicsItem.ItemIsMovable)
   graphview2.scene.setSceneRect(0, 0, int(self.imgSize[1]*self.f), int(self.imgSize[0]*self.f))
   graphview2.scene.addItem(self.hatIMG)
   graphview2.background=0
   graphview2.update()
   graphview2.scene.update()
   graphview2.setScene(graphview2.scene)  # 将场景添加至视图
  ##########################
  self.child.horizontalSlider.setGeometry(QtCore.QRect(0,graphview.height(), 200, 32))
  self.child.buttonBox.setGeometry(QtCore.QRect(210, graphview.height(), 160, 32))
  if(img.shape[1]==front.shape[1]):
   self.Dir="Vertical"
  else:
   self.Dir="Horizontal"

  if(self.Dir=="Horizontal"):
   left=(img.shape[1]-front.shape[1])//2
   print(left)
   self.child.horizontalSlider.setMinimum(0-left)
   self.child.horizontalSlider.setMaximum(left)
   self.child.horizontalSlider.setValue(0)
   if(self.hat):
    print(self.hatSize,self.imgSize)
    left=int((self.imgSize[0]//2))
    self.child.horizontalSlider_2.setMinimum(0-left)
    self.child.horizontalSlider_2.setMaximum(left-self.hatSize[0])
    self.child.horizontalSlider_2.setValue(0)
    self.child.horizontalSlider_2.setGeometry(QtCore.QRect(400, graphview.height(), 200, 32))
    left = int((self.imgSize[1] // 2))
    self.child.horizontalSlider_3.setMinimum(0-left)
    self.child.horizontalSlider_3.setMaximum(left-self.hatSize[1])
    self.child.horizontalSlider_3.setValue(0)
    self.child.horizontalSlider_3.setGeometry(QtCore.QRect(600, graphview.height(), 200, 32))
  if(self.Dir=="Vertical"):
   left=(img.shape[0]-front.shape[0])//2
   self.child.horizontalSlider.setMinimum(0-left)
   self.child.horizontalSlider.setMaximum(left)
   self.child.horizontalSlider.setValue(0)
   if(self.hat):
    left=int((self.imgSize[0]//2))
    self.child.horizontalSlider_2.setMinimum(0-left)
    self.child.horizontalSlider_2.setMaximum(left-self.hatSize[0])
    self.child.horizontalSlider_2.setValue(0)
    self.child.horizontalSlider_2.setGeometry(QtCore.QRect(400, graphview.height(), 200, 32))
    left = int((self.imgSize[1] // 2))
    self.child.horizontalSlider_3.setMinimum(0-left)
    self.child.horizontalSlider_3.setMaximum(left-self.hatSize[1])
    self.child.horizontalSlider_3.setValue(0)
    self.child.horizontalSlider_3.setGeometry(QtCore.QRect(600, graphview.height(), 200, 32))
 def valueChange(self):
  if(self.Dir=="Horizontal"):
   self.value=self.child.horizontalSlider.value()
   self.front.setX(int((self.imgSize[1] // 2 - (self.frontSize[1] // 2)+self.value)*self.f))
   if (self.hat):
    self.front2.setX(int((self.imgSize[1] // 2 - (self.frontSize[1] // 2)+self.value)*self.f))
    #self.hatIMG.setX(int((self.imgSize[1] // 2 - (self.frontSize[1] // 2) + self.value) * self.f))
  if(self.Dir=="Vertical"):
   self.value=self.child.horizontalSlider.value()
   self.front.setY(int((self.imgSize[0] // 2 - (self.frontSize[0] // 2)+self.value)*self.f))
   if(self.hat):
    #self.hatIMG.setY(int((self.imgSize[0] // 2 - (self.frontSize[0] // 2)+self.value-90)*self.f))
    self.front2.setY(int((self.imgSize[0] // 2 - (self.frontSize[0] // 2) + self.value) * self.f))
 def valueChange2(self):
  #print(self.child.horizontalSlider.value())
  if(self.hat):
   self.hatValue = self.child.horizontalSlider_2.value()
   self.hatIMG.setY(int((self.imgSize[0] // 2+self.hatValue)*self.f))
 def valueChange3(self):
  if(self.hat):
   self.hatValue2 = self.child.horizontalSlider_3.value()
   self.hatIMG.setX(int((self.imgSize[1] // 2+self.hatValue2)*self.f))
 def myAccept(self):
  if(self.Dir=="Horizontal"):
   if(self.hat):
    self.hat_pos = [int(self.hatIMG.mapToScene(0,0).x()/self.f),int(self.hatIMG.mapToScene(0,0).y()/self.f)]
    f = open('./tmp/hat.txt', 'w')
    f.write(str(self.hat_pos[0])+" "+str(self.hat_pos[1]))
    f.close()
   #print(self.hat_pos)
   #print(self.value)
   self.value_signal.emit(self.value,0)
  else:
   if(self.hat):
    self.hat_pos = [int(self.hatIMG.mapToScene(0,0).x()/self.f),int(self.hatIMG.mapToScene(0,0).y()/self.f)]
    f = open('./tmp/hat.txt', 'w')
    f.write(str(self.hat_pos[0])+" "+str(self.hat_pos[1]))
    f.close()
   #print(self.hat_pos)
   #print(self.value)
   self.value_signal.emit(0,self.value)


class DragGWindowSlc(QDialog):
 my_signal = pyqtSignal(str)
 value_signal = pyqtSignal(int,int,int,int,int)
 def __init__(self):
  QDialog.__init__(self)
  self.initPos=[0,0]
  self.Dir=""
  self.front=""
  self.front2=""
  self.value=0
  self.hat=0
  self.hatValue=0
  self.hatValue2=0
  self.imgSize=[]
  self.fronSize=[]
  self.sleeveLSize = []
  self.sleeveRSize = []
  self.hatSize=[]
  self.f=1
  self.sleeveRPos=[]
  self.sleeveRPos=[]
  self.hat_ori=0
  self.child = dragG.Ui_Dialog()
  #self.child.setFixedSize(MainWindow.width(), MainWindow.height())
  #self.child.myDialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
  self.sleeveLIMG=0
  self.sleeveRIMG = 0
  if(1):
   self.child.graphicsView = DragGraph.DragGraph(self)
   self.child.graphicsView.setGeometry(QtCore.QRect(0, 0, 600, 600))
   #self.child.graphicsView.setMaximumSize(800,600)
   brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
   brush.setStyle(QtCore.Qt.SolidPattern)
   self.child.graphicsView.setBackgroundBrush(brush)
   self.child.graphicsView.setMouseTracking(True)
   self.child.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
   self.child.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
   self.child.graphicsView.setDragMode(QtWidgets.QGraphicsView.NoDrag)
   self.child.graphicsView.setObjectName("graphicsView")
   self.child.setupUi(self)
   self.child.buttonBox.accepted.connect(self.myAccept)

   self.child.graphicsView2 = DragGraph.DragGraph(self)
   self.child.graphicsView2.setGeometry(QtCore.QRect(0, 0, 600, 600))
   brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
   brush.setStyle(QtCore.Qt.SolidPattern)
   self.child.graphicsView2.setBackgroundBrush(brush)
   self.child.graphicsView2.setMouseTracking(True)
   self.child.graphicsView2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
   self.child.graphicsView2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
   self.child.graphicsView2.setDragMode(QtWidgets.QGraphicsView.NoDrag)
   self.child.graphicsView2.setObjectName("graphicsView2")
   self.child.graphicsView2.hide()

   self.child.horizontalSlider = QtWidgets.QSlider(self)
   self.child.horizontalSlider.setGeometry(QtCore.QRect(30, 430, 160, 22))
   self.child.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
   self.child.horizontalSlider.setObjectName("horizontalSlider")
   self.child.horizontalSlider_2 = QtWidgets.QSlider(self.child.myDialog)
   #self.child.horizontalSlider_2.setGeometry(QtCore.QRect(30, 400, 160, 22))
   self.child.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
   self.child.horizontalSlider_2.setObjectName("horizontalSlider_2")
   self.child.horizontalSlider_3 = QtWidgets.QSlider(self.child.myDialog)
   #self.child.horizontalSlider_3.setGeometry(QtCore.QRect(30, 370, 160, 22))
   self.child.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
   self.child.horizontalSlider_3.setObjectName("horizontalSlider_3")
   self.child.horizontalSlider_3.hide()
   self.child.horizontalSlider_2.hide()

   self.child.setupUi(self)
   self.child.buttonBox.accepted.connect(self.myAccept)
   self.child.horizontalSlider.valueChanged['int'].connect(self.valueChange)
   self.child.horizontalSlider_2.valueChanged['int'].connect(self.valueChange2)
   self.child.horizontalSlider_3.valueChanged['int'].connect(self.valueChange3)
 def processIMG(self,string,right,down):
  self.initPos=[right,down]
  front_path=str(string)+"/bigtmp/back.png"
  print(front_path)
  sleeveL_path=str(string)+"/bigtmp/sleeveL.png"
  sleeveR_path = str(string) + "/bigtmp/sleeveR.png"
  print(os.path.join(string,"bigtmp/bigImage.jpg"))
  img=cv2.imread(os.path.join(string,"bigtmp/bigImage.jpg"),-1)
  sleeveL=cv2.imread(sleeveL_path,-1)
  sleeveR = cv2.imread(sleeveR_path, -1)
  front = cv2.imread(front_path, -1)
  self.child.horizontalSlider_2.setEnabled(False)
  self.child.horizontalSlider_3.setEnabled(False)
  self.hat=0
  self.imgSize=img.shape
  self.sleeveLSize=sleeveL.shape
  self.sleeveRSize = sleeveR.shape
  self.fronSize=front.shape
  img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
  front = cv2.cvtColor(np.array(front), cv2.COLOR_BGRA2RGBA)
  f1=600.0/img.shape[1]
  f2=600.0/img.shape[0]
  self.f=f1 if f1<f2 else f2
  self.f=self.f if self.f<1 else 1
  graphview = self.child.graphicsView
  graphview.setMinimumSize(int(img.shape[1]*self.f),int(img.shape[0]*self.f))
  graphview.setMaximumSize(int(img.shape[1]*self.f),int(img.shape[0]*self.f))
  print(self.f)
  tmp=int(img.shape[1]*self.f)
  if(tmp<550):
   tmp=550
  self.child.myDialog.resize(tmp,int(img.shape[0]*self.f)+50)
  if (img.shape[2] == 4):
   frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
  elif (img.shape[2] == 3):
   frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
  pix = QPixmap.fromImage(frame)
  self.background = QGraphicsPixmapItem(pix)  # 创建像素图元
  self.background.setScale(self.f)
  graphview.background = self.background
  # self.item.setFlag(QGraphicsItem.ItemIsMovable)
  graphview.scene = QGraphicsScene()  # 创建场景
  graphview.scene.setSceneRect(0, 0, int(self.imgSize[1]*self.f), int(self.imgSize[0]*self.f))
  graphview.scene.addItem(self.background)


  if (front.shape[2] == 4):
   front[:,:,3]=front[:,:,3]*0.8
   frame = QImage(front, front.shape[1], front.shape[0], front.shape[1] * 4, QImage.Format_RGBA8888)
  elif (img.shape[2] == 3):
   frame = QImage(front, front.shape[1], front.shape[0], front.shape[1] * 3, QImage.Format_RGB888)
  pix = QPixmap.fromImage(frame)
  self.front = QGraphicsPixmapItem(pix)  # 创建像素图元
  self.front.setScale(self.f)
  graphview.background = self.front
  self.front.setY(int((img.shape[0] // 2-(front.shape[0]//2))*self.f)+int(self.initPos[1]*self.f))
  self.front.setX(int((img.shape[1] // 2-(front.shape[1]//2))*self.f)+int(self.initPos[0]*self.f))
  print(233,self.initPos)
  graphview.background=0
  graphview.scene.addItem(self.front)

  #self.child.horizontalSlider_2.hide()
  ####################################hat

  if (sleeveL.shape[2] == 4):
   sleeveL[:, :, 3] = sleeveL[:, :, 3] * 0.8
   frame = QImage(sleeveL, sleeveL.shape[1], sleeveL.shape[0], sleeveL.shape[1] * 4, QImage.Format_RGBA8888)
  elif (front.shape[2] == 3):
   frame = QImage(sleeveL, sleeveL.shape[1], sleeveL.shape[0], sleeveL.shape[1] * 3, QImage.Format_RGB888)
  # frame.setScaledSize(QSize(img.shape[1],img.shape[0]))
  pix = QPixmap.fromImage(frame)
  self.sleeveLIMG = QGraphicsPixmapItem(pix) # 创建像素图元
  self.sleeveLIMG.setScale(self.f)
  self.sleeveLIMG.setFlag(QGraphicsItem.ItemIsMovable)

  if (sleeveR.shape[2] == 4):
   sleeveR[:, :, 3] = sleeveR[:, :, 3] * 0.8
   frame = QImage(sleeveR, sleeveR.shape[1], sleeveR.shape[0], sleeveR.shape[1] * 4, QImage.Format_RGBA8888)
  elif (front.shape[2] == 3):
   frame = QImage(sleeveR, sleeveR.shape[1], sleeveR.shape[0], sleeveR.shape[1] * 3, QImage.Format_RGB888)
  # frame.setScaledSize(QSize(img.shape[1],img.shape[0]))
  pix = QPixmap.fromImage(frame)
  self.sleeveRIMG = QGraphicsPixmapItem(pix) # 创建像素图元
  self.sleeveRIMG.setScale(self.f)
  self.sleeveRIMG.setFlag(QGraphicsItem.ItemIsMovable)
  if("Tshirt" in front_path):
   self.sleeveLIMG.setY(int((img.shape[0] // 2-(front.shape[0]//2))*self.f)+int(self.initPos[1]*self.f)-int(sleeveL.shape[0]*self.f)+int((front.shape[0] // 2)*self.f))
   self.sleeveRIMG.setX(int((img.shape[1]) * self.f)-int(sleeveR.shape[1] * self.f))
   self.sleeveRIMG.setY(int((img.shape[0] // 2-(front.shape[0]//2))*self.f)+int(self.initPos[1]*self.f)-int(sleeveR.shape[0]*self.f)+int((front.shape[0] // 2)*self.f))
   self.sleeveLIMG.setX(0)
  if("Sweater" in front_path):
   self.sleeveRIMG.setY(int((img.shape[0]) * self.f) - int(sleeveL.shape[0] * self.f))
   self.sleeveRIMG.setX(int((img.shape[1]) * self.f)-int(sleeveR.shape[1] * self.f))
   self.sleeveLIMG.setY(int((img.shape[0]) * self.f) - int(sleeveR.shape[0] * self.f))
   self.sleeveLIMG.setX(0)  # +int((img.shape[1]//2)*self.f)
  graphview.scene.addItem(self.sleeveLIMG)
  graphview.scene.addItem(self.sleeveRIMG)
  graphview.update()
  graphview.scene.update()
  graphview.setScene(graphview.scene)  # 将场景添加至视图
  ##########################
  self.child.horizontalSlider.setGeometry(QtCore.QRect(0,graphview.height(), 200, 32))
  self.child.horizontalSlider.hide()
  self.child.buttonBox.setGeometry(QtCore.QRect(210, graphview.height(), 160, 32))

 def valueChange(self):
  if(self.Dir=="Horizontal"):
   self.value=self.child.horizontalSlider.value()
   self.front.setX(int((self.imgSize[1] // 2 - (self.frontSize[1] // 2)+self.value)*self.f))
   if (self.hat):
    self.front2.setX(int((self.imgSize[1] // 2 - (self.frontSize[1] // 2)+self.value)*self.f))
    #self.hatIMG.setX(int((self.imgSize[1] // 2 - (self.frontSize[1] // 2) + self.value) * self.f))
  if(self.Dir=="Vertical"):
   self.value=self.child.horizontalSlider.value()
   self.front.setY(int((self.imgSize[0] // 2 - (self.frontSize[0] // 2)+self.value)*self.f))
   if(self.hat):
    #self.hatIMG.setY(int((self.imgSize[0] // 2 - (self.frontSize[0] // 2)+self.value-90)*self.f))
    self.front2.setY(int((self.imgSize[0] // 2 - (self.frontSize[0] // 2) + self.value) * self.f))
 def valueChange2(self):
  #print(self.child.horizontalSlider.value())
  if(self.hat):
   self.hatValue = self.child.horizontalSlider_2.value()
   self.hatIMG.setY(int((self.imgSize[0] // 2+self.hatValue)*self.f))
 def valueChange3(self):
  if(self.hat):
   self.hatValue2 = self.child.horizontalSlider_3.value()
   self.hatIMG.setX(int((self.imgSize[1] // 2+self.hatValue2)*self.f))
 def myAccept(self):
  success=1
  self.sleeveLPos = [int(self.sleeveLIMG.mapToScene(0, 0).x() / self.f),
                     int(self.sleeveLIMG.mapToScene(0, 0).y() / self.f)]
  self.sleeveRPos = [int(self.sleeveRIMG.mapToScene(0, 0).x() / self.f),
                     int(self.sleeveRIMG.mapToScene(0, 0).y() / self.f)]
  #print(self.value)
  if(self.sleeveLPos[1]<0 or self.sleeveLPos[1]>(self.imgSize[0]-self.sleeveLSize[0])):
   success=0
  if(self.sleeveLPos[0]<0 or self.sleeveLPos[0]>(self.imgSize[1]-self.sleeveLSize[1])):
   success=0
  if(self.sleeveRPos[1]<0 or self.sleeveRPos[1]>(self.imgSize[0]-self.sleeveRSize[0])):
   success=0
  if(self.sleeveRPos[0]<0 or self.sleeveRPos[0]>(self.imgSize[1]-self.sleeveRSize[1])):
   success=0
  self.value_signal.emit(self.sleeveLPos[0],self.sleeveLPos[1],self.sleeveRPos[0],self.sleeveRPos[1],success)
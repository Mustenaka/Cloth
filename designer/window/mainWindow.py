import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QMessageBox, QDialog, QGraphicsPixmapItem, QGraphicsItem

from designer import UI_ex
from designer import DragGraph
import sys, os
import cv2
import shutil
from wand.image import Image

from designer.ComboCheckBox import ComboCheckBox
from runSweater import runSweater
from runTshirt import runTshirt
#from src.ColorSpace import ColorSpace
from src.FreeTypography import FreeTypography
from src.drawWord import drawWord
from src.newColorSpace import newColorSpace
from src.saveFullSize import saveFullSzie


class MyPyQT_Form(QtWidgets.QWidget, UI_ex.UI_ex_Form):
 my_signal = pyqtSignal()
 my_signal_slc = pyqtSignal()
 imgsignal = pyqtSignal(str)
 imgsignal_slc = pyqtSignal(str,int,int)
 def __init__(self):
  super(MyPyQT_Form, self).__init__()
  self.setupUi(self)
  #self.setWindowFlags(QtCore.Qt.WindowFullscreenButtonHint|QtCore.Qt.WindowMaximizeButtonHint)
  self.graphicsView_slc_front.deleteLater()
  self.graphicsView_slc_front = DragGraph.DragGraph(self)
  self.graphicsView_slc_front.setGeometry(QtCore.QRect(740, 50, 600, 551))
  self.gridLayout.addWidget(self.graphicsView_slc_front, 0, 6, 5, 8)
  brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
  brush.setStyle(QtCore.Qt.SolidPattern)
  self.graphicsView_slc_front.setBackgroundBrush(brush)
  self.graphicsView_slc_front.setMouseTracking(True)
  self.graphicsView_slc_front.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
  self.graphicsView_slc_front.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
  self.graphicsView_slc_front.setDragMode(QtWidgets.QGraphicsView.NoDrag)
  self.graphicsView_slc_front.setObjectName("graphicsView_slc_front")
  self.pushButton_13.setEnabled(False)
  self.pushButton_10.setEnabled(False)
  self.pushButton_11.setEnabled(False)
  self.pushButton_7zhezhou.setEnabled(False)
  self.pushButton_8_paiban.setEnabled(False)
  self.pushButton_9_qiepian.setEnabled(False)
  self.pushButton_2.setEnabled(False)

  self.listWidget_size.deleteLater()
  self.listWidget_size = ComboCheckBox(items=["aaa", "aaaa"])
  self.listWidget_size.setMinimumSize(QtCore.QSize(0, 30))
  self.listWidget_size.setObjectName("listWidget_size")
  self.gridLayout.addWidget(self.listWidget_size, 5, 1, 1, 2)

  #self.listWidget_size.hide()
  #self.listWidget_size=ComboCheckBox(self=MyPyQT_Form)
  #self.listWidget_size.setGeometry(QtCore.QRect(120, 620, 151, 31))
  #self.listWidget_size.show()
#  self.pushButton_12.hide()

  self.lineEdit.setText(os.path.abspath("./"))
  if(os.path.exists("./tmp/savefile.txt")):
   file = open("./tmp/savefile.txt", 'r')
   list_read = file.readline()
   file.close()
   if(os.path.exists(os.path.abspath(list_read))):
    self.lineEdit.setText(os.path.abspath(list_read))
   else:
    self.lineEdit.setText(os.path.abspath("./"))
  self.output_path=self.lineEdit.text()
  if (not os.path.exists("./save/")):
   os.mkdir("./save")
  if (not os.path.exists("tmp/prelist")):
   os.makedirs("tmp/prelist")
  if (not os.path.exists("tmp/preview")):
   os.makedirs("tmp/preview")
  self.refreshList()
  savefile=os.path.join(self.pre_list,"model/model.txt")
  file = open(savefile, 'r')
  list_read = file.readlines()
  file.close()
  if(len(list_read)==0):
   QMessageBox.about(self, "警告", "无模型文件夹,请检查")
   sys.exit()
  self.model_name = list_read
  self.select_sizes=0
  self.listWidget_class.addItems(self.model_name)
  self.init = 0
  self.randFlag=0
  self.backgroundColor="black"
  self.process_fun=None
  self.layout_init()

 def select_model(self): #button2 临时改为true
  self.randFlag=0
  self.slc_paths=[]
  self.pushButton_13.setEnabled(False)
  self.pushButton_10.setEnabled(False)
  self.pushButton_11.setEnabled(False)
  self.pushButton_7zhezhou.setEnabled(False)
  self.pushButton_8_paiban.setEnabled(False)
  self.pushButton_9_qiepian.setEnabled(False)
  self.listWidget_size_3.setEnabled(False)
  self.pushButton_2.setEnabled(False)
  self.select_model_name[0] = self.listWidget_class.currentText()[:-1]
  filepath=os.path.join(self.pre_list+"size/", self.select_model_name[0] + ".txt")
  file = open(filepath, 'r')
  list_read = file.readlines()
  rule = {"S":0,"M":1,"L":2,"XL":3,"XXL":4,"3XL":5}
  # 单级排序，仅按照score排序
  #print("3XL\\n")
  print(list_read)
  size = sorted(list_read, key=lambda x:(rule.get(x[:-1]) if rule.get(x[:-1]) is not None else int(re.findall('\d+',x)[0])+5))
  self.listWidget_size.addList(size)
  #self.listWidget_size.addItem()
  #self.listWidget_size.clear()
  #self.listWidget_size.addItems(size)
  #dir_name=os.path.join(self.select_model_name[0],size[0][:-1])
  dir_name = self.select_model_name[0]
  view_dir=os.path.join(self.save_dir,dir_name)
  print(view_dir)
  self.view_front=os.path.join(view_dir,"front.png")
  self.view_back=os.path.join(view_dir,"back.png")
  if(not (os.path.exists(self.view_front) and os.path.exists(self.view_back))):
   QMessageBox.about(self, "警告", "无褶皱图文件，请检查")
   sys.exit()
  self.pre_view_front, _, _=self.preview(self.view_front,self.view_front_size)
  self.pre_view_back, _ , _= self.preview(self.view_back,self.view_back_size)
  self.updateimg(self.pre_view_front,self.graphicsView_pre_front)
  self.updateimg(self.pre_view_back, self.graphicsView_pre_back)
  print("choose model:", self.select_model_name[0])


  self.slc_paths=[]
  self.items=[]
  self.pushButton_13.setEnabled(False)
  self.select_model_name[1]=self.listWidget_size.currentText()[:-1]
  #dir_name=os.path.join(self.select_model_name[0],self.select_model_name[1])
  dir_name=self.select_model_name[0]
  self.select_dir=os.path.join(self.save_dir,dir_name)
  print("choose size:",self.select_model_name[1])
  if(self._initial==1):
   self.layout_add()
  self._initial=1   #button2
 def select_size(self):
  self.select_model_name[1] = self.listWidget_size_3.currentText()
  if(self.randFlag==1):
   output = os.path.join(self.save_dir, self.select_model_name[0])
   dir = os.path.join(output, self.select_model_name[1])
   output = os.path.join(dir, "eff/Composed.png")
   if (os.path.exists(output)):
    self.process(img_path=output, default=1)
  elif(self.randFlag==2):
   self.slc_paths = []
   print(self.select_model_name[1], self.choosImgPath)
   slc_dir = os.path.join(self.save_dir, self.select_model_name[0])
   slc_dir = os.path.join(slc_dir, self.select_model_name[1])
   slc_dir = os.path.join(slc_dir, "eff")
   for root, dirs, files in os.walk(os.path.join(slc_dir)):
    for file in files:
     if (file != "ansBack.jpg" and file != "ansFront.jpg" and file != "Composed.jpg" and file != "free_slice.jpg" and file != "ansBack.jpg" and file != "ansFront.png" and file != "Composed.png" and file != "free_slice.png"):
      self.slc_paths.append(os.path.join(slc_dir, file))
   self.mode="default"
   self.free_slice()

 def graph_doubleClick(self,string):  #双击
  if(self.stat=="normal"): #string为所选素材路径
   self.randFlag = 0
   self.listWidget_size_3.setEnabled(False)
   self.pushButton_13.setEnabled(True)
   self.pushButton_10.setEnabled(False)
   self.pushButton_11.setEnabled(False)
   self.pushButton_7zhezhou.setEnabled(False)
   self.pushButton_8_paiban.setEnabled(False)
   self.pushButton_9_qiepian.setEnabled(False)
   self.pushButton_2.setEnabled(False)
   self.doubleSpinBox.setValue(1)
   self.choosImgPath=string
   print(string)
   self.process(string)

 def import_mat(self):
  size = self.listWidget_size.Selectlist()
  if(len(size)>1):
   QMessageBox.about(self, "警告", "请勿多选尺码")
   return -1
  img_paths=QFileDialog.getOpenFileNames()
  dir=os.path.join(self.save_dir,self.select_model_name[0])
  dir=os.path.join(dir,size[0])
  for name in img_paths[0]:
   img_pic_path=os.path.join(dir,self.ori_dir)
   #print(img_pic_path)
   shutil.copy(str(name),img_pic_path)
  self.refreshList()

 def add_image(self):
  img_paths,_ = QFileDialog.getOpenFileNames()
  if(len(img_paths)!=0):
   for img_path in img_paths:
    img_name=str(img_path).split("/")[-1]
    print(img_path)
    shutil.copy(img_path, "./tmp/a." + str(img_path).split(".")[-1])
    img_path="./tmp/a." + str(img_path).split(".")[-1]
   # if(os.path.abspath(img_pic_path)!=img_path):
    directiong_file=self.checkSameName(img_path)
    img=cv2.imread(img_path,-1)
    if(img is None):
     return -1
    #img=cv2.imdecode(np.fromfile(str(img_path), dtype=np.uint8),-1)
    if(img.shape[1]<img.shape[0]*2  or  img.shape[1]*2 > img.shape[0]):
     shutil.copy(img_path,directiong_file)
     self.layout_add()
    else:
     QMessageBox.about(self, "警告", img_name+"图片尺寸不合规，导入失败")
    #directiong_file=os.path.realpath(directiong_file)

 def delete_image(self):
  if(self.stat=="normal"):
   self.stat="delete_image"
   self.pushButton_deleteimg.setText("完成")
  elif(self.stat=="delete_image"):
   self.stat="normal"
   self.pushButton_deleteimg.setText("删除图片")
   for id in self.deleteid:
    os.remove(self.layout_graph_list[id].img_path)
   self.deleteid=[]
   self.layout_add()
 def output_rander(self):  #褶皱
  self.select_model_name[1] = self.listWidget_size_3.currentText()
  #savepath=QFileDialog.getExistingDirectory(self,"保存","./")
  if(not os.path.exists(self.output_path)):
   QMessageBox.about(self, "警告", "请选择正确导出路径")
   return -1
  if (os.path.exists(self.view_front)):
   output = os.path.join(self.save_dir, self.select_model_name[0])
   dir = os.path.join(output, self.select_model_name[1])
   front_path=os.path.join(output,"out/ansFront.jpg")
   back_path =os.path.join(output, "out/ansBack.jpg")
   if(self.output_path==""):
    output_path="./"
   else:
    output_path=self.output_path
   if (self.productCode == ""):
    productCode="None"
   else:
    productCode=self.productCode
   with Image(filename=str(front_path).encode("utf8")) as img:
    # 存的目录为依旧是当前目录,用了一步replace，换了个目录
    img.save(
     filename="./tmp/1.jpg")
    if (os.path.exists(str(os.path.join(output_path, productCode + ".jpg"))) or 1):
     #ok = QMessageBox.warning(self, "警告对话框", "存在同名文件，是否覆盖?", QMessageBox.Yes | QMessageBox.No)
     ok = 16384
     if (ok==16384):
      saveFullSzie("./tmp/1.jpg",str(os.path.join(output_path, productCode + ".jpg")),self.select_model_name[0])
      #drawWord(str(os.path.join(output_path, productCode + ".jpg")),self.select_model_name[0],)
      #shutil.copy("./tmp/1.jpg", str(os.path.join(output_path, productCode + ".jpg")))

   with Image(filename=str(back_path).encode("utf8")) as img:
    # 存的目录为依旧是当前目录,用了一步replace，换了个目录
    img.save(
     filename="./tmp/1.jpg")
    if (os.path.exists(str(os.path.join(output_path, productCode + "-B.jpg"))) or 1):
     #ok = QMessageBox.warning(self, "警告对话框", "存在同名文件，是否覆盖?", QMessageBox.Yes | QMessageBox.No)
     ok=16384
     if (ok==16384):
      saveFullSzie("./tmp/1.jpg", str(os.path.join(output_path, productCode + "-B.jpg")),self.select_model_name[0])
      #shutil.copy("./tmp/1.jpg", str(os.path.join(output_path, productCode + "-B.jpg")))
  QMessageBox.about(self, "OK", "导出成功")
 def output_slice(self):  #切片
  self.select_model_name[1] = self.listWidget_size_3.currentText()
  # savepath=QFileDialog.getExistingDirectory(self,"保存","./")
  #print(self.output_path)
  if(not os.path.exists(self.output_path)):
   QMessageBox.about(self, "警告", "请选择正确导出路径")
   return -1
  self.slc_paths=[]
  slc_dir = os.path.join(self.save_dir, self.select_model_name[0])
  slc_dir = os.path.join(slc_dir, self.select_model_name[1])
  slc_dir = os.path.join(slc_dir, "eff")
  for root, dirs, files in os.walk(os.path.join(slc_dir)):
   for file in files:
    if (file != "ansBack.jpg" and file != "ansFront.jpg" and file != "Composed.jpg" and file != "free_slice.jpg" and file != "ansBack.jpg" and file != "ansFront.png" and file != "Composed.png" and file != "free_slice.png"):
     self.slc_paths.append(os.path.join(slc_dir, file))
  i=0
  for path in self.slc_paths:
   name=str(path).split("\\")[-1]
   name=str(name).split(".")[-2]
   if("back" in name):
    temp="后片"
   if ("forward" in name):
    temp = "前片"
   if ("sleeve" in name):
    temp = "袖子"
   if ("hem" in name):
    temp = "下摆"
   if ("front_bag_cloth" in name):
    temp = "袋布"
   if ("cuff_l" in name):
    temp = "袖口"
   if ("cuff_r" in name):
    temp = "袖口1"
   if ("hat_cloth_l" in name):
    temp = "帽布"
   if ("hat_cloth_r" in name):
    temp = "帽布1"
   if ("sleeve_l" in name):
    temp = "袖子"
   if ("sleeve_r" in name):
    temp = "袖子1"
   if ("neckline" in name):
    temp = "领口"
   if ("sleeve1" in name):
    temp = "袖子1"
   #name=os.path.join(self.output_path,name+".tif")
   #ColorSpace("./tmp/"+str(i)+".tif").changeColorSpace()

   if (self.productCode == ""):
    productCode="None"
    savepath=os.path.join(self.output_path, productCode + "_" + temp + "_" + self.select_model_name[1] + ".tif")
    newColorSpace(str(path), str(savepath)).usingICC()
   else:
    productCode=self.productCode
    savepath=os.path.join(self.output_path,productCode+"_"+temp+"_"+self.select_model_name[1]+".tif")
    newColorSpace(str(path), str(savepath)).usingICC()
   i=i+1
  QMessageBox.about(self, "OK", "导出成功")

 def output_compose(self):  #排班
  self.select_model_name[1] = self.listWidget_size_3.currentText()
  #savepath=QFileDialog.getExistingDirectory(self,"保存","./")
  if(not os.path.exists(self.output_path)):
   QMessageBox.about(self, "警告", "请选择正确导出路径")
   return -1
  if(self.productCode==""):
   savepath=os.path.join(self.output_path,"None_"+self.select_model_name[1]+"_ALL.tif")
  else:
   savepath=os.path.join(self.output_path,self.productCode+"_"+self.select_model_name[1]+"_ALL.tif")
  input = os.path.join(self.save_dir, self.select_model_name[0])
  dir = os.path.join(input, self.select_model_name[1])
  input_path = os.path.join(dir, "eff/Composed.png")
  if(savepath and os.path.exists(input_path)):
   path = str(savepath)[:-3] + 'tif'
   print(input_path,path)
   newColorSpace(input_path,str(path)).usingICC()
   '''
    ColorSpace("./tmp/1.tif").changeColorSpace()
    if (os.path.exists(path)):
     #ok = QMessageBox.warning(self, "警告对话框", "存在同名文件，是否覆盖?", QMessageBox.Yes | QMessageBox.No)
     ok = 16384
     if(ok==16384):
      shutil.copy("./tmp/1.tif", str(path))
    else:
     shutil.copy("./tmp/1.tif",str(path))
   '''
  QMessageBox.about(self, "OK", "导出成功")
 def chooseDir(self):
  output_path=QFileDialog.getExistingDirectory(self,"保存",self.output_path)
  if(output_path):
   self.output_path=output_path
   self.lineEdit.setText(str(output_path))
   file = open("./tmp/savefile.txt", "w")
   file.write(output_path)
   file.close()
 def textDir(self):
  output_path=self.lineEdit.text()
  if not os.path.exists(output_path):
   os.makedirs(output_path)
   self.output_path=output_path

  file = open("./tmp/savefile.txt", "w")
  file.write(output_path)
  file.close()
  if(not os.path.exists(output_path)):
   QMessageBox.about(self, "警告", "导出文件目录错误，请检查")
   self.lineEdit.setText(os.path.abspath("./"))
   file = open("./tmp/savefile.txt", "w")
   file.write(self.lineEdit.text())
   file.close()
 def textCode(self):
  self.productCode=self.lineEdit_2.text()

 def change_scale(self):
  value=self.doubleSpinBox.value()
  self.slc_f_2=value
  self.process()
 def default_slice(self):
  #这里是你的程序，给我默认切片渲染图地址
  self.randFlag = 1
  self.mode="default"
  self.pushButton_11.setText("自由排版")
  self.pushButton_7zhezhou.setEnabled(True)
  self.pushButton_8_paiban.setEnabled(True)
  self.pushButton_9_qiepian.setEnabled(True)
  self.process_fun.slices()
  self.select_size()
 def free_slice(self):
  self.pushButton_10.setEnabled(True)
  self.pushButton_11.setEnabled(True)
  if(self.mode!="free"):
   self.mode="free"
   self.slc_paths = []
   self.items=[]
   self.randFlag = 2
   #self.pushButton_13.hide()
   graphview = self.graphicsView_slc_front
   slc_dir = os.path.join(self.save_dir, self.select_model_name[0])
   slc_dir = os.path.join(slc_dir, self.select_model_name[1])
   slc_dir = os.path.join(slc_dir, "eff")
   self.pushButton_11.setText("生成排版图")
   for root, dirs, files in os.walk(os.path.join(slc_dir)):
    for file in files:
     if(file!="ansBack.png" and file!="ansFront.png" and file!="Composed.png" and file!="free_slice.png"):
      self.slc_paths.append(os.path.join(slc_dir, file))
   #print(self.slc_paths)
   graphview.scene = QGraphicsScene()  # 创建场景
   graphview.scene.setSceneRect(0, 0, self.slc_process_size[0], self.slc_process_size[1])
   flag=0
   for path in self.slc_paths:
    if(flag==0):
     img, _, self.slc_f = self.preview(path,[self.slc_process_size[0]//2, self.slc_process_size[1]//2], reload=1)
     flag=1
    else:
     img, _, self.slc_f = self.preview(path,f=self.slc_f, reload=1)
    if (img.shape[2] == 4):
     frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
    elif (img.shape[2] == 3):
     frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
    pix = QPixmap.fromImage(frame)
    self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
    #self.item.setTransformOriginPoint(img.shape[1]//2, img.shape[0]//2)
    self.items.append(self.item)
    self.item.setFlag(QGraphicsItem.ItemIsMovable)
    graphview.scene.addItem(self.item)
   # graphview.scene.addItem(self.item)
   graphview.update()
   graphview.scene.update()
   graphview.setScene(graphview.scene)  # 将场景添加至视图
  else:
   self.pushButton_7zhezhou.setEnabled(True)
   self.pushButton_8_paiban.setEnabled(True)
   self.pushButton_9_qiepian.setEnabled(True)
   output = os.path.join(self.save_dir, self.select_model_name[0])
   dir = os.path.join(output, self.select_model_name[1])
   output_path=os.path.join(dir,"eff/Composed.png")
   # API说明：
   #     传入，图片地址列表（Imglist）,图片参数（Parlist），最大尺寸（maxSize）
   #   图片地址列表为一个list，其中内容均为需要进行自由排版的切片地址
   #   图片参数为一个list嵌套一个三元组(a,b,c)，其中a,b为放置位置【左上角(0，0)坐标系】，c为旋转角度，仅允许(0,90,180,270)四个参数
   #   最大尺寸为一个二元组(x,y)，其表示这个自由排版的最大尺寸为
   # 注：在传入时为了避免超框的问题应当最大尺寸设计合理，不宜过大或者过小
   # 最后一个参数为保存文件名，这个自定义
   #print(self.items[0].mapToScene(0, 0).x(), self.items[0].mapToScene(0, 0).y())
   #print(self.items[0].rotation())
   #print(self.items[0].boundingRect().width())
   Parlist=[]
   maxX=0
   maxY=0
   for item in self.items:
    point = [0, 0]
    width=int(item.boundingRect().width()*self.slc_f_2)
    height = int(item.boundingRect().height()*self.slc_f_2)
    point[0]=item.mapToScene(0, 0).x()
    point[1]=item.mapToScene(0, 0).y()
    angle=item.rotation()
    if(angle==0):
     maxX=maxX if maxX > (point[0]+width) else (point[0]+width)
     maxY = maxY if maxY > (point[1] + height) else (point[1] + height)
    elif(angle == 90):
     point[0]=point[0]-height

     maxX= maxX if maxX > (point[0]+height) else (point[0]+height)
     maxY = maxY if maxY > (point[1] + width) else (point[1] + width)
    elif(angle==180):
     point[0] = point[0] - width
     point[1] = point[1] - height
     maxX = maxX if maxX > (point[0] + width) else (point[0] + width)
     maxY = maxY if maxY > (point[1] + height) else (point[1] + height)
    elif(angle==270):
     point[1] = point[1] - width
     maxX= maxX if maxX > (point[0]+height) else (point[0]+height)
     maxY = maxY if maxY > (point[1] + width) else (point[1] + width)
     print(point[0], point[1])
    Parlist.append((int(point[0]/(self.slc_f_2*self.slc_f)),int(point[1]/(self.slc_f_2*self.slc_f)),(360-angle)%360))
   size=(int(maxX/(self.slc_f_2*self.slc_f)),int(maxY/(self.slc_f_2*self.slc_f)))
   #print(self.slc_paths)
   print(self.slc_paths)
   FreeTypography(self.slc_paths, Parlist, size, output_path).type()
   print(self.slc_f,self.slc_f_2,self.background_f)
   QMessageBox.about(self, "OK", "生成成功")

 def test(self):
  savepath = QFileDialog.getExistingDirectory(self,"保存","./")
  #if(savepath and os.path.exists(self.view_front)):
   #shutil.copy(self.view_front, savepath)
   #shutil.copy(self.view_back, savepath)
  #QGraphicsScene.items()[0].mapToParent()
  #print(self.items[0].mapToParent(0,0).x(),self.items[0].mapToParent(0,0).y())

 def Stretch(self,String):
  print(String)
 def rand_slice(self):
  #self.process_rand_btn()
  self.process_fun.Preprocessing()
  self.my_signal_slc.emit()
  #self.initPos=[0,0]   #tmp
  self.imgsignal_slc.emit(str("./save/" + self.select_model_name[0]+"/"+self.select_model_name[1]),self.initPos[0],self.initPos[1])
  '''
  self.process_fun.Preprocessing()
  self.process_fun.starts((self.anchorPoint[0],self.anchorPoint[1]))
  self.pushButton_9_qiepian.setEnabled(True)
  self.pushButton_10.setEnabled(True)
  self.pushButton_11.setEnabled(True)
  QMessageBox.about(self, "OK", "渲染成功")
  '''
  #self.randFlag=0
  #self.my_signal.emit()
  #self.imgsignal.emit(str("./save/"+self.select_model_name[0]))
  #else:
  # QMessageBox.about(self, "失败", "请选择尺码")

 def moveUpDownSlc(self, rightL, downL,rightR, downR,success):
  if(success or 1):
   self.process_fun.starts((self.anchorPoint[0], self.anchorPoint[1]),[(rightL, downL),(rightR, downR)])
   sizes=self.listWidget_size.Selectlist()
   for size in sizes:
    dir=os.path.join(self.save_dir,self.select_model_name[0])
    dir = os.path.join(dir, size)
    dir = os.path.join(dir, "eff")
    for root, dirs, files in os.walk(os.path.join(dir)):
     for file in files:
      if (root == dir and ("Composed" not in file)):
       if(1):
        if(self.productCode==""):
         productCode="None"
        else:
         productCode=self.productCode
        if ("back" in file):
         temp = "后片"
        if ("forward" in file):
         temp = "前片"
        if ("sleeve" in file):
         temp = "袖子"
        if ("hem" in file):
         temp = "下摆"
        if ("front_bag_cloth" in file):
         temp = "袋布"
        if ("cuff_l" in file):
         temp = "袖口"
        if ("cuff_r" in file):
         temp = "袖口1"
        if ("hat_cloth_l" in file):
         temp = "帽布"
        if ("hat_cloth_r" in file):
         temp = "帽布1"
        if ("sleeve_l" in file):
         temp = "袖子"
        if ("sleeve_r" in file):
         temp = "袖子1"
        if ("neckline" in file):
         temp = "领口"
        if ("sleeve1" in file):
         temp = "袖子1"
       tra=0
       if("Tshirt" in self.select_model_name[0] and "sleeve" in file):
        tra=270
       code=productCode+"_"+temp+"_"+size
       drawWord(os.path.join(dir,file),code,tra=tra)
       #print(os.path.join(dir,file),code)
   self.pushButton_9_qiepian.setEnabled(True)
   self.pushButton_10.setEnabled(True)
   self.pushButton_11.setEnabled(True)
   QMessageBox.about(self, "OK", "渲染成功")
  else:
   QMessageBox.about(self, "警告", "超出边界")
   self.rand_slice()
 def rand_btn(self):
  #print(aaaaa)
  self.randFlag = 0
  size = self.listWidget_size.Selectlist()
  self.select_sizes = size
  print(size)
  if (len(size) != 0):
   if (self.select_model_name[0] == "Sweater"):
    del self.process_fun
    self.process_fun = runSweater(size, str(self.choosImgPath).split("\\")[-1])  # , (self.anchorPoint[0],self.anchorPoint[1],self.anchorPoint[2]))
    self.process_fun.preFlodDiagram()
   if (self.select_model_name[0] == "Tshirt"):
    del self.process_fun
    self.process_fun = runTshirt(size, str(self.choosImgPath).split("\\")[-1])  # ,(self.anchorPoint[0],self.anchorPoint[1], self.anchorPoint[2]))
    self.process_fun.preFlodDiagram()
   self.pushButton_2.setEnabled(True)
   self.my_signal.emit()
   self.imgsignal.emit(str("./save/" + self.select_model_name[0]))
 def moveUpDown(self,right, down):
  self.pushButton_11.setText("自由排版")
  self.anchorPoint=[0-down,0-right]
  if("Sweater" in self.select_model_name[0]):
   self.initPos=[right*5,down*5]
  if("Tshirt" in self.select_model_name[0]):
   self.initPos=[int(2.7*right),int(3.1*down)]
  print(self.initPos)
  self.process_fun.aftFlodDiagram((self.anchorPoint[0],self.anchorPoint[1]))

  output=os.path.join(self.save_dir,self.select_model_name[0])
  dir=output
  #dir=os.path.join(output,self.select_model_name[1])
  #output=os.path.join(dir,"eff/Composed.png")
  #self.process(img_path=output,default=1)
  front_img,_,_=self.preview(os.path.join(dir,"out/ansFront.jpg"),preview_size=self.view_front_size)
  back_img, _, _ = self.preview(os.path.join(dir, "out/ansBack.jpg"),preview_size=self.view_back_size)
  self.updateimg(front_img,self.graphicsView_pre_front)
  self.updateimg(back_img, self.graphicsView_pre_back)
  self.mode="none"
  self.pushButton_7zhezhou.setEnabled(True)
  print(down, right)
  QMessageBox.about(self, "OK", "渲染成功")
  self.listWidget_size_3.clear()
  self.listWidget_size_3.setEnabled(True)
  self.listWidget_size_3.addItems(self.select_sizes)
 def select_color(self):
  if(self.backgroundColor=="black"):
   self.backgroundColor = "white"
   brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
   brush.setStyle(QtCore.Qt.SolidPattern)
   self.graphicsView_slc_front.setBackgroundBrush(brush)
  else:
   self.backgroundColor = "black"
   brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
   brush.setStyle(QtCore.Qt.SolidPattern)
   self.graphicsView_slc_front.setBackgroundBrush(brush)
 def add_size(self,string):
  new_dir=os.path.join(self.save_dir,self.select_model_name[0])
  new_dir=os.path.join(new_dir,string)
  if(os.path.exists(new_dir)):
   QMessageBox.about(self, "警告", "已有尺码文件夹")
  else:
   os.mkdir(new_dir)
   os.mkdir(os.path.join(new_dir, "eff"))
   os.mkdir(os.path.join(new_dir, "ori"))
   os.mkdir(os.path.join(new_dir, "pic"))
   os.mkdir(os.path.join(new_dir, "tmp"))
   os.mkdir(os.path.join(new_dir, "opt"))
   os.mkdir(os.path.join(new_dir, "topt"))
   self.refreshList()
   self.listWidget_size.addItem(string+"\n")








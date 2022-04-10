#coding=utf-8
import operator
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPixmap, QImageReader
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QWidget, QGraphicsItem, QMessageBox
from PIL import Image as Im
from designer import LayoutGraph
from designer import DragGraph
from designer import UI2 as UI
import os
import cv2
import numpy as np
from wand.image import Image
from PIL import Image as pil_image

class UI_ex_Form(UI.Ui_Form):
    _chooseTIF = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(UI_ex_Form, self).__init__()
        self._initial = 0
        self.output_path=""
        self.choosImgPath=None
        self.productCode=""
        self.stat = "normal"
        self.save_dir = "./save"
        self.pic_dir = "pic/"
        self.pre_list = "./tmp/prelist/"
        self.preview_dir = "./tmp/preview/"
        self.ori_dir = "ori/"
        self.eff_dir = "eff/"
        self.default_size=["S","M","L","XL","XXL","3XL"]
        self.slc_paths=[]
        self.select_dir = ""
        self.select_img_name = ""  # 所选图片名字
        self.select_model_name = ["", ""]  # 所选衣服类型 尺码
        self.model_name = []
        self.initPos=[0,0]
        self.view_front = ""  # 正面图
        self.view_back = ""  # 背面图
        self.pre_view_front = 0  # 正面预览图
        self.pre_view_back = 0  # 背面预览图
        self.view_slc_front = ""  # 正面切片图
        self.view_slc_back = ""  # 背面切片图
        self.pre_view_slc_front = 0  # 正面切片预览图
        self.pre_view_slc_back = 0  # 背面切片预览图
        self.view_front_size = [251, 192]
        self.view_back_size = [251, 192]
        self.layout_graph_size = [160, 160]
        self.slc_process_size=[600,550]
        self.layout = QtWidgets.QGridLayout()
        self.layout_graph_list = []
        self.tif_num = 0
        self.deleteid = []
        self.background=None
        self.items=[]
        self.process_graph=None
        self.background_f=0
        self.slc_filenames=["前片.tif","后片.tif","领口.tif","袖子.tif","袖子1.tif"]
        self.slc_f=0
        self.slc_f_2=1
        self.anchorPoint=[0,0]
        self.mode = "None"
    def refreshList(self):  # 刷新列表
        models = []
        file_model=None
        for root, dirs, files in os.walk(self.save_dir):
            for dir in dirs:
                if (root == self.save_dir):
                    # dir_path=os.path.join(root,dir)
                    if (len(models) == 0):
                        model_savepath = os.path.join(self.pre_list, "model/model.txt")
                        file_model = open(model_savepath, "w")
                        models.append(dir)
                        file_model.write(str(dir))
                        file_model.write("\n")
                    else:
                        models.append(dir)
                        file_model.write(str(dir))
                        file_model.write("\n")
                else:
                    break
        if(file_model==None):
            QMessageBox.about(self, "警告", "无模型文件夹，请检查")
            sys.exit()
        file_model.close()
        print(models)
        for model in models:
            size = []
            dir_path = os.path.join(self.save_dir, model)
            for root, dirs, files in os.walk(dir_path):
                for dir in dirs:
                    if (root == dir_path):
                        if (not os.path.exists(os.path.join(dir_path, str(dir) + "/tmp/"))):
                            os.makedirs(os.path.join(dir_path, dir + "/tmp"))
                        if("pic" not in dir and "out" not in dir):
                            if (len(size) == 0):
                                size.append(dir)
                                size_savepath = os.path.join(self.pre_list, "size/" + model + ".txt")
                                file_size = open(size_savepath, "w")
                                file_size.write(str(dir))
                                file_size.write("\n")
                            else:
                                size.append(dir)
                                file_size.write(str(dir))
                                file_size.write("\n")
                    else:
                        break
                new_size_dir=None
                #print(dirs)
                if(root == dir_path):
                    for defaule_size in  self.default_size:
                        if(defaule_size not in dirs):
                            new_size_dir=os.path.join(dir_path, defaule_size)
                            #print(new_size_dir)
                            os.mkdir(new_size_dir)
                            os.mkdir(os.path.join(new_size_dir,"eff"))
                            os.mkdir(os.path.join(new_size_dir, "ori"))
                            os.mkdir(os.path.join(new_size_dir, "pic"))
                            os.mkdir(os.path.join(new_size_dir, "tmp"))
                            os.mkdir(os.path.join(new_size_dir, "opt"))
                            os.mkdir(os.path.join(new_size_dir, "topt"))
                    if(new_size_dir!=None):
                        self.refreshList()
            file_size.close()

    def preview(self, img_path, preview_size=None,f=1,reload=0,scale=1):  # preview=[width,height]
        img_path=img_path.replace("\\","/")
        fileInfo = os.stat(img_path)  # 获取文件属性信息
        m_time = fileInfo.st_mtime
        filename = str(img_path).replace(".", "_").replace("/", "_").replace("\\", "_")
        filename = filename + "_" + str(int(m_time)) + ".png"
        preview_path = os.path.join(self.preview_dir, filename)
        if (os.path.exists(preview_path) and reload==0):
            img = cv2.imread(preview_path,-1)
            if(len(img.shape)==2):
               img = cv2.imread(preview_path,1)
            if (img.shape[2] == 4):
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
            else:
                img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            return img, preview_path,f
        else:
            if(img_path.endswith(".tif")):
                with Image(filename=str(img_path).encode("utf8")) as img:
                    # 存的目录为依旧是当前目录,用了一步replace，换了个目录
                    img.save(
                        filename=str("./tmp/1.png"))
                ori_img = cv2.imread(str("./tmp/1.png"),-1)
            else:
                img_path=img_path
                print(img_path)
                ori_img = cv2.imread(img_path,-1)
                if (len(ori_img.shape) == 2):
                    ori_img = cv2.imread(img_path, 1)
                    cv2.imwrite(img_path,ori_img)
                if (ori_img is None):
                    return None, 0, 0
            height = ori_img.shape[0]
            width = ori_img.shape[1]
            if(preview_size!=None):
                fx = preview_size[0] / width
                fy = preview_size[1] / height
                f = (fx if (fx < fy) else fy)
            if(scale==1):
                img = cv2.resize(ori_img, (0,0), fy=f, fx=f, interpolation=cv2.INTER_AREA)
            else:
                img=ori_img
            if(reload==0 and scale==1):
                cv2.imwrite(preview_path, img)
            if(img.shape[2]==4):
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
            else:
                img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            return img, preview_path,f

    def updateimg(self, img, graphview,f=1):
        # self.graphview.setGeometry(QtCore.QRect(20, 80, self.nowimg.shape[1], self.nowimg.shape[0]))  # 设置画布大小，四周留白10像素，否则出现滚动条，坐标会错误
        if (img.shape[2] == 4):
            frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
        elif (img.shape[2] == 3):
            frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setScale(f)
        graphview.scene = QGraphicsScene()  # 创建场景
        graphview.scene.clear()
        graphview.scene.addItem(self.item)
        graphview.update()
        graphview.scene.update()
        graphview.setScene(graphview.scene)  # 将场景添加至视图
        #graphview.scene.items()[0].mapToParent()
        #graphview.mapFromScene(0,0)
        #for i in graphview.scene.items():
            #print(graphview.mapFromScene(0,0).x(),graphview.mapFromScene(0,0).y())

    def layout_init(self):
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 399, 649))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        tif_paths = []
        #pic_dir_path = os.path.join(self.select_dir, self.pic_dir)
        pic_dir_path="./pic"
        for root, dirs, files in os.walk(pic_dir_path):
            for file in files:
                if(root == pic_dir_path):
                    tif_path = os.path.join(root, file)
                    if os.path.splitext(tif_path)[1] == '.png':
                        # print(filename)
                        img = cv2.imread(tif_path)
                        print(tif_path.replace(".png", ".jpg"))
                        newfilename = tif_path.replace(".png", ".jpg")
                        # cv2.imshow("Image",img)
                        # cv2.waitKey(0)
                        cv2.imwrite(newfilename, img)
                        os.remove(tif_path)
                        tif_path=newfilename
                    tif_paths.append(tif_path)
        self.tif_num = len(tif_paths)
        for i in range(self.tif_num):
            img, _ , f= self.preview(tif_paths[i], self.layout_graph_size)
            if(not(img is None)):
                temp = LayoutGraph.LayoutGraph()
                temp.img_path = tif_paths[i]
                temp.id = i
                temp.ctime=int(os.path.getmtime(tif_paths[i]))
                #temp.setMaximumSize(180, 180)
                temp.setMinimumSize(180, 180)
                temp.setStyleSheet("QGraphicsView{background-color:gray;border-top-left-radius:15px;border-top-right-radius:15px;border-bottom-left-radius:15px;border-bottom-right-radius:15px;}")
                temp.doubleClick.connect(self.graph_doubleClick)
                temp.Click.connect(self._deleteIMG)
                self.layout_graph_list.append(temp)
        cmpfun = operator.attrgetter('ctime')  # 参数为排序依据的属性，可以有多个，这里优先id，使用时按需求改换参数即可
        self.layout_graph_list.sort(key=cmpfun,reverse=True)  # 使用时改变列表名即可
        for i in range(self.tif_num):
            self.layout_graph_list[i].id=i
            img, _, f = self.preview(self.layout_graph_list[i].img_path, self.layout_graph_size)
            self.layout.addWidget(self.layout_graph_list[i], i / 2, i % 2, 1, 1)
            self.updateimg(img, self.layout_graph_list[i])
        self.scrollArea.widget().setLayout(self.layout)
        for temp in self.scrollArea.widget().findChildren(LayoutGraph.LayoutGraph):
            break

    def graph_doubleClick(self, string):
        pass

    def layout_add(self):
        self.layout_graph_list = []
        self.tif_num = 0
        self.layout.deleteLater()
        self.layout = QtWidgets.QGridLayout()
        self.layout_init()

    def checkSameName(self, img_path):
        img_name = str(img_path).split("/")[-1]
        #pic_dir_path = os.path.join(self.select_dir, self.pic_dir)
        pic_dir_path="./pic"
        img_pic_path = os.path.join(pic_dir_path, img_name)
        if (os.path.exists(img_pic_path)):  # 如果存在同名
            portion = os.path.splitext(img_path)  # 分离文件名与扩展名
            directiong_file = portion[0] + "_" + portion[1]  # 更改文件名
            directiong_file = self.checkSameName(directiong_file)
        else:
            directiong_file = img_pic_path
            return directiong_file
        return directiong_file

    def _deleteIMG(self, id):
        temp = self.layout_graph_list[id]
        if (self.stat == "delete_image"):
            if (temp.ifdelete == 0):
                temp.ifdelete = 1
                img, _ , _ = self.preview(temp.img_path, self.layout_graph_size)
                if(img.shape[2]==3):
                    cv2.circle(img, (10, 10), 10, (255, 0, 0), -1, 0)
                elif (img.shape[2] == 4):
                    cv2.circle(img, (10, 10), 10, (255, 0, 0,255), -1, 0)
                else:
                    cv2.circle(img, (10, 10), 10, (255, 0, 0), -1, 0)
                self.updateimg(img, temp)
                self.deleteid.append(id)
            else:
                temp.ifdelete = 0
                img, _ , _= self.preview(temp.img_path, self.layout_graph_size)
                self.updateimg(img, temp)
                self.deleteid.remove(id)

    def process(self,img_path=None,default=0):
        self.slc_process_size=[self.graphicsView_slc_front.width(),self.graphicsView_slc_front.height()]
        slc_pre_imgs=[]
        graphview = self.graphicsView_slc_front
        if(img_path!=None):
            slc_dir=os.path.join(self.save_dir,self.select_model_name[0])
            slc_dir=os.path.join(slc_dir,self.select_model_name[1])
            slc_dir=os.path.join(slc_dir,"opt")
            img,pre_img_path,self.background_f=self.preview(img_path,self.slc_process_size,reload=1)
            #frame = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            if (img.shape[2] == 4):
                frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 4, QImage.Format_RGBA8888)
            elif (img.shape[2] == 3):
                frame = QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            #frame.setScaledSize(QSize(img.shape[1],img.shape[0]))
            pix = QPixmap.fromImage(frame)
            self.background = QGraphicsPixmapItem(pix)  # 创建像素图元
            graphview.background=self.background
            #self.item.setFlag(QGraphicsItem.ItemIsMovable)
            graphview.scene = QGraphicsScene()  # 创建场景
            graphview.scene.setSceneRect(0,0,img.shape[1],img.shape[0])
            graphview.scene.addItem(self.background)
            graphview.update()
            graphview.scene.update()
            graphview.setScene(graphview.scene)  # 将场景添加至视图
        elif(img_path==None and self.mode=="free"):
            for i in self.items:
                i.setScale(self.slc_f_2)
                #print(i.scale())
        # graphview.scene.items()[0].mapToParent()
        # graphview.mapFromScene(0,0)
        #for i in graphview.scene.items():
            #print(graphview.mapFromScene(0, 0).x(), graphview.mapFromScene(0, 0).y())

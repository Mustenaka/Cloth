import sys
import traceback

from PyQt5 import QtWidgets

from designer.window.dragWindow import DragGWindow, DragGWindowSlc
from designer.window.mainWindow import MyPyQT_Form
from designer.window.textSWindow import TextSWindow
import os
import sys
import trace


# 默认__name__ ,可更改
if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        my_pyqt_form = MyPyQT_Form()
        textSWindow=TextSWindow()
        addSize_btn=my_pyqt_form.pushButton_4
        addSize_btn.clicked.connect(textSWindow.show)
        textSWindow.my_signal.connect(my_pyqt_form.add_size)

        dragGWindow = DragGWindow()
        dragGWindow_slc = DragGWindowSlc()

        my_pyqt_form.my_signal.connect(dragGWindow.show)
        my_pyqt_form.my_signal_slc.connect(dragGWindow_slc.show)
        my_pyqt_form.imgsignal.connect(dragGWindow.processIMG)
        my_pyqt_form.imgsignal_slc.connect(dragGWindow_slc.processIMG)

        dragGWindow.value_signal.connect(my_pyqt_form.moveUpDown)
        dragGWindow_slc.value_signal.connect(my_pyqt_form.moveUpDownSlc)

        my_pyqt_form.show()
        sys.exit(app.exec_())
    except Exception as e:
        f = open("log.txt","w")
        f.write(e)
        f.close()

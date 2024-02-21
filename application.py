# ------------openCV와 Pyqt camera--------------#

from datetime import datetime
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import urllib.request       # url이미지를 가져오기 위한 모듈
from  PyQt5.QtCore import *
import cv2, imutils
from MediaController import * 
import time

from_class = uic.loadUiType("application.ui")[0]


class WindowClass(QMainWindow, from_class) :
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowTitle("Camera Application")       

        # Flag
        self.isCameraOn = True
        self.isRecStart = False
        self.mode = 'capture'
        
        
        # Instance
        self.camera = MediaController(self)                          # camera instance
        self.camera.daemon = True
        
        self.record = MediaController(self)                          # recorde instance
        self.record.daemon = True
                              
        self.pixmap = QPixmap()                             # pixmap instance
        
        
        # Action            
        # 1. Camera
        self.camera.cameraStart()                               
        self.camera.update.connect(self.updateCamera)
        self.startButton.clicked.connect(self.clickCamera)      
        
        # 2. Capture
        self.captureButton.clicked.connect(lambda mode, btn=self.captureButton: self.modeChanged(btn.text()))

        # 3. Record
        self.recordButton.clicked.connect(lambda mode, btn=self.recordButton: self.modeChanged(btn.text()))
        self.record.update.connect(self.updateRecording)    
        
        # 4. File
        self.openButton.clicked.connect(self.openFile)

    def modeChanged(self, btn) :
        if btn == 'capture' :
            self.setWindowTitle("Capture mode")
            self.mode = btn
            self.captureButton.setStyleSheet("background-color : rgb(154, 153, 150)")   # darkgrey
            self.recordButton.setStyleSheet("background-color : rgb(222, 221, 218)")    # grey
            
        elif btn == 'record' :
            self.setWindowTitle("Record mode")  
            self.mode = btn
            
            self.recordButton.setStyleSheet("background-color : rgb(154, 153, 150)")    # darkgrey
            self.captureButton.setStyleSheet("background-color : rgb(222, 221, 218)")   # grey
            
                
    def clickCamera(self):
        if self.mode == 'capture':
            self.captureMode()
            
        elif self.mode == 'record':
            self.recordMode()
    
    
    # ------------- Record -------------------------------- #
           
    def recordMode(self):
        if self.isRecStart == False:
            self.isRecStart = True
            
            self.recordingStart()
        else:
            self.isRecStart = False
            
            self.recordingStop()
           
              
    # ------------- Capture ---------------------------------- #
    def captureMode(self):
        self.now = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.png'
        
        cv2.imwrite(filename, self.now.image)
     
     
    # ------------- File ---------------------------------- #
    def openFile(self):
        file = QFileDialog.getOpenFileName(filter='Image (*.*)')
        
        self.image = cv2.imread(file)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
        
        h, w, c = self.image.shape
        
        self.pixmap = self.pixmap.scaled(self.labelPixmap.width(), self.labelPixmap.height())
        qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)
        
        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.labelPixmap.width(), self.labelPixmap.height())
        
        self.labelPixmap.setPixmap(self.pixmap)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show() 
    
    sys.exit(app.exec_())

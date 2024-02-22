# ------------openCV와 Pyqt camera--------------#

from datetime import datetime
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import urllib.request       # url이미지를 가져오기 위한 모듈
import cv2, imutils
from Camera import Camera
from Recorder import Recorder
from qt_opencv.camera_application.Recorder import Recoder
from EffectWindow import *
import time
from PyQt5.QtCore import *

from_class = uic.loadUiType("application.ui")[0]


class WindowClass(QMainWindow, from_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowTitle("Camera Application")
        
        
        # Instance
        self.recorder = Recorder(self)                          # recorde instance
        self.recorder.daemon = True
        
        self.camera = Camera(self)                              # camera instance
        self.camera.daemon = True
               
        self.pixmap = QPixmap()                                 # pixmap instance
        
        
        # Action            
        # 1. Camera
        self.start()                               
        self.camera.frame.connect(self.dispalyFrame)    
        
        # 2. Capture
        self.captureButton.clicked.connect(lambda mode, btn=self.captureButton: self.modeChanged(btn.text()))

        # 3. Record
        self.recordButton.clicked.connect(lambda mode, btn=self.recordButton: self.modeChanged(btn.text()))
        
        # 4. start
        self.startButton.clicked.connect(self.clickCamera)  
        
        # 5. File
        self.openButton.clicked.connect(self.openFile)

        # 6. Effect
        self.effectButton.clicked.connect(self.showEffects)
    
    
    def modeChanged(self, btn) :
        if btn == 'capture' :
            self.setWindowTitle("Capture mode")
            self.mode = 'capture'
            self.captureButton.setStyleSheet("background-color : rgb(154, 153, 150)")   # darkgrey
            self.recordButton.setStyleSheet("background-color : rgb(222, 221, 218)")    # grey
            
        elif btn == 'record' :
            self.setWindowTitle("Record mode")  
            self.mode = 'record'
            
            self.recordButton.setStyleSheet("background-color : rgb(154, 153, 150)")    # darkgrey
            self.captureButton.setStyleSheet("background-color : rgb(222, 221, 218)")   # grey
            
                
    def clickCamera(self):
        if self.mode == 'capture':
            self.captureMode()
            
        elif self.mode == 'record':
            self.recordMode()
    
    
    def recordMode(self):
        
        if self.recorder.running:
            self.recorder.stopRecording()
            self.startButton.setText("start")
        
        else:
            self.recorder.startRecording()
            self.startButton.setText("🔴 Rec")
            
             
    def captureMode(self):
        self.now = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.png'
        
        cv2.imwrite(filename, self.image)
        
        self.startButton.setText("complete!")
        time.sleep(1)
        self.startButton.setText("start")
     
     
    # 받아온 BGR frame -> RGB frame으로 변환
    def dispalyFrame(self, frame):
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            
            h, w, c = self.image.shape
            qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)
            
            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.videoScreen.width(), self.videoScreen.height())
            
            self.videoScreen.setPixmap(self.pixmap)
    
    
    def updateRecording(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.writer.write(self.image)
        

    def showEffects(self):
        self.effectWindows = EffectWindow()
        self.effectWindows.show()
        self.close()
     
     
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
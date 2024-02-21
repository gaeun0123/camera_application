from  PyQt5.QtCore import *
import time
import cv2
from datetime import datetime

# QThread는 보통 start, running, stop함수가 있다.
# run은 loop 돌게끔
class MediaController(QThread):                          
    update = pyqtSignal()                           # 시그널 업데이트               
    
    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True
        
        
    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()                      # 시그널 발생
            time.sleep(0.1)                         # 시그널 주기
            
            
    def stop(self):
        self.running = False
        
        
    def cameraStart(self):
        self.running = True
        self.start()
        self.video = cv2.VideoCapture(-1)
    
    
    def cameraStop(self):
        self.running = False
        self.count = 0
        self.video.release()
        
        
    def updateCamera(self):
        retval, self.image = self.camera.video.read()
        if retval:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            
            h, w, c = self.image.shape
            qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)
            
            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.videoScreen.width(), self.videoScreen.height())
            
            self.videoScreen.setPixmap(self.pixmap)
            
    
    
    def recordingStart(self):
        self.record.running = True
        self.record.start()
        
        self.now = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')                       # 코덱 정의
        
        w = int(self.camera.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.camera.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w,h))
        
        
    def recordingStop(self):
        self.record.running = False
        self.record.stop()
        
        if self.isRecStart == True:
            self.writer.release()
    
    
    def updateRecording(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.writer.write(self.image)
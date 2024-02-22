from  PyQt5.QtCore import *
import cv2
import numpy as np

class Camera(QThread):                          
    frame = pyqtSignal(np.ndarray)           
    
    def __init__(self, parent=None):
        super().__init__()
        
        self.effectMode = False
        self.isRunning = True
        self.video = None
    

    def run(self):
        self.video = cv2.VideoCapture(0)      
        
        while self.isRunning:
            ret, frame = self.video.read()
            if ret:
                self.frameCaptured.emit(frame)  # frame signal 발생
        self.video.release()

        
        
    def stop(self):
        self.isRunning = False
        
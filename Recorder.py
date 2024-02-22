import cv2
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
import numpy as np
from datetime import datetime


class Recorder(QThread):
       
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isRecording = False
        self.writer = None
        self.frame = None


    # Main loop
    def run(self):
        while self.isRecording:                        # Running 상태가 false면 stop
            if self.frame is not None:
                self.writer.write(self.frame)
                

    # Record Thread 시작
    def startRecording(self):
        self.isRecording = True
        self.start()

    
    # Record Thread 정지
    def stopRecording(self):
        self.isRecording = False
        
        if self.writer:
            self.writer.release()
            self.writer = None


    def recieveFrame(self, frame):
        if self.isRecording:        # 녹화 중일 때만 frame update
            self.frame = frame






from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot
from Camera import *

class EffectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Select Effort") 
    
    
    def initUI(self):
        self.camera = Camera()
        self.camera.frame.connect(self.setImage)
        self.camera.start()
        
    # 받은 이미지(np.ndarray) -> QImage로 변환
    def cvtQImage(self, frame):
        pass
        
    
    # QImage를 R, G, B로 변환 후 pixmap에 출력
    def setImage(self, image):
        redImage = image.copy()
        greenImage = image.copy()
        blueImage = image.copy()

        # R, G, B 채널 분리 후 다른 채널은 검정색으로 처리
        redImage.fill(Qt.black)
        greenImage.fill(Qt.black)
        blueImage.fill(Qt.black)

        redImage.setAlphaChannel(image.alphaChannel())
        greenImage.setAlphaChannel(image.alphaChannel())
        blueImage.setAlphaChannel(image.alphaChannel())

        self.labelR.setPixmap(QPixmap.fromImage(redImage))
        self.labelG.setPixmap(QPixmap.fromImage(greenImage))
        self.labelB.setPixmap(QPixmap.fromImage(blueImage))
        
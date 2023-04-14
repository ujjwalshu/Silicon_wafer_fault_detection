import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Wafer Fault Detection'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.width, self.height)

        browse_btn = QPushButton('Browse', self)
        browse_btn.setGeometry(10, 10, 80, 30)
        browse_btn.clicked.connect(self.browse_image)

        self.show()

    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Select Image", "","All Files (*);;Image Files (*.jpg *.png)", options=options)
        if file_name:
            image = cv2.imread(file_name)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pixmap = QPixmap.fromImage(QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888))
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)

            # Apply wafer fault detection algorithm to the image here
            # Remove this line -> image = cv2.imread('silicon_wafer_fresh.jpg')

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to segment the image
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # Find contours in the image
            contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # Loop over the contours and draw a rectangle around each faulty area
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if w * h > 100:  # Arbitrary threshold for area of the bounding box
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Display the resulting image
            cv2.imshow('Faulty Areas', image)
            cv2.waitKey(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

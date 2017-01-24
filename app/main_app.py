#!/usr/bin/python
# -*- coding: utf-8 -*-
#TODO: Write the documentation

import sys
from PySide import QtGui
from PySide import QtCore
import pic.encrypt
import pic.decrypt

class AoPIC(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AoPIC, self).__init__(parent)

        self.tab = QtGui.QTabWidget()
        self.tab.addTab(EncodeTab(), "Encode")
        self.tab.addTab(DecodeTab(), "Decode")

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.tab)
        self.setLayout(mainLayout)
        self.setWindowTitle('App for Python Image Crypter')
        self.setMaximumSize(600,250)
        self.setMinimumSize(600,250)
        self.show()

    def getImageOpenPath(self):
        return QtGui.QFileDialog.getOpenFileName(self, "Image open", filter="Images (*.png *.jpg)")[0]

    def getImageSavePath(self):
        return QtGui.QFileDialog.getSaveFileName(self, "Image save", filter="Images (*.png)")[0]

class EncodeTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(EncodeTab, self).__init__(parent)
        self.mainImage = ''
        self.encodeImage = ''
        self.outputImage = ''

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        self.mainImageLabel = QtGui.QLabel(self)
        self.mainImageLabel.setText("Main image:")

        self.mainImageLine = QtGui.QLineEdit(self)
        self.mainImageLine.setEnabled(False)

        self.mainImageButton = QtGui.QPushButton("Open", self)
        self.mainImageButton.clicked.connect(self.buttonClicked)

        self.imageToEncryptLabel = QtGui.QLabel(self)
        self.imageToEncryptLabel.setText("Image to be encoded:")

        self.imageToEncryptLine = QtGui.QLineEdit(self)
        self.imageToEncryptLine.setEnabled(False)

        self.imageToEncryptButton = QtGui.QPushButton("Open", self)
        self.imageToEncryptButton.clicked.connect(self.buttonClicked)

        self.outputImageLabel = QtGui.QLabel(self)
        self.outputImageLabel.setText("Save as:")

        self.outputImageLine = QtGui.QLineEdit(self)
        self.outputImageLine.setEnabled(False)

        self.outputImageButton = QtGui.QPushButton("Save", self)
        self.outputImageButton.clicked.connect(self.buttonClicked)

        self.startEncodeButton = QtGui.QPushButton("Start", self)
        self.startEncodeButton.clicked.connect(self.buttonClicked)
        self.startEncodeButton.setEnabled(False)

        self.encodeProgressBar = QtGui.QProgressBar(self)

        grid.addWidget(self.mainImageLabel, 1, 0)
        grid.addWidget(self.mainImageLine, 2, 0)
        grid.addWidget(self.mainImageButton, 2, 1)

        grid.addWidget(self.imageToEncryptLabel, 3, 0)
        grid.addWidget(self.imageToEncryptLine, 4, 0)
        grid.addWidget(self.imageToEncryptButton, 4, 1)

        grid.addWidget(self.outputImageLabel, 5, 0)
        grid.addWidget(self.outputImageLine, 6, 0)
        grid.addWidget(self.outputImageButton, 6, 1)

        grid.addWidget(self.encodeProgressBar, 7, 0)
        grid.addWidget(self.startEncodeButton, 7, 1)

        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

    def encodeStart(self):
        self.encryptThread = pic.encrypt.Encrypt(self.mainImage, self.encodeImage, self.outputImage, self)
        self.encryptThread.progress.connect(self.encodeProgressBarUpdate, QtCore.Qt.QueuedConnection)
        if not self.encryptThread.isRunning():
            self.encryptThread.start()

    def encodeProgressBarUpdate(self, value):
        self.encodeProgressBar.setValue(value)

    def buttonClicked(self): #TODO: After new UI implement Cancel Button
        sender = self.sender()
        if sender == self.mainImageButton:
            self.mainImage = AoPIC.getImageOpenPath(self)
            self.mainImageLine.setText(self.mainImage)

        elif sender == self.imageToEncryptButton:
            self.encodeImage = AoPIC.getImageOpenPath(self)
            self.imageToEncryptLine.setText(self.encodeImage)

        elif sender == self.outputImageButton:
            self.outputImage = AoPIC.getImageSavePath(self)
            self.outputImageLine.setText(self.outputImage)

        elif sender == self.startEncodeButton:
            self.encodeStart()

        if self.mainImage and self.encodeImage and self.outputImage:
            self.startEncodeButton.setEnabled(True)
        else :
            self.startEncodeButton.setEnabled(False)

class DecodeTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DecodeTab, self).__init__(parent)
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.setAlignment(QtCore.Qt.AlignTop)
        grid.setVerticalSpacing(10)

        self.decodeSaveImage = ''

        self.imageToDecodeLabel = QtGui.QLabel(self)
        self.imageToDecodeLabel.setText("Image to be decoded:")

        self.imageToDecodeLine = QtGui.QLineEdit(self)
        self.imageToDecodeLine.setEnabled(False)

        self.imageToDecodeButton = QtGui.QPushButton("Open", self)
        self.imageToDecodeButton.clicked.connect(self.buttonClicked)

        self.outputImageLabel = QtGui.QLabel(self)
        self.outputImageLabel.setText("Save as:")

        self.imageToDecodeSaveLine = QtGui.QLineEdit(self)
        self.imageToDecodeSaveLine.setEnabled(False)

        self.imageToDecodeSaveButton = QtGui.QPushButton("Save", self)
        self.imageToDecodeSaveButton.clicked.connect(self.buttonClicked)

        self.startDecodeButton = QtGui.QPushButton("Start", self)
        self.startDecodeButton.clicked.connect(self.buttonClicked)
        self.startDecodeButton.setEnabled(False)

        self.decodeProgressBar = QtGui.QProgressBar(self)

        grid.addWidget(self.imageToDecodeLabel, 1, 0)
        grid.addWidget(self.imageToDecodeLine, 2, 0)
        grid.addWidget(self.imageToDecodeButton, 2, 1)

        grid.addWidget(self.outputImageLabel, 3, 0 )

        grid.addWidget(self.imageToDecodeSaveLine, 4, 0)
        grid.addWidget(self.imageToDecodeSaveButton, 4, 1)

        grid.addWidget(self.decodeProgressBar, 5, 0)
        grid.addWidget(self.startDecodeButton, 5, 1)

        self.setLayout(grid)

    def decodeProgressBarUpdate(self, value):
        self.decodeProgressBar.setValue(value)

    def decodeStart(self):
        self.decodeThread = pic.decrypt.Decrypt(self.decodeImage, self, self.decodeSaveImage)
        self.decodeThread.progress.connect(self.decodeProgressBarUpdate, QtCore.Qt.QueuedConnection)
        if not self.decodeThread.isRunning():
            self.decodeThread.start()

    def buttonClicked(self): #TODO: Implement cancel button with threads
        sender = self.sender()

        if sender == self.imageToDecodeButton:
            self.decodeImage = AoPIC.getImageOpenPath(self)
            self.imageToDecodeLine.setText(self.decodeImage)

        elif sender == self.startDecodeButton:
            self.decodeStart()
        elif sender == self.imageToDecodeSaveButton:
            self.decodeSaveImage = AoPIC.getImageSavePath(self)
            self.imageToDecodeSaveLine.setText(self.decodeSaveImage)

        if self.decodeProgressBar.value() == 100:
            self.decodeProgressBar.setValue(0)

        if self.decodeImage:
            self.startDecodeButton.setEnabled(True)
        else:
            self.startDecodeButton.setEnabled(False)

def main():
    app = QtGui.QApplication(sys.argv)
    appOfPythonImageCrpyter = AoPIC()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
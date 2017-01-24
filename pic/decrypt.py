#!/usr/bin/python
# -*- coding: utf-8 -*-
#TODO: Write the documentation

from PySide import QtCore
from PIL import Image

class Decrypt (QtCore.QThread): #TODO: <!> REFACTOR WHOLE CLASS </!>
    progress = QtCore.Signal(int)

    def __init__(self, image, parent=None, saveImage=''):
        super(Decrypt, self).__init__(parent)
        self.__image = image
        self.__parent = parent
        self.__saveImage = saveImage

        try: #TODO: Implement pop-up like errors !
            self.iTE = Image.open(self.__image)
        except FileNotFoundError as err:
            print(err) #TODO: Error Handling

    @staticmethod
    def __readPix(x):
        g = int( bin(x[0])[2:][-2:]+bin(x[1])[2:][-2:]+bin(x[2])[2:][-2:], 2) * 4 #To RGB
        return g,g,g

    def run(self):
        ite_pix = self.iTE.load()
        width,height = self.iTE.size
        image = Image.new('RGB', (width, height))
        im_pix = image.load()

        for x in range(0, width):
            for y in range(0, height):
                im_pix[x,y] = self.__readPix(ite_pix[x,y])
                QtCore.QThread.sleep(0.1)
            self.progress.emit(round(100*x/width))

        if self.__saveImage:
            image.save(self.__saveImage)
        image.show()

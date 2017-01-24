#!/usr/bin/python
# -*- coding: utf-8 -*-
#TODO: Write the documentation

from PySide import QtCore
from PIL import Image

class Encrypt (QtCore.QThread):
    progress = QtCore.Signal(int)

    # noinspection PyPep8Naming
    def __init__(self, im, itc, out, parent=None):
        super(Encrypt, self).__init__(parent)

        self.__out = out
        try:
            self.__im = Image.open(im)
            self.__itc = Image.open(itc)
        except FileNotFoundError as err:
            print(err) #TODO: Error Handling

    def __pixWrite(self, x, n):
        return self.__bitWrite(x[0], n[:2]), self.__bitWrite(x[1], n[2:4]), self.__bitWrite(x[2], n[4:6])

    @staticmethod
    def __bitWrite(n, x):
        return int(bin(n)[:-2]+x,2)

    @staticmethod
    def __pixToGray(x):
        if type(x) == tuple:
            x = sum(x)/len(x)
        n = int(x//4)
        return bin(n)[2:].zfill(6)

    def run(self):
        #TODO: Implement pop-ups for differences in sizes of images
        #if self.__im.size[0]<self.__itc.size[0] or self.__im.size[1]<self.__itc.size[1]:
        #    print('Main image is smaller than image for encrypt. Message will be cutted off.')

        pix = self.__im.load()
        itc_pix = self.__itc.load()
        width,height = self.__im.size

        for x in range(0, width):
            for y in range(0, height):
                try: #TODO: Implement pop-up like errors
                    pix[x,y] = self.__pixWrite(pix[x,y], self.__pixToGray(itc_pix[x,y]))
                    QtCore.QThread.sleep(0.1)
                except IndexError:
                    pass
            self.progress.emit(round(100*x/width))
        self.__im.save(self.__out)






















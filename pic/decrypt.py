#!/usr/bin/python
# -*- coding: utf-8 -*-
#TODO: Write the documentation

from PySide import QtCore

from PIL import Image
class Decrypt (QtCore.QThread): #TODO: <!> REFACTOR WHOLE CLASS </!>
    progress = QtCore.Signal(int)

    def __init__(self, image, parent=None):
        super(Decrypt, self).__init__(parent)
        self.__image = image
        self.__parent = parent

        try: #TODO: Implement pop-up like errors
            self.iTE = Image.open(self.__image)
        except FileNotFoundError as err:
            print(err) #TODO: Error Handling

    @staticmethod
    def __readBinListToPix(x): #TODO: Implement something faster than that
        g = [bin(x[0])[-1:], bin(x[1])[-1:], bin(x[2])[-1:]]
        n = round(int(str(g[0]) + g[1] + g[2],2)*256/7)
        return n, n, n

    def run(self):
        ite_pix = self.iTE.load()
        width,height = self.iTE.size
        image = Image.new('RGB', (width, height))
        im_pix = image.load()

        for x in range(0, width):
            for y in range(0, height):
                im_pix[x,y] = self.__readBinListToPix(ite_pix[x,y])
                QtCore.QThread.sleep(0.1)
            self.progress.emit(round(100*x/width))

        image.show()

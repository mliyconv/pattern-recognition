import cv2 as cv
import numpy as np
import math
from PIL import Image

class Preprocessor():
    inDir = "ressources/"
    outDir = "output/"
    skelDir = "skeleton/"
    prepDir = "preprocessed/"

    def __init__(self, inPath, outPath, withSkeleton = False, scale=3):
        self.img = cv.imread(self.inDir + inPath, 0)

        self.height, self.width = self.img.shape
        resizedImg = cv.resize(self.img, (self.width*scale, self.height*scale))
        self.height *= scale
        self.width *= scale

        # binarize image
        # ret2, self.img = cv.threshold(self.img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        ret2, self.img = cv.threshold(resizedImg, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        # dst = cv.fastNlMeansDenoising(self.img, None)
        self.smooth()

        # cv.imwrite(self.outDir + self.prepDir + outPath, dst)
        cv.imwrite(self.outDir + self.prepDir + outPath, self.img)

        if(withSkeleton):
            self.skeletonize()
            cv.imwrite(self.outDir + self.skelDir + outPath, self.skelImg)


    def smooth(self):
        self.filling()
        self.thinning()

    def filling(self):
        for y in range(1, self.height-2):
            for x in range(1, self.width-2):
                if(self.img.item(y, x) == 0):
                    continue
                a = self.img.item(y-1, x-1) == 0
                b = self.img.item(y-1, x) == 0
                c = self.img.item(y-1, x+1) == 0
                d = self.img.item(y, x-1) == 0
                e = self.img.item(y, x+1) == 0
                f = self.img.item(y+1, x-1) == 0
                g = self.img.item(y+1, x) == 0
                h = self.img.item(y+1, x+1) == 0

                if((a and h) or (b and g) or (c and f) or (d and e)):
                    self.img.itemset((y, x), 0)
                    # self.img.itemset((y, x, 1), 0)
                    # self.img.itemset((y, x, 2), 0)
    
    def thinning(self):
        for y in range(1, self.height-2):
            for x in range(1, self.width-2):
                if (self.img.item(y, x) == 255):
                    continue

                a = self.img.item(y - 1, x - 1) == 0
                b = self.img.item(y - 1, x) == 0
                c = self.img.item(y - 1, x + 1) == 0
                d = self.img.item(y, x - 1) == 0
                e = self.img.item(y, x + 1) == 0
                f = self.img.item(y + 1, x - 1) == 0
                g = self.img.item(y + 1, x) == 0
                h = self.img.item(y + 1, x + 1) == 0

                if(not(((a or b or d) and (e or g or h)) or ((b or c or e) and (d or f or g)))):
                    self.img.itemset((y, x), 255)
                    # self.img.itemset((y, x, 1), 255)
                    # self.img.itemset((y, x, 2), 255)

    def thinningIteration(self, im, iter):
        height, width = im.shape
        I, dst = im, np.zeros(im.shape, np.uint8)

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if(im.item(y, x) == 0):
                    continue

                p2 = im.item(y-1, x)
                p3 = im.item(y-1, x+1)
                p4 = im.item(y, x+1)
                p5 = im.item(y+1, x+1)
                p6 = im.item(y+1, x)
                p7 = im.item(y+1, x-1)
                p8 = im.item(y, x-1)
                p9 = im.item(y-1, x-1)

                A = (p2 == 0 and p3 == 1) + (p3 == 0 and p4 == 1) + (p4 == 0 and p5 == 1) + (p5 == 0 and p6 == 1) + (p6 == 0 and p7 == 1) + (p7 == 0 and p8 == 1) + (p8 == 0 and p9 == 1) + (p9 == 0 and p2 == 1)

                B = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9

                if(iter == 0):
                    m1 = (p2 * p4 * p6)
                else:
                    m1 = (p2 * p4 * p8)

                if(iter == 0):
                    m2 = (p4 * p6 * p8)
                else:
                    m2 = (p2 * p6 * p8)

                if(A == 1 and 2 <= B and B <= 6 and m1 == 0 and m2 == 0):
                    dst.itemset((y, x), 0)
                else:
                    dst.itemset((y, x), 1)

        return dst

    def skeletonize(self):
        dst = self.reverse(self.img.copy() / 255)

        prev = np.zeros(self.img.shape[:2], np.uint8)
        diff = None

        while True:
            dst = self.thinningIteration(dst, 0)
            dst = self.thinningIteration(dst, 1)
            diff = np.absolute(dst - prev)
            prev = dst.copy()
            if np.sum(diff) == 0:
                break

        self.skelImg = self.reverse(dst) * 255

    def reverse(self, src):
        height, width = src.shape

        for y in range(0, height - 1):
            for x in range(0, width - 1):
                if(src.item(y, x) == 0):
                    src.itemset((y,x), 1)
                else:
                    src.itemset((y,x), 0)

        return src

    # DEPRECATED
    # def binarize(self):
    #     # img = cv.imread(path, cv.CV_LOAD_IMAGE_GRAYSCALE)
    #     # (thresh, im_bw) = cv.threshold(img, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    #     self.greyscale();
    #
    #     for y in range(self.height-1):
    #         for x in range(self.width-1):
    #             pixel = self.img.item(y, x)
    #             if(pixel > self.threshold):
    #                 self.img.itemset((y, x), 255)
    #                 self.img.itemset((y, x, 1), 255)
    #                 self.img.itemset((y, x, 2), 255)
    #             else:
    #                 self.img.itemset((y, x, 0), 0)
    #                 self.img.itemset((y, x, 1), 0)
    #                 self.img.itemset((y, x, 2), 0)
    #
    # def greyscale(self):
    #     totalValue = 0;
    #
    #     for y in range(self.height-1):
    #         for x in range(self.width-1):
    #             blue = self.img.item(y, x, 0)
    #             green = self.img.item(y, x, 1)
    #             red = self.img.item(y, x, 2)
    #             average = (int(blue) + int(green) + int(red))/3
    #             self.img.itemset((y, x, 0), average)
    #             self.img.itemset((y, x, 1), average)
    #             self.img.itemset((y, x, 2), average)
    #             totalValue += average
    #
    #     self.threshold = int((totalValue/(self.width*self.height)))
    #
    # def normalize(self):
    #     NEW_WIDTH = 1000
    #     NEW_HEIGHT = 1000
    #     normalizedImg = np.zeros((NEW_HEIGHT, NEW_WIDTH))
    #
    #     wRatio = float(NEW_WIDTH)/float(self.width)
    #     hRatio = float(NEW_HEIGHT)/float(self.height)
    #
    #     for y in range(0, self.height-1):
    #         for x in range (0,  self.width-1):
    #             newX = int(round(x*wRatio))
    #             newY = int(round(y*hRatio))
    #
    #             pixelVal = self.img.item(y, x)
    #             if(newY < NEW_HEIGHT and newX < NEW_WIDTH):
    #                 normalizedImg.itemset((newY, newX), pixelVal)
    #                 # normalizedImg.itemset((newX, newY), pixelVal)
    #                 # normalizedImg.itemset((newX, newY), pixelVal)
    #
    #             if((newY+1) < NEW_HEIGHT and (newX+1) < NEW_WIDTH):
    #                 normalizedImg.itemset((newY+1, newX+1), pixelVal)
    #                 # normalizedImg.itemset((newX+1, newY+1), pixelVal)
    #                 # normalizedImg.itemset((newX+1, newY+1), pixelVal)
    #
    #     self.normalizedImg  = normalizedImg
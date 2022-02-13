import os
# import random
import numpy as np
import cv2
import json
# from sklearn.ensemble import RandomForestClassifier
# import pandas

from xml.dom import minidom
from dataclasses import dataclass

class Decode_Data:
    path_anno = "annotations\\"
    path_images = "images\\"
    DataUnit_list = []

    def generate_list(self):
        onlyfiles = [f for f in os.listdir(self.path_anno) if os.path.isfile(os.path.join(self.path_anno, f))]
        for i in range(len(onlyfiles)):
            onlyfiles[i] = onlyfiles[i][0:len(onlyfiles[i])-4]
        self.names_list = onlyfiles # ( ͡° ͜ʖ ͡°)

    def fill_object_list(self):
        for name in self.names_list:
            self.DataUnit_list.append( DataUnit(name,self.path_anno,self.path_images) )

        # testowanie
        # self.DataUnit_list.append(DataUnit("road0", self.path_anno, self.path_images))
        # self.DataUnit_list.append(DataUnit("road1", self.path_anno, self.path_images))
        # self.DataUnit_list.append(DataUnit("road2", self.path_anno, self.path_images))
        print()

    # def save_DataUnit_list(self):
    #     str = json.dumps(self.DataUnit_list[0].__dict__,skipkeys=True)
    #     print(str)

class DataUnit:

    def __init__(self,filename,path_anno,path_images):
        self.name = filename
        self.path_anno = path_anno
        self.path_images = path_images

        self.read_annotation()
        self.read_image()

    def read_annotation(self):
        full_path = self.path_anno + self.name + ".xml"
        doc = minidom.parse(full_path)

        self.width = int(doc.getElementsByTagName('width')[0].childNodes[0].data)
        self.height = int(doc.getElementsByTagName('height')[0].childNodes[0].data)
        self.class_name = doc.getElementsByTagName('name')[0].childNodes[0].data
        self.xmin = int(doc.getElementsByTagName('xmin')[0].childNodes[0].data)
        self.xmax = int(doc.getElementsByTagName('xmax')[0].childNodes[0].data)
        self.ymin = int(doc.getElementsByTagName('ymin')[0].childNodes[0].data)
        self.ymax = int(doc.getElementsByTagName('ymax')[0].childNodes[0].data)

    def read_image(self):
        img = cv2.imread(self.path_images+self.name+".png")
        cropped_img = img[self.ymin:self.ymax,self.xmin:self.xmax]
        self.image = cropped_img
        #self.image_to_list = self.image.tolist()




# TODO zapisac liste obiektow wraz z zdekodowanymi obrazami do pliku wtedy to jest koniec w tym pliku .py (opcjonalnie)
# nastepnie w nastepnym ogarnac skrypt do dzielenia na train i test

   
    

#dekoder1 = Decode_Data();
path = "annotations\\"
filename = "road0"
#test = dekoder1.read_annotation(path,filename)
# test = DataUnit("road0","annotations\\","images\\")
# test.read_annotation()
# test.read_image()
# cv2.imshow("a",test.image)
# cv2.waitKey(0)

dekoder1 = Decode_Data()
dekoder1.generate_list()
dekoder1.fill_object_list()
#dekoder1.save_DataUnit_list()
print()



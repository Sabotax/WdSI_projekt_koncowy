# import os
# import random
import numpy as np
import cv2
# from sklearn.ensemble import RandomForestClassifier
# import pandas

from xml.dom import minidom
from dataclasses import dataclass

class Decode_Data:

    def read_annotation(self,path,name):
        full_path = path+name+".xml";
        doc = minidom.parse(full_path)
        
        width = doc.getElementsByTagName('width')[0].childNodes[0].data
        height = doc.getElementsByTagName('height')[0].childNodes[0].data
        class_name = doc.getElementsByTagName('name')[0].childNodes[0].data
        xmin = doc.getElementsByTagName('xmin')[0].childNodes[0].data
        xmax = doc.getElementsByTagName('xmax')[0].childNodes[0].data
        ymin = doc.getElementsByTagName('ymin')[0].childNodes[0].data
        ymax = doc.getElementsByTagName('ymax')[0].childNodes[0].data
        
        return DataUnit(name, width, height, xmin, xmax, ymin, ymax, class_name,None)
    
    def read_image(self,ob):
        ob.image = cv2.imread("images\\"+ob.filename+".png")
        print()
    
    
@dataclass
class DataUnit:
    filename: str
    width: int 
    height: int 
    box_xmin: int
    box_xmax: int
    box_ymin: int
    box_ymax: int
    class_name: str
    image: np.array
   
    

dekoder1 = Decode_Data();
path = "annotations\\"
filename = "road0"
test = dekoder1.read_annotation(path,filename)
dekoder1.read_image(test)
print()



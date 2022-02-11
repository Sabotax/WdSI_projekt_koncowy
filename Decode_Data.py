# import os
# import random
# import numpy as np
# import cv2
# from sklearn.ensemble import RandomForestClassifier
# import pandas

from xml.dom import minidom
from dataclasses import dataclass

class Decode_Data:
    
    # def __init__():
    #     print("-")

    def read_annotation(self,path,name):
        full_path = path+name;
        doc = minidom.parse(full_path)
        
        width = doc.getElementsByTagName('width')[0].childNodes[0].data
        height = doc.getElementsByTagName('height')[0].childNodes[0].data
        class_name = doc.getElementsByTagName('name')[0].childNodes[0].data
        xmin = doc.getElementsByTagName('xmin')[0].childNodes[0].data
        xmax = doc.getElementsByTagName('xmax')[0].childNodes[0].data
        ymin = doc.getElementsByTagName('ymin')[0].childNodes[0].data
        ymax = doc.getElementsByTagName('ymax')[0].childNodes[0].data
        
        return Annotation(name, width, height, xmin, xmax, ymin, ymax, class_name)
    
    
@dataclass
class Annotation:
    filename: str
    width: int 
    height: int 
    box_xmin: int
    box_xmax: int
    box_ymin: int
    box_ymax: int
    class_name: str
   
    

dekoder1 = Decode_Data();
path = "annotations\\"
filename = "road0.xml"
test = dekoder1.read_annotation(path,filename)


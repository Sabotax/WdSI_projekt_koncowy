import os
# import random
import numpy as np
import cv2
#import json
# from sklearn.ensemble import RandomForestClassifier
# import pandas

from xml.dom import minidom
from dataclasses import dataclass
import pandas

class Decode_Data:
    path_anno = "annotations\\"
    path_images = "images\\"
    DataUnit_dict = {"name": [],
                     "width": [],
                     "height": [],
                     "class_name_true": [],
                     "class_name_identified": [],
                     "image": []}



    def __init__(self):
        self.generate_units_list()
        self.fill_object_list()
        self.split_to_train_and_test()
        self.database_train = pandas.DataFrame(self.dict_train)
        self.database_test = pandas.DataFrame(self.dict_test)
        #print(self.database)
        self.show_all_classes()

    def generate_units_list(self):
        onlyfiles = [f for f in os.listdir(self.path_anno) if os.path.isfile(os.path.join(self.path_anno, f))]
        for i in range(len(onlyfiles)):
            onlyfiles[i] = onlyfiles[i][0:len(onlyfiles[i])-4]
        self.names_list = onlyfiles # ( ͡° ͜ʖ ͡°)

    def fill_object_list(self):
        for name in self.names_list:

            #xml
            full_path = self.path_anno + name + ".xml"
            doc = minidom.parse(full_path)

            self.DataUnit_dict["name"].append(name)
            self.DataUnit_dict["width"].append(int(doc.getElementsByTagName('width')[0].childNodes[0].data))
            self.DataUnit_dict["height"].append(int(doc.getElementsByTagName('height')[0].childNodes[0].data))
            self.DataUnit_dict["class_name_true"].append(doc.getElementsByTagName('name')[0].childNodes[0].data)
            self.DataUnit_dict["class_name_identified"].append(None)
            xmin = int(doc.getElementsByTagName('xmin')[0].childNodes[0].data)
            xmax = int(doc.getElementsByTagName('xmax')[0].childNodes[0].data)
            ymin = int(doc.getElementsByTagName('ymin')[0].childNodes[0].data)
            ymax = int(doc.getElementsByTagName('ymax')[0].childNodes[0].data)
            #img
            img = cv2.imread(self.path_images + name + ".png")
            cropped_img = img[ymin:ymax, xmin:xmax]
            self.DataUnit_dict["image"].append(cropped_img)

    def show_all_classes(self):
        print(self.database["class_name_true"].value_counts())
        #output
        # speedlimit
        # 652
        # crosswalk
        # 88
        # stop
        # 76
        # trafficlight
        # 61
        # Name: class_name_true, dtype: int64

    def split_to_train_and_test(self,speedlimit_n,crosswalk_n,stop_n,traffic_light_n):
        data_train = {"name": [],
            "width": [],
            "height": [],
            "class_name_true": [],
            "class_name_identified": [],
            "image": [] }

        data_test = {"name": [],
            "width": [],
            "height": [],
            "class_name_true": [],
            "class_name_identified": [],
            "image": [] }

        part = 1/3 #ile trafi do train (reszta do test)

        speedlimit_c = 0
        crosswalk_c = 0
        stop_c = 0
        traffic_light_c = 0

        for i in range(len(self.database)) :

            if self.DataUnit_dict["class_name_true"][i] == "speedlimit":

                if speedlimit_c < speedlimit_n * part:
                    data_train["name"].append(self.DataUnit_dict["name"][i])
                    data_train["width"].append(self.DataUnit_dict["width"][i])
                    data_train["height"].append(self.DataUnit_dict["height"][i])
                    data_train["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_train["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_train["image"].append(self.DataUnit_dict["image"])
                else:
                    data_test["name"].append(self.DataUnit_dict["name"][i])
                    data_test["width"].append(self.DataUnit_dict["width"][i])
                    data_test["height"].append(self.DataUnit_dict["height"][i])
                    data_test["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_test["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_test["image"].append(self.DataUnit_dict["image"][i])

                speedlimit_c += 1

            if self.DataUnit_dict["class_name_true"][i] == "crosswalk":

                if crosswalk_c < crosswalk_n * part:
                    data_train["name"].append(self.DataUnit_dict["name"][i])
                    data_train["width"].append(self.DataUnit_dict["width"][i])
                    data_train["height"].append(self.DataUnit_dict["height"][i])
                    data_train["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_train["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_train["image"].append(self.DataUnit_dict["image"])
                else:
                    data_test["name"].append(self.DataUnit_dict["name"][i])
                    data_test["width"].append(self.DataUnit_dict["width"][i])
                    data_test["height"].append(self.DataUnit_dict["height"][i])
                    data_test["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_test["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_test["image"].append(self.DataUnit_dict["image"][i])

                crosswalk_c += 1

            if self.DataUnit_dict["class_name_true"][i] == "stop":

                if stop_c < stop_n * part:
                    data_train["name"].append(self.DataUnit_dict["name"][i])
                    data_train["width"].append(self.DataUnit_dict["width"][i])
                    data_train["height"].append(self.DataUnit_dict["height"][i])
                    data_train["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_train["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_train["image"].append(self.DataUnit_dict["image"])
                else:
                    data_test["name"].append(self.DataUnit_dict["name"][i])
                    data_test["width"].append(self.DataUnit_dict["width"][i])
                    data_test["height"].append(self.DataUnit_dict["height"][i])
                    data_test["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_test["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_test["image"].append(self.DataUnit_dict["image"][i])

                stop_c += 1

            if self.DataUnit_dict["class_name_true"][i] == "traffic_light":

                if traffic_light_c < traffic_light_n * part:
                    data_train["name"].append(self.DataUnit_dict["name"][i])
                    data_train["width"].append(self.DataUnit_dict["width"][i])
                    data_train["height"].append(self.DataUnit_dict["height"][i])
                    data_train["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_train["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_train["image"].append(self.DataUnit_dict["image"])
                else:
                    data_test["name"].append(self.DataUnit_dict["name"][i])
                    data_test["width"].append(self.DataUnit_dict["width"][i])
                    data_test["height"].append(self.DataUnit_dict["height"][i])
                    data_test["class_name_true"].append(self.DataUnit_dict["class_name_true"][i])
                    data_test["class_name_identified"].append(self.DataUnit_dict["class_name_identified"][i])
                    data_test["image"].append(self.DataUnit_dict["image"][i])

                traffic_light_c += 1

        self.dict_train = data_train
        self.dict_test = data_test




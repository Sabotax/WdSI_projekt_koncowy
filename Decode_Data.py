import os
# import random
import shutil
import numpy as np
import cv2
import pickle
import json
# from sklearn.ensemble import RandomForestClassifier
# import pandas

from xml.dom import minidom
from dataclasses import dataclass
import pandas

class Decode_Data:
    path_anno = "annotations\\"
    path_images = "images\\"

    path_anno_train = "train\\annotations\\"
    path_anno_test = "test\\annotations\\"
    path_img_train = "train\\images\\"
    path_img_test = "test\\images\\"

    DataUnit_dict = {"name": [],
                     "width": [],
                     "height": [],
                     "class_name_true": [],
                     "class_name_identified": [],
                     "image": [],
                     "box_true": [],
                     "box_identified": [],
                     "ilosc_obiektow":[],}



    def __init__(self):

        if os.path.isdir("train"):
            print("tworze baze danych 2")

            self.generate_units_list(self.path_anno_train)
            self.fill_object_list(self.path_anno_train,self.path_img_train)
            self.database_train = pandas.DataFrame(self.DataUnit_dict)

            self.DataUnit_dict = {"name": [],
                             "width": [],
                             "height": [],
                             "class_name_true": [],
                             "class_name_identified": [],
                             "image": [],
                             "box_true": [],
                             "box_identified": [],
                             "ilosc_obiektow": [], }

            self.generate_units_list(self.path_anno_test)
            self.fill_object_list(self.path_anno_test,self.path_img_test)
            self.database_test = pandas.DataFrame(self.DataUnit_dict)

            print("stworzono bazy danych 2 pomyslnie")
        else:
            print("tworze bazy danych")
            self.generate_units_list(self.path_anno)
            self.fill_object_list(self.path_anno,self.path_images)
            self.split_to_train_and_test(652,88,76,61)
            self.database_train = pandas.DataFrame(self.dict_train)
            self.database_test = pandas.DataFrame(self.dict_test)
            self.move_reorganize()

            self.generate_units_list(self.path_anno_train)
            self.fill_object_list(self.path_anno_train, self.path_img_train)
            self.database_train = pandas.DataFrame(self.DataUnit_dict)

            self.DataUnit_dict = {"name": [],
                                  "width": [],
                                  "height": [],
                                  "class_name_true": [],
                                  "class_name_identified": [],
                                  "image": [],
                                  "box_true": [],
                                  "box_identified": [],
                                  "ilosc_obiektow": [], }

            self.generate_units_list(self.path_anno_test)
            self.fill_object_list(self.path_anno_test, self.path_img_test)
            self.database_test = pandas.DataFrame(self.DataUnit_dict)

            print("stworzono bazy danych i przeorganizowano pliki pomyslnie")



    def generate_units_list(self,path):
        onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        for i in range(len(onlyfiles)):
            onlyfiles[i] = onlyfiles[i][0:len(onlyfiles[i])-4]
        self.names_list = onlyfiles # ( ͡° ͜ʖ ͡°)

    def fill_object_list(self,path_xml,path_images):

        for name in self.names_list:
            full_path = path_xml + name + ".xml"
            doc = minidom.parse(full_path)

            width = int(doc.getElementsByTagName('width')[0].childNodes[0].data)
            height = int(doc.getElementsByTagName('height')[0].childNodes[0].data)
            elements = doc.getElementsByTagName('object')
            for obj in elements:
                # elementy są w 1 3 5 7 9 11
                # 1.child[0] = typ (trafficlight)
                # 3.child[0] = pose (unspecified)
                # 5.child[0] = truncated (0)
                # 7.child[0] = occluded (0)
                # 9.child[0] = difficult (0)
                # 11.child[1].child[0] = xmin
                # 11.child[3].child[0] = ymin
                # 11.child[5].child[0] = xmax
                # 11.child[7].child[0] = ymax
                self.DataUnit_dict["name"].append(name)
                self.DataUnit_dict["width"].append(width)
                self.DataUnit_dict["height"].append(height)
                self.DataUnit_dict["class_name_true"].append(obj.childNodes[1].childNodes[0].data)
                self.DataUnit_dict["class_name_identified"].append(None)
                self.DataUnit_dict["ilosc_obiektow"].append(len(elements))
                xmin = int(obj.childNodes[11].childNodes[1].childNodes[0].data)
                xmax = int(obj.childNodes[11].childNodes[5].childNodes[0].data)
                ymin = int(obj.childNodes[11].childNodes[3].childNodes[0].data)
                ymax = int(obj.childNodes[11].childNodes[7].childNodes[0].data)
                self.DataUnit_dict["box_true"].append([xmin, xmax, ymin, ymax])
                self.DataUnit_dict["box_identified"].append(None)
                img = cv2.imread(path_images + name + ".png")
                self.DataUnit_dict["image"].append(img)
                #self.DataUnit_dict["desc"].append(None)
                #cropped_img = img[ymin:ymax, xmin:xmax]
#TODO pomyslec o odchudzeniu bazy danych (na przyklad train nie potrzebuje image full), (wystarczy image full i odpowiednie odczytywanie boxem a nie)
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

    def scandown(self,elements, indent):
        for el in elements:
            print("   " * indent + "nodeName: " + str(el.nodeName))
            print("   " * indent + "nodeValue: " + str(el.nodeValue))
            print("   " * indent + "childNodes: " + str(el.childNodes))
            self.scandown(el.childNodes, indent + 1)

    def split_to_train_and_test(self,speedlimit_n,crosswalk_n,stop_n,traffic_light_n):
        data_train = {"name": [],
                     "width": [],
                     "height": [],
                     "class_name_true": [],
                     "image": [],
                     "box_true": [],
                     "ilosc_obiektow":[]}

        data_test = {"name": [],
                     "width": [],
                     "height": [],
                     "class_name_true": [],
                     "class_name_identified": [],
                     "image": [],
                     "box_true": [],
                     "box_identified": [],
                     "ilosc_obiektow":[]}

        part = 1/3 #ile trafi do train (reszta do test)

        speedlimit_c = 0
        crosswalk_c = 0
        stop_c = 0
        traffic_light_c = 0

        #edit po zrobieniu całości wyrównujący ilość speedlimit (które jest jakieś 10 razy więcej niż reszty) do poziomu reszty
        if True: #94% 70% 71% 74%
            min1 = np.min([speedlimit_n*part,crosswalk_n*part,traffic_light_n*part,stop_n*part])

            speedlimit_end = min1
            crosswalk_end = min1
            stop_end = min1
            traffic_light_end = min1
        elif False: #93% 83%
            speedlimit_end = speedlimit_n*part
            crosswalk_end = crosswalk_n*part
            stop_end = stop_n*part
            traffic_light_end = traffic_light_n*part
        elif False:
            speedlimit_end = speedlimit_n * part / 6
            crosswalk_end = crosswalk_n * part
            stop_end = stop_n * part
            traffic_light_end = traffic_light_n * part
        #edit end

        for i in range(len(self.DataUnit_dict["name"])) :

            if self.DataUnit_dict["class_name_true"][i] == "speedlimit":
                if speedlimit_c < speedlimit_end:
                    for pole in data_train.keys():
                        data_train[pole].append(self.DataUnit_dict[pole][i])
                else:
                    for pole in data_test.keys():
                        data_test[pole].append(self.DataUnit_dict[pole][i])

                speedlimit_c += 1

            if self.DataUnit_dict["class_name_true"][i] == "crosswalk":
                if crosswalk_c < crosswalk_end:
                    for pole in data_train.keys():
                        data_train[pole].append(self.DataUnit_dict[pole][i])
                else:
                    for pole in data_test.keys():
                        data_test[pole].append(self.DataUnit_dict[pole][i])

                crosswalk_c += 1

            if self.DataUnit_dict["class_name_true"][i] == "stop":
                if stop_c < stop_end:
                    for pole in data_train.keys():
                        data_train[pole].append(self.DataUnit_dict[pole][i])
                else:
                    for pole in data_test.keys():
                        data_test[pole].append(self.DataUnit_dict[pole][i])

                stop_c += 1

            if self.DataUnit_dict["class_name_true"][i] == "trafficlight":
                if traffic_light_c < traffic_light_end:
                    for pole in data_train.keys():
                        data_train[pole].append(self.DataUnit_dict[pole][i])
                else:
                    for pole in data_test.keys():
                        data_test[pole].append(self.DataUnit_dict[pole][i])

                traffic_light_c += 1

        self.dict_train = data_train
        self.dict_test = data_test

    def move_reorganize(self):
        if not os.path.isdir("train"):
            os.mkdir("train")
            os.mkdir("train\\images")
            os.mkdir("train\\annotations")

            for index, row in self.database_train.iterrows():
                if os.path.isfile("annotations\\" + row["name"] + ".xml"):
                    os.rename("annotations\\"+row["name"]+".xml","train\\annotations\\"+row["name"]+".xml")
                if os.path.isfile("images\\"+row["name"]+".png"):
                    os.rename("images\\"+row["name"]+".png","train\\images\\"+row["name"]+".png")

        if not os.path.isdir("test"):
            os.mkdir("test")
            os.mkdir("test\\images")
            os.mkdir("test\\annotations")

            for index, row in self.database_test.iterrows():
                if os.path.isfile("annotations\\" + row["name"] + ".xml"):
                    os.rename("annotations\\"+row["name"]+".xml","test\\annotations\\"+row["name"]+".xml")
                if os.path.isfile("images\\" + row["name"] + ".png"):
                    os.rename("images\\"+row["name"]+".png","test\\images\\"+row["name"]+".png")

        shutil.rmtree("annotations")
        os.rmdir("images")

        # warto zauważyć że o ile podział zgadza się z w bazie danych, to w podziale zdjęc na foldery, zdjecie wyladuje tam gdzie zostanie najpierw zabrane, a staranie
        # by to nie miało miejsca w przypadku gdy i tak nie robi to różnicy dla uczenia maszynowego, a i tak specjalnie są dzielone te foldery tylko dla
        # sprawdzającego to nie ma potrzeby większość sił zużywać na obracanie plikami poprawnie

# TODO jestli ilosc obektow > 1 to wtedy moze przesunac, ale licnzik zwieksza o n, dodatkowa zawsze sprawdza zanim przesunie czy ma co przesunac zanim to zrobi i inkrementuje c
#dodatkowo jesli n>1 to wszystkie krotki gdzir n
# TODO train ograniczyc ilosc pol, zwlaszcza tylko image_cropped dzieki czemu moze byc tam uzywane bez znaczenia czy jest wiele na zdjeciu czy nie
# TODO zeby jakos rozsadnie dzielilo krotki jesli pochodza z tego samego zdjecia
# TODO w tym zamienic keys w kopiowaniu krotek na customowe bazy danych czyli z data_train.keys() itp



import os.path

import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

class Training_Ground:
    def __init__(self,data):
        self.data_train = data
        self.learn_bovw()
        self.data_train = self.extract_features(self.data_train)
        self.train()

    def learn_bovw(self):
        if os.path.isfile("voc.npy"):
            print("korzystam z poprzednio utworzonego voc.py")
        else:
            print("Rozpoczynam tworzenie voc.py")
            dict_size = 128
            bow = cv2.BOWKMeansTrainer(dict_size)
            sift = cv2.SIFT_create()

            for index,row in self.data_train.iterrows():
                #wycina obrazek w locie
                img_cropped = row['image'][row['box_true'][2]:row['box_true'][3], row['box_true'][0]:row['box_true'][1]]
                kpts = sift.detect(img_cropped, None)
                kpts, desc = sift.compute(img_cropped, kpts)

                if desc is not None:
                    bow.add(desc)

            vocabulary = bow.cluster()

            np.save('voc.npy', vocabulary)
            print("voc.npy zapisano pomyslnie")

    def extract_features(self,data):
        print("rozpoczynam extract_features")
        sift = cv2.SIFT_create()
        flann = cv2.FlannBasedMatcher_create()
        bow = cv2.BOWImgDescriptorExtractor(sift, flann)
        vocabulary = np.load('voc.npy')
        bow.setVocabulary(vocabulary)
        for index,row in data.iterrows():
            kpt = sift.detect(row["image"],None)
            desc = bow.compute(row["image"],kpt)
            row['desc'] = desc
        print("zakonczono extract_features")

        return data

    def train(self):
        print("rozpoczynam uczenie")
        descs = []
        labels = []
        for index,row in self.data_train.iterrows():
            if row['desc'] is not None:
                descs.append(row['desc'].squeeze(0))
                labels.append(row['class_name_true'])

        rf = RandomForestClassifier()
        rf.fit(descs, labels)

        self.rf = rf

        print("pomyslnie nauczono")

    def predict_one(self,ob):
        return self.rf.predict(ob)

    def predict_all(self,data):
        for index, row in self.data_train.iterrows():
            if row['desc'] is not None:
                row['class_name_identified'] = self.predict_one(row["desc"])

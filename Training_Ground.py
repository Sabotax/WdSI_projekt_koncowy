import cv2
import numpy as np
from io import StringIO

class Training_Ground:
    def __init__(self,data):
        self.data_train = data.database_train
        self.learn_bovw()

    def learn_bovw(self):
        print("Rozpoczynam tworzenie voc.py")
        dict_size = 128
        bow = cv2.BOWKMeansTrainer(dict_size)
        sift = cv2.SIFT_create()

        for index,row in self.data_train.iterrows():
            #wycina obrazek w locie
            img_cropped = row['image'][int(row['box_true'][2]):int(row['box_true'][3]), int(row['box_true'][0]):int(row['box_true'][1])]
            kpts = sift.detect(img_cropped, None)
            kpts, desc = sift.compute(img_cropped, kpts)

            if desc is not None:
                bow.add(desc)

        vocabulary = bow.cluster()

        np.save('voc.npy', vocabulary)
        print("voc.npy zapisano pomyslnie")
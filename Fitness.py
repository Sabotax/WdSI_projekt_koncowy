import numpy as np
from sklearn.metrics import confusion_matrix

class Fitness:
    #def __init__(self):

    def evaulate(self,data):
        print("Rozpoczynam ocene SI")
        print("Zle rozpoznano:")
        licznik = 0
        mianownik = 0
        pred_labels = []
        true_labels = []
        for index, row in data.iterrows():
            if row['desc'].v is not None and row['class_name_identified'] is not None:
                pred_labels.append(row['class_name_identified'])
                true_labels.append(row['class_name_true'])
                if row['class_name_identified'] == row['class_name_true']:
                    licznik += 1
                # else:
                #     print(row['name']+" prawdziwa: "+row["class_name_true"]+" rozpoznana: "+row['class_name_identified'])

            mianownik += 1
        accuracy = licznik / mianownik
        conf_matrix = confusion_matrix(true_labels, pred_labels,labels=["speedlimit", "crosswalk", "stop","trafficlight"])
        # traffic light zostaje najcześciej mylone i najczęściej jest mylone z speedlimit, w następnej kolejności stop i crosswalk są mylone ze speedlimit, ale też
        # w bazie danych jest taki problem, że speedlimit jest o wiele wiele więcej niż pozostałych więc średnio równomiernie
        print("---------")
        print("Accuracy:", accuracy)
        print("Mass confusion:")
        print(conf_matrix)
        # ------------------
        return

    def print_zadanie(self,data):
        string1 = ""
        for index,row in data.iterrows():
            if (row["class_name_identified"] == "crosswalk"
            and np.absolute(row["box_true"][0]-row["box_true"][1]) >row["width"]/10
            and np.absolute(row["box_true"][2]-row["box_true"][3]) >row["height"]/10):
                string1+=row["name"]+".png\r\n"+str(row["ilosc_obiektow"])+"\r\n"+str(row["box_true"][0])+" "+ str(row["box_true"][1])+" "+str(row["box_true"][2])+" "+str(row["box_true"][3])+"\r\n"

        with open('wyjscie_do_oceny.txt', 'w') as f:
            f.write(string1)


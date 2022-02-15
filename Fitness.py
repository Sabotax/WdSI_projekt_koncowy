from sklearn.metrics import confusion_matrix

class Fitness:
    #def __init__(self):

    def evaulate(self,data):

        licznik = 0
        mianownik = 0
        pred_labels = []
        true_labels = []
        for index, row in data.iterrows():
            if row['desc'] is not None:
                pred_labels.append(row['class_name_identified'])
                true_labels.append(row['class_name_true'])
                if row['class_name_identified'] == row['class_name_true']:
                    licznik += 1

                mianownik += 1
        accuracy = licznik / mianownik
        conf_matrix = confusion_matrix(true_labels, pred_labels)
        print("Accuracy:", accuracy)
        print("Mass confusion:")
        print(conf_matrix)
        # ------------------
        return

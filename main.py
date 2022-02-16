import io

import numpy as np
import os
import pandas
import pickle

from Decode_Data import *
from Training_Ground import *
from Fitness import *

dekoder = Decode_Data()
trainer = Training_Ground(dekoder.database_train)
extracted_data_test = trainer.extract_features(dekoder.database_test)
tester = Fitness()
data_test = trainer.predict_all(extracted_data_test)
tester.evaulate(data_test)

tester.print_zadanie(data_test)



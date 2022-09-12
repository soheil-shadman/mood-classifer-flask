## Package

import numpy as np
import pandas as pd
import librosa

## Keras

from keras.utils import np_utils
from keras.optimizers import SGD
from keras.models import model_from_json

## Sklearn
from sklearn.preprocessing import LabelEncoder

## Rest
from tqdm import tqdm
import os
import json
from datetime import datetime
from my_model.file_init_class import FileInitClass
from my_model.my_data_maker import MyDataMaker
from constant_info import DATA_PATH,WEIGHTS_PATH,MODELS_PATH,RESULT_PATH, DELETE_RAW_ITEMS


class MyModel:

    def __init__(self, model_number):
        FileInitClass()
        print('init model')
        self.data_maker = MyDataMaker(delete_raw_items=DELETE_RAW_ITEMS)
        self.my_model = None
        self.isModelUp=False
        self.input_duration = 3
        self.MODEL_NAME_JSON = 'my_model_json_' + str(model_number) + '.json'
        self.MODEL_WEIGHT = 'model_weight_aug_np_' + str(model_number) + '.h5'
        self.OPTIMIZER = SGD(learning_rate=0.0001, momentum=0.0, decay=0.0, nesterov=False)
        # self.load_model()

    def load_model(self):
        try:
            json_file = open(MODELS_PATH + self.MODEL_NAME_JSON, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)

            # load weights into new model
            loaded_model.load_weights(WEIGHTS_PATH + self.MODEL_WEIGHT)
            print("Loaded model from files")

            # evaluate loaded model on test data
            loaded_model.compile(loss='categorical_crossentropy', optimizer=self.OPTIMIZER, metrics=['accuracy'])
            self.my_model = loaded_model
            self.isModelUp=True
            return str('model loaded!')
        except:
            return str('cant load model')
            

    def clear_data_folder(self):
        try:
            files = os.listdir(DATA_PATH)
            for i in files:
                os.remove(DATA_PATH + i)
            return str('data folder cleared')
        except OSError as e:
            return str("Error: " + e.strerror)

    def clear_result_folder(self):
        try:
            files = os.listdir(RESULT_PATH)
            for i in files:
                os.remove(RESULT_PATH + i)
            return str('result folder cleared')
        except OSError as e:
            return str("Error: " + e.strerror)

    def start_processing_data(self):
       res= self.data_maker.process_data()
       return str(res)

    def predict_data(self, result_number):
        try:
            if self.my_model is None:
                return str('no model found ...')
            files = os.listdir(DATA_PATH)
            if len(files) == 0:
                return str('no files found ...')
            data_pred = pd.DataFrame(columns=['feature'])
            filenames = []
            for i in tqdm(range(len(files))):
                X, sample_rate = librosa.load(DATA_PATH + files[i], res_type='kaiser_fast',
                                              duration=self.input_duration,
                                              sr=22050 * 2,
                                              offset=0.5)

                sample_rate = np.array(sample_rate)
                mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13), axis=0)
                feature = mfccs

                if len(feature) < 259:
                    for j in range(len(feature) + 1, 260):
                        feature = np.append(feature, 0)
                filenames.append(files[i])
                data_pred.loc[i] = [feature]

            data_pred = data_pred.fillna(0)

            test_valid = pd.DataFrame(data_pred['feature'].values.tolist())
            test_valid = np.array(test_valid)

            test_valid_lb = np.array(['negative', 'neutral', 'positive'])
            lb = LabelEncoder()
            test_valid_lb = np_utils.to_categorical(lb.fit_transform(test_valid_lb))

            test_valid = np.expand_dims(test_valid, axis=2)
            print('data preprocessing over ...')
            preds = self.my_model.predict(test_valid,
                                          batch_size=16,
                                          verbose=1)
            preds1 = preds.argmax(axis=1)
            abc = preds1.astype(int).flatten()
            predictions = (lb.inverse_transform((abc)))
            jsonValue = []
            print('prediction done ...')
            for i in range(0, len(filenames)):
                jsonValue.append({
                    "filename": filenames[i],
                    "mood": predictions[i],
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })
            with open(RESULT_PATH + 'result_' + str(result_number) + ".json", 'w') as f:
                json.dump(jsonValue, f, ensure_ascii=False)
            return str('result saved !')    
        except:
            return str('there was an error with prediction ')

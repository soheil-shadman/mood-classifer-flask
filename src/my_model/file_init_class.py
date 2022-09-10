import os
from constant_info import RAW_DATA_PATH , DATA_PATH,WEIGHTS_PATH,MODELS_PATH,RESULT_PATH
class FileInitClass:
    def __init__(self):
        print('init paths')
 
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
        if not os.path.exists(RESULT_PATH):
            os.makedirs(RESULT_PATH)
        if not os.path.exists(MODELS_PATH):
            os.makedirs(MODELS_PATH)
        if not os.path.exists(WEIGHTS_PATH):
            os.makedirs(WEIGHTS_PATH)
        if not os.path.exists(RAW_DATA_PATH):
            os.makedirs(RAW_DATA_PATH)


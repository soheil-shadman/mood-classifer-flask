import os
from constant_info import SESSION_PATH,WEIGHTS_PATH,MODELS_PATH
class FileInitClass:
    def __init__(self):

        if not os.path.exists(MODELS_PATH):
            os.makedirs(MODELS_PATH)
        if not os.path.exists(WEIGHTS_PATH):
            os.makedirs(WEIGHTS_PATH)
        if not os.path.exists(SESSION_PATH):
            os.makedirs(SESSION_PATH)


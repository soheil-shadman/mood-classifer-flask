from flask import abort  , make_response ,jsonify,Response
from constant_info import RAW_PATH , RESULT_PATH , DATA_PATH
import os
def isEmpty(val):
    if val is None:
        return True
    elif val =="":
        return True
    else:
        return False
def optionalValueHelper(val):
    if isEmpty(val):
        return None
    else :
        return val          
def SendError(status_code=500, message=''):
    response = make_response( jsonify(
                    {"error":message , "code": status_code}
                ),status_code)
    return response

def SendRes(data='',error=''):
    
    response = make_response(  jsonify(
                    {"error":error , "code": 200,"_data":data}
                ),200)

    return response;    

def makeNewSessionFolder(path):
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(path+RAW_PATH):
            os.makedirs(path+RAW_PATH)
        if not os.path.exists(path+RESULT_PATH):
            os.makedirs(path+RESULT_PATH)
        if not os.path.exists(path+DATA_PATH):
            os.makedirs(path+DATA_PATH)


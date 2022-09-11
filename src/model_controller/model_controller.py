import re
from flask import Blueprint , request
from constant_info import RESULT_PATH
from utils.utils import SendError , SendRes, isEmpty, optionalValueHelper
from werkzeug.utils import secure_filename
model_controller_blueprint = Blueprint('model_controller_blueprint', __name__)
from app import model , app
import os
from os.path import exists
import json

@model_controller_blueprint.route('/api/model-controller/<x>', methods=['POST','GET'])
def router(x):
    if x == 'init-model':
        return  __initmodel()
    elif x == 'predict-items':
        return  __predict() 
    elif x == 'model-status':
        return  __modelStatus()     
    elif x == 'process-raw-data':
        return  __start_processing_raw_data()    
    elif x == 'clear-results-folder':
        return  __clear_result_folder()
    elif x == 'clear-data-folder':
        return  clear_data_folder()
    elif x == 'get_results':
        return  __getResults()    
    elif x == 'get_single_result':
        return  __getSingleResult()     
    elif x == 'upload_audio':
        return  __upload_audio()                
    else :
        return SendError(403,"no route found")

def __initmodel():
    try:
     if request.method == 'POST':
        res =model.load_model()
        return SendRes(str(res)) 
    except Exception as e:
        return SendError(400, str(e))

def __modelStatus():
    try:
        if request.method == 'GET':
            if model.isModelUp == True:
                return SendRes(str('model is up')) 
            return SendRes(error='model not init')   
    except Exception as e:
        return SendError(400, str(e))       


def __clear_result_folder():
    try:
     if request.method == 'POST':
        res =model.clear_result_folder()
        return SendRes(res) 
    except Exception as e:
        return SendError(400, str(e))

def __upload_audio():
    try:
     if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file is None:
            return SendError(400, str('no file included'))
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return SendError(404, str('bad file !'))
        file_exists = exists(app.config['UPLOAD_PATH']+filename)    
        if file_exists :
              uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], "e"+filename))
        else:
          uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))      

        return SendRes('File Uploaded!')
    except Exception as e:
        return SendError(400, str(e))
 

def clear_data_folder():
    try:
     if request.method == 'POST':
        res =model.clear_data_folder()
        return SendRes(res) 
    except Exception as e:
        return SendError(400, str(e))

def __start_processing_raw_data():
    try:
     if request.method == 'POST':
        res =model.start_processing_data()
        return SendRes(res) 
    except Exception as e:
        return SendError(400, str(e))

def __predict():
    try:
     if request.method == 'POST':
        if request.is_json:
            body = request.get_json()
    
            if isEmpty(body.get('result_number')) :
                return SendError(400,'invalid result_number params')

            res =model.predict_data(int(body.get('result_number')))     
                  
            return SendRes(res) 
        else:
            return  SendError(400, 'The request payload is not in JSON format')
    except Exception as e:
        return SendError(400, str(e))

def __getSingleResult():
    try:
        if request.method == 'POST':
            if request.is_json:
                body = request.get_json()
        
                if isEmpty(body.get('result_number')) :
                    return SendError(400,'invalid result_number params')
            result_no= int(body.get('result_number'))
            files = os.listdir(RESULT_PATH)
            if len(files) == 0 :
                SendRes(str('no files found'))    
            res =  None 
            for i in files :
                if i == "result_"+str(result_no)+".json":
                    with open(RESULT_PATH+i) as jsonfile:
                        res=json.load(jsonfile)
                    
            if res is None:
                return SendError(404, str('No item :('))         

            return SendRes(res)    
        else:
            return  SendError(400, 'The request payload is not in JSON format')
    except Exception as e:
        return SendError(400, str(e))

def __getResults():
    try:
     if request.method == 'GET':
        result =[]
        files = os.listdir(RESULT_PATH)
        if len(files) == 0 :
            SendRes(str('no files found'))

        for i in files: 
            with open(RESULT_PATH+i) as jsonfile:
                result.append(json.load(jsonfile))
            
        return SendRes(result)    

    except Exception as e:
        return SendError(400, str(e))              

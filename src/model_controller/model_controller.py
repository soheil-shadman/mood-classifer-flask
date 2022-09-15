from datetime import datetime

from constant_info import RAW_PATH, SESSION_PATH, SESSIONS_FILE,RESULT_PATH,FEED_BACK_FILE,API_TOKEN
from flask import Blueprint, request
from utils.utils import SendError, SendRes, isEmpty, makeNewSessionFolder
from werkzeug.utils import secure_filename

model_controller_blueprint = Blueprint('model_controller_blueprint', __name__)
import json
import os
from os.path import exists

from app import app, model


@model_controller_blueprint.route('/api/model-controller/<x>', methods=['POST','GET'], strict_slashes=False)
def router(x):
    if 'api-token' in request.headers:
        api_token=request.headers['api-token']
        if api_token == None or api_token!=API_TOKEN:
            return SendError(404,"access denied")
    else:
        return SendError(404,"access denied")        
    if x == 'reload-model':
        return  __reloadmodel()
    elif x == 'make-session':
        return  __make_session()     
    elif x == 'clear-sessions-folder':
        return  __clear_sessions_folder()
    elif x == 'upload-audio':
        return  __upload_audio()      
    elif x == 'process-raw-data':
        return  __start_processing_raw_data()      
    elif x == 'predict-items':
        return  __predict()          
    elif x == 'get_session_file_result':
        return  __get_session_file_result()    
    elif x == 'get_session_results':
        return  __get_session_results()     
    elif x == 'feed_back_on_audio':
        return  __feed_back_on_audio()            
    else :
        return SendError(403,"no route found")

def __reloadmodel():
    try:
     if request.method == 'POST':
        res =model.load_model()
        return SendRes(str(res)) 
    except Exception as e:
        return SendError(400, str(e))

def __make_session():
    try:
        if request.method == 'POST':
            if model.isModelUp == True:
                session_Id= 0
                if exists(SESSIONS_FILE) == False:
                        with open(SESSIONS_FILE, mode='w') as f:
                            json.dump([], f)
                            f.close()    
                with open(SESSIONS_FILE, mode='r+') as seesionJson:
                    data=json.loads(seesionJson.read())
                    session_Id=len(data)+1
                    entry = {'session_Id':str(session_Id), 'date': str( datetime.now())}
                    data.append(entry)    
                    seesionJson.seek(0)
                    json.dump(data, seesionJson)
                    seesionJson.close()

                makeNewSessionFolder(SESSION_PATH+"session_"+str(session_Id)+"/")                
                return SendRes(str(session_Id)) 
            return SendError(message='model is not initiated for session')   
    except Exception as e:
        return SendError(400, str(e))       


def __upload_audio():
    
    try:
     if request.method == 'POST':

        data=request.form.get('session_id')
        if isEmpty(data) :
            return SendError(500,'invalid session_id param')
              
        session_id=int(data)  
        if session_id == -1 :
            return SendError(500,'no session_id recieved')

        uploaded_file = request.files['file']
        if uploaded_file is None:
                return SendError(500, str('no file included'))
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return SendError(500, str('wrong file type!'))
        filepath =SESSION_PATH+"session_"+str(session_id)+"/"+RAW_PATH     
        if exists(filepath) == False:
            return SendError('session_id path not exists')
        file_exists = exists(filepath+filename)    
        if file_exists :
            return SendError(500,'file already exists')
        else:
            uploaded_file.save(os.path.join(filepath, filename))      
            return SendRes('file uploaded!')
    except Exception as e:

        return SendError(400, str(e))
 

def __clear_sessions_folder():
    try:
     if request.method == 'POST':
        res =model.clear_sessions_folder()
        return SendRes(res) 
    except Exception as e:
        return SendError(400, str(e))


def __predict():
    try:
     if request.method == 'POST':
        if request.is_json:
            body = request.get_json()
      
            if isEmpty(body.get('session_id')) or isEmpty(body.get('filename')) :
                return SendError(500,'invalid params')

            session_id=int(body.get('session_id'))
            filename=body.get('filename')    
            res =model.predict_data(session_id=session_id,filename=filename)     
                  
            return SendRes(res) 
        else:
            return  SendError(500, 'The request payload is not in JSON format')
    except Exception as e:
        return SendError(400, str(e))

def __start_processing_raw_data():
    try:
        if request.method == 'POST':
            if request.is_json:
                body = request.get_json()
                if isEmpty(body.get('session_id')) or isEmpty(body.get('filename')) :
                    return SendError(500,'invalid params')

                session_id=int(body.get('session_id'))
                filename=body.get('filename')
                res =model.start_processing_data(session_id,filename)
                return SendRes(res) 
            else:
                return  SendError(500, 'The request payload is not in JSON format')    

    except Exception as e:
        return SendError(400, str(e))        

def __get_session_file_result():
    try:
        if request.method == 'POST':
            if request.is_json:
                body = request.get_json()
                if isEmpty(body.get('session_id')) or isEmpty(body.get('filename')) :
                    return SendError(500,'invalid params')

                session_id=int(body.get('session_id'))
                filename=body.get('filename').split('.')[0]
                file_name=SESSION_PATH+"session_"+str(session_id)+"/"+RESULT_PATH + 'result_' +filename+'.json'
                print('==================================')
                print(file_name)
                if exists(file_name) == False:
                     return SendError(500, str('File doesnt exist'))   
                res = None
                with open(file_name) as jsonfile:
                    res=json.load(jsonfile)     
                        
                if res is None:
                    return SendError(500, str('no item :('))         

                return SendRes(res)    
            else:
                return  SendError(400, 'The request payload is not in JSON format')
    except Exception as e:
        return SendError(400, str(e))

def __get_session_results():
    try:
        if request.method == 'POST':
          if request.is_json:
                body = request.get_json()
                if isEmpty(body.get('session_id')) :
                    return SendError(500,'invalid params')

                session_id=int(body.get('session_id'))    
                result =[]
                if exists(SESSION_PATH+"session_"+str(session_id)) == False:
                      SendRes(500,str('no session found'))

                files = os.listdir(SESSION_PATH+"session_"+str(session_id)+"/"+RESULT_PATH)
                if len(files) == 0 :
                    SendRes(500,str('no result found'))

                

                for i in files: 
                    with open(SESSION_PATH+"session_"+str(session_id)+"/"+RESULT_PATH+i) as jsonfile:
                        result.append(json.load(jsonfile))
                
                return SendRes(result)    
        else:
            return  SendError(400, 'The request payload is not in JSON format')    

    except Exception as e:
        return SendError(400, str(e))              

def __feed_back_on_audio():
    try:
        if request.method == 'POST':
            if request.is_json:
                body = request.get_json()
                if isEmpty(body.get('session_id')) or isEmpty(body.get('filename')) or isEmpty(body.get('mood')) or isEmpty(body.get('audio_duration')):
                    return SendError(500,'invalid params')
                mood =body.get('mood')
                print('mood')
        
                if mood not in ['positive','neutral','negative']:
                     return SendError(500,'invalid mood (positive , neutral , negative)')

                session_id=int(body.get('session_id'))
                audio_duration=int(body.get('audio_duration'))
                filename=body.get('filename')
                file_name=SESSION_PATH+"session_"+str(session_id)+"/"+RAW_PATH +filename

                if exists(file_name) == False:
                     return SendError(500, str('file / session doesnt exist'))   


                if exists(FEED_BACK_FILE) == False:
                    with open(FEED_BACK_FILE, mode='w') as f:
                        json.dump([], f)
                        f.close()    

                with open(FEED_BACK_FILE, mode='r+') as seesionJson:
                    data=json.loads(seesionJson.read())
                    session_Id=len(data)+1
                    entry = {'session_Id':str(session_Id), 'date': str( datetime.now()),'filename':filename,'mood':mood,'audio_duration':audio_duration}
                    data.append(entry)    
                    seesionJson.seek(0)
                    json.dump(data, seesionJson)
                    seesionJson.close()     

                return SendRes(data='feed back submitted')    
            else:
                return  SendError(400, 'The request payload is not in JSON format')
    except Exception as e:
        return SendError(400, str(e))
 


from flask import abort  , make_response ,jsonify,Response
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
def SendError(status_code, message):
    response = make_response(  jsonify(
                    {"error":message , "code": status_code}
                ),)
    response.status_code = status_code
    print(str(response))
    print(message)
    abort(response)

def SendRes(data='',error=''):
    
    response = make_response(  jsonify(
                    {"error":error , "code": 200,"_data":data}
                ),)
    response.status_code = 200
    return response;    
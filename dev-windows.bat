py -m venv env
CALL env\Scripts\activate
set FLASK_APP=src/app.py
set FLASK_RUN_PORT=8080
set FLASK_DEBUG=1
flask run --host=0.0.0.0
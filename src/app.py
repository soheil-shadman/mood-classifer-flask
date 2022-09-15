from flask import Flask
from constant_info import MODEL_NUMBER
from my_model.my_model import MyModel


model = MyModel(model_number=MODEL_NUMBER)
model.load_model()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 *1024
app.config['UPLOAD_EXTENSIONS'] = ['.wav']


#Blueprints import
from model_controller.model_controller import model_controller_blueprint 

#Blueprints Routes
app.register_blueprint(model_controller_blueprint)

@app.route('/')
def Index():
  return "Driver Mood Classifer"


if __name__ == '__main__':
    app.run()
 


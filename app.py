
from flask import Flask,jsonify,request
import joblib
import os
from flask.templating import render_template
import pandas as pd
from sklearn.base import BaseEstimator

app=Flask(__name__)
UPLOAD_FOLDER='static/files'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

class OutletTypeEncoder(BaseEstimator):
    def __init__(self):
        pass
    
    def fit(self,documents,y=None):
        return self
    
    def transform(self,x_dataset):
        x_dataset['outlet_grocery_store'] = (x_dataset['Outlet_Type'] == 'Grocery Store')*1
        x_dataset['outlet_supermarket_3'] = (x_dataset['Outlet_Type'] == 'Supermarket Type3')*1
        x_dataset['outlet_identifier_OUT027'] = (x_dataset['Outlet_Identifier'] == 'OUT027')*1
        return x_dataset

def load_model():
    loaded_model=joblib.load('salespredictionpipeline.joblib')
    print(type(loaded_model))
    return loaded_model

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    try:
        data=request.files['file']
        #data=request.form['dataframe']
        file_path=os.path.join(app.config['UPLOAD_FOLDER'],data.filename)
        data.save(file_path)
        #print(file_path)
        test_data=pd.read_csv(file_path)
        model=load_model()
        val=model.predict(test_data)
        return render_template('result.html',results=val)
    except:
        return "Error Occurred!!!!"

app.run(host='0.0.0.0')

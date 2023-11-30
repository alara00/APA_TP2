import pickle
import shelve
from flask import Flask, request, jsonify    
import numpy as np
import pandas as pd
app = Flask(__name__)
#%%
@app.route("/predict/<tv>", methods=['GET'])
def predictSales(tv):
    s = shelve.open("../Data/handson_model.db")
    model = s["model"]
    
    with open('./data/modelo_prueba.pkl', 'rb') as file: 
        model = pickle.load(file) 
    
    tv_df = pd.DataFrame(data = [tv], columns = ["TV"])
    prediction = model.predict(tv_df)
    # The return type must be a string, dict, tuple, Response instance, or WSGI callable
    result = {"Sales": prediction[0]}
    return result
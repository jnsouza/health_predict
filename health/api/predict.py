import os
import pickle
import pandas as pd
# from ml_logic.preprocess import preprocess_data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from joblib import load
import numpy as np
import xgboost

## script dir
script_dir = os.path.dirname(os.path.abspath(__file__))

## loading model
model_name     = "best_xgb_model.pkl"
model_path     = os.path.join(script_dir, "../data/model")
abs_model_path = os.path.abspath(model_path)
model_file     = os.path.join(model_path, model_name)
model          = pickle.load(open(model_file, 'rb'))

print("model loaded")
## API
app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# model = pickle.load(f)

#PRECISA ATUALIZAR COM O QUE VEM DO FRONT
@app.post("/predict")
def make_prediction(df: pd.DataFrame):

    #PRECISA FAZER O X_PRED COM O QUE VEM DO FRONT.


    ## prediction
    predict = model.predict(X_pred)
    proba   = model.predict_proba(X_pred)

    prediction = {'result': int(predict[0]), 'probability': proba.tolist()}

    return prediction


X_pred = pd.DataFrame([{
        'var_1': np.random.randint(1, 3),
        'var_2': np.random.randint(1, 3),
        'var_3': np.random.randint(1, 3),
        'var_4': np.random.randint(1, 3),
        'var_5': np.random.randint(1, 3),
        'var_6': np.random.randint(1, 3),
        'var_7': np.random.randint(1, 3),
        'var_8': np.random.randint(1, 3),
        'var_9': np.random.randint(1, 3),
        'var_10': np.random.randint(1, 3),
        'var_11': np.random.randint(1, 3),
        'var_12': np.random.randint(1, 3),
        'var_13': np.random.randint(1, 3),
        'var_14': np.random.randint(1, 3),
        'var_15': np.random.randint(1, 3),
        'var_16': np.random.randint(1, 3),
        'var_17': np.random.randint(1, 3),
        'var_18': np.random.randint(1, 3),
        'var_19': np.random.randint(1, 3),
        'var_20': np.random.randint(1, 3),
        'var_21': np.random.randint(1, 3),
        'var_22': np.random.randint(1, 3),
        'var_23': np.random.randint(1, 3),
        'var_24': np.random.randint(1, 3),
        'var_25': np.random.randint(1, 3),
        'var_26': np.random.randint(1, 3),
        'var_27': np.random.randint(1, 3),
        'var_28': np.random.randint(1, 3),
        'var_29': np.random.randint(1, 3),
        'var_30': np.random.randint(1, 3),
        'var_31': np.random.randint(1, 3),
        'var_32': np.random.randint(1, 3),
        'var_33': np.random.randint(1, 3),
        'var_34': np.random.randint(1, 3),
        'var_35': np.random.randint(1, 3),
        'var_36': np.random.randint(1, 3),
        'var_37': np.random.randint(1, 3),
        'var_38': np.random.randint(1, 3),
        'var_39': np.random.randint(1, 3),
        'var_40': np.random.randint(1, 3)
    }])

make_prediction(X_pred)

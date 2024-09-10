import os
import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

# Define a classe que representa o formato de entrada dos dados
class InputData(BaseModel):
    input_data: Dict[str, float]

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

@app.post("/predict")
def make_prediction(input_data: InputData):
    try:
        print("starting prediction")
        print(input_data, "esse é o input_data!!!!!!!!!!!!!")


        X_pred = pd.DataFrame([input_data.input_data])
        print(X_pred, "esse é o XPRED")

        ## prediction
        predict = model.predict(X_pred)
        proba   = model.predict_proba(X_pred)

        prediction = {'result': int(predict[0]), 'probability': proba.tolist()}

        print("prediction finished!")
        print()

        return prediction
    except Exception as e:
        print(f'Erro {e}!!!!!!!!!!!!!!!')




# variables = [
#     '_PACAT3', '_RFHYPE6', '_RFCHOL3', '_MICHD', '_LTASTH1', '_AGEG5YR',
#     '_DRDXAR2', 'HTM4', 'WTKG3', '_BMI5CAT', '_EDUCAG', '_INCOMG1',
#     '_PAINDX3', 'SEXVAR', 'PHYSHLTH', 'MENTHLTH', 'CHECKUP1',
#     'EXERANY2', 'EXRACT12', 'EXERHMM1', 'EXRACT22', 'CVDINFR4', 'CVDCRHD4',
#     'CVDSTRK3', 'CHCOCNC1', 'CHCCOPD3', 'ADDEPEV3', 'CHCKDNY2', 'DIABETE4',
#     'DECIDE', 'DIFFALON', '_PHYS14D', '_MENT14D', 'MAXVO21_', 'ACTIN13_',
#     'STRFREQ_', 'PA3MIN_'
# ]

# X_pred = pd.DataFrame([{var: np.random.randint(1, 3) for var in variables}])
# pred   = make_prediction(X_pred)
# print(pred)

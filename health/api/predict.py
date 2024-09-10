import os
import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))

## loading model
model_name     = "best_xgb_model.pkl"
model_path     = os.path.join(script_dir, "../data/model")
abs_model_path = os.path.abspath(model_path)
model_file     = os.path.join(model_path, model_name)
model          = pickle.load(open(model_file, 'rb'))
print("model loaded")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/predict")
async def make_prediction(input_data: dict):

    # Converta o input_data em um DataFrame
    X_pred = pd.DataFrame([input_data])

    # Faça a predição
    predict = model.predict(X_pred)
    proba = model.predict_proba(X_pred)

    model_in_pipeline = model.named_steps['classifier']
    importances = model_in_pipeline.feature_importances_
    print(importances, "IMPORTANCIAS!!!!!!!!")
    # feature_names = data.feature_names
# Ordenar as features pela importância
    # sorted_idx = np.argsort(importances)

    # Retorne os resultados
    return {"result": int(predict[0]), "probability": proba.tolist()}

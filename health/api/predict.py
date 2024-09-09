import pickle
import pandas as pd
from ml_logic.preprocess import preprocess_data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import joblib
# Carrega o modelo já treinado
#MODELO = JOBLIB.LOAD(caminhodomodelo)

app = FastAPI()
app.state.model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model_path = 'data/models/meu_modelo.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

#PRECISA ATUALIZAR COM O QUE VEM DO FRONT CERTINHO
def make_prediction(
        pickup_datetime: str,  # 2014-07-06 19:18:00
        pickup_longitude: float,    # -73.950655
        pickup_latitude: float,     # 40.783282
        dropoff_longitude: float,   # -73.984365
        dropoff_latitude: float,    # 40.769802
        passenger_count: int
    ):      # 1
    #PRECISA FAZER O X_PRED COM O QUE VEM DO FRONT.
    X_pred = pd.DataFrame(dict(
        pickup_datetime=[pd.Timestamp(pickup_datetime, tz='UTC')],
        pickup_longitude=[pickup_longitude],
        pickup_latitude=[pickup_latitude],
        dropoff_longitude=[dropoff_longitude],
        dropoff_latitude=[dropoff_latitude],
        passenger_count=[passenger_count],
    ))

    prediction = model.predict(X_pred)
    probability = model.predict_proba(X_pred)
    #PRECISA MONTAR O DICIONARIO DO RETORNO AQUI
    prediction = {'result':int(prediction), 'probability': 2}
    return prediction

#CARREGA A PIPELINE.

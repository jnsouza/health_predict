import pickle
import pandas as pd
from ml_logic.preprocess import preprocess_data

# Carrega o modelo já treinado
model_path = 'data/models/meu_modelo.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

def make_prediction(data: pd.DataFrame):
    # Aqui você faz o pré-processamento necessário nos dados
    processed_data = preprocess_data(data)

    # Faz a previsão
    prediction = model.predict(processed_data)

    return prediction

import os
import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

script_dir = os.path.dirname(os.path.abspath(__file__))

## loading model
model_name     = "best_xgb_model.pkl"
model_path     = os.path.join(script_dir, "../data/model")
abs_model_path = os.path.abspath(model_path)
model_file     = os.path.join(model_path, model_name)
model          = pickle.load(open(model_file, 'rb'))
print("model loaded")

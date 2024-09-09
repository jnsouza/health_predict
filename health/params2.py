import os
import numpy as np

##################  VARIABLES  ##################
# MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT  = "seventh-hallway-429514-c3"
# GCP_PROJECT_WAGON = os.environ.get("GCP_PROJECT_WAGON")
GCP_REGION   = "EU"
BQ_DATASET   = "LLCP2023"
BQ_REGION    = "EU"
BUCKET_NAME  = "lewagon_health"
# INSTANCE = os.environ.get("INSTANCE")
# MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
# MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT")
# MLFLOW_MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME")
# PREFECT_FLOW_NAME = os.environ.get("PREFECT_FLOW_NAME")
# PREFECT_LOG_LEVEL = os.environ.get("PREFECT_LOG_LEVEL")
# EVALUATION_START_DATE = os.environ.get("EVALUATION_START_DATE")
# GAR_IMAGE = os.environ.get("GAR_IMAGE")
# GAR_MEMORY = os.environ.get("GAR_MEMORY")

##################  CONSTANTS  #####################
LOCAL_DATA_PATH     = os.path.join(os.getcwd(), "data")
# LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "mlops", "training_outputs")


COLUMN_NAMES_RAW = ["_PACAT3", "_RFHYPE6", "_RFCHOL3", "_MICHD", "_LTASTH1",
                    "_AGEG5YR", "_DRDXAR2", "HTM4", "WTKG3", "_BMI5CAT",
                    "_EDUCAG", "_INCOMG1", "_PAINDX3", "SEXVAR", "GENHLTH",
                    "PHYSHLTH", "MENTHLTH", "CHECKUP1", "EXERANY2", "EXRACT12",
                    "EXERHMM1", "EXRACT22", "CVDINFR4", "CVDCRHD4", "CVDSTRK3",
                    "CHCOCNC1", "CHCCOPD3", "ADDEPEV3", "CHCKDNY2", "DIABETE4",
                    "DECIDE", "DIFFALON", "_PHYS14D", "_MENT14D", "MAXVO21_",
                    "ACTIN13_", "STRFREQ_", "PA3MIN_"]
# DTYPES_RAW = {
#     "fare_amount":       "float32",
#     "pickup_datetime":   "datetime64[ns, UTC]",
#     "pickup_longitude":  "float32",
#     "pickup_latitude":   "float32",
#     "dropoff_longitude": "float32",
#     "dropoff_latitude":  "float32",
#     "passenger_count":   "int16"
# }

DTYPES_PROCESSED = np.float32



################## VALIDATIONS #################

# env_valid_options = dict(
#     DATA_SIZE=["1k", "200k", "all"],
#     MODEL_TARGET=["local", "gcs", "mlflow"],
# )

# def validate_env_value(env, valid_options):
#     env_value = os.environ[env]
#     if env_value not in valid_options:
#         raise NameError(f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}")


# for env, valid_options in env_valid_options.items():
#     validate_env_value(env, valid_options)

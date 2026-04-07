import os

# Config file
CONFIG_PATH = "config/config.yaml"

# Data Ingestion Configurations
RAW_DIR             = "artifacts/raw_data"
RAW_FILE_PATH       = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH     = os.path.join(RAW_DIR, "train.csv")       # raw train
TEST_FILE_PATH      = os.path.join(RAW_DIR, "test.csv")        # raw test

# Data Processing Configurations
PROCESSED_DIR             = "artifacts/processed_data"
PROCESSED_FILE_PATH       = os.path.join(PROCESSED_DIR, "processed_data.csv")
PROCESSED_TRAIN_FILE_PATH = os.path.join(PROCESSED_DIR, "processed_data_train.csv")
PROCESSED_TEST_FILE_PATH  = os.path.join(PROCESSED_DIR, "processed_data_test.csv")

# Model Training Configurations
MODEL_DIR             = "artifacts/model/lgbm_model.pkl"
MODEL_OUTPUT_PATH    = os.path.join(MODEL_DIR, "lgbm_model.pkl")


from src.data_ingestion import DataIngestion
from src.data_pre_processing import DataProcessing
from src.model_training import model_training
from utils.common_functions import read_yaml_file
from config.paths_config import *


if __name__ == "__main__":
    from src.model_training import model_training

    # 1 Data Ingestion
    data_ingestion = DataIngestion(read_yaml_file(CONFIG_PATH))
    data_ingestion.run()

    # 2 Data Preprocessing
    preprocessor = DataProcessing(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    preprocessor.process()

    # 3 Model Training
    model = model_training(
        PROCESSED_TRAIN_FILE_PATH,
        PROCESSED_TEST_FILE_PATH,
        MODEL_OUTPUT_PATH
    )
    model.run()
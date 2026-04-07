import os
import sys
import pandas as pd
from src.logger import getLogger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml_file
from config.paths_config import *
from google.cloud import storage
from sklearn.model_selection import train_test_split

logger = getLogger(__name__)

class DataIngestion:

    def __init__(self, config):
        logger.info("Initializing DataIngestion class with provided configuration")
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]
        self.test_ratio = self.config["test_ratio"]

        # creating a raw folder in artifact directory to store the raw data
        self.raw_data_dir = RAW_DIR
        os.makedirs(self.raw_data_dir, exist_ok=True)
        logger.info(f"Raw data directory created at: {self.raw_data_dir}")
        logger.info(f"DataIngestion started with GCP Bucket {self.bucket_name} and GCP Bucket File Name {self.bucket_file_name}")

    # downloading the data from google cloud storage
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"File downloaded from GCP bucket {self.bucket_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Failed to download file from GCP: {e}")
            raise CustomException(e, sys)  # Fix 2: added sys

    # splitting the data into train and test
    def split_data(self):
        logger.info("Starting data splitting into train and test sets")
        try:
            data = pd.read_csv(RAW_FILE_PATH)
            train_df, test_df = train_test_split(data, test_size=self.test_ratio, random_state=42)
            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Data successfully split into train and test sets with ratio {self.train_ratio}:{self.test_ratio}")
        except Exception as e:
            logger.error(f"Failed to split data: {e}")
            raise CustomException(e, sys)

    def run(self):
        try:
            logger.info("Data Ingestion process started")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data Ingestion process completed successfully")
        except Exception as e:
            logger.error(f"Failed to run data ingestion process: {e}")
            raise CustomException(e, sys)
        finally:
            logger.info("Data Ingestion process ended")


if __name__ == "__main__":
    try:
        config = read_yaml_file(CONFIG_PATH)  # Fix 4: call function separately
        data_ingestion = DataIngestion(config)
        data_ingestion.run()
    except Exception as e:
        logger.error(f"Data Ingestion failed: {e}")
import sys
import yaml
import pandas
from src.logger import getLogger
from src.custom_exception import CustomException

logger = getLogger(__name__)

def read_yaml_file(path):
    try:
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"YAML file loaded successfully from: {path}")
            return config
    except FileNotFoundError:
        logger.error(f"YAML file not found at given path: {path}")
        raise CustomException(f"YAML file not found at given path: {path}", sys)  # ✅ sys
    except Exception as e:
        logger.error(f"Failed to read the yaml file: {e}")
        raise CustomException(f"Failed to read yaml file: {e}", sys)              # ✅ sys

def load_data(path):
    try:
        data = pandas.read_csv(path)
        logger.info(f"Data loaded successfully from: {path}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found at path: {path}")
        raise CustomException(f"File not found at path: {path}", sys)             # ✅ sys
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise CustomException(f"Failed to load data: {e}", sys)                   # ✅ sys
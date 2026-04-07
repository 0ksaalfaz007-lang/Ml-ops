from src.custom_exception import CustomException
from src.logger import getLogger
import sys


logger = getLogger(__name__)

def divide(a, b):
    try:
        result = a / b
        return result
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise CustomException("Error in division operation", sys)

if __name__ == "__main__":
    try:
        logger.info("Starting division operation")
        result = divide(10, 0)
        logger.info(f"Result: {result}")
    except CustomException as ce:
        logger.error(f"CustomException caught: {ce}")
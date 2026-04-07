import os
import sys
import pandas as pd
from src.logger import getLogger
from src.custom_exception import CustomException
import numpy as np
from utils.common_functions import read_yaml_file, load_data
from config.paths_config import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = getLogger(__name__)

class DataProcessing:

    def __init__(self, train_path, test_path, processed_data_dir, config_path):
        logger.info("Initializing DataProcessing class")
        self.train_path = train_path
        self.test_path = test_path
        self.processed_data_dir = processed_data_dir
        # reading config file from given path
        self.config = read_yaml_file(config_path)
        # creating a processed data directory to store the processed data
        if not os.path.exists(self.processed_data_dir):
            os.makedirs(self.processed_data_dir)
            logger.info(f"Processed data directory created at: {self.processed_data_dir}")

    def pre_process_data(self, df):
        try:
            logger.info("Starting data preprocessing")
            logger.info("Dropping the column Booking_ID")
            df.drop(columns=['Booking_ID'], inplace=True)
            logger.info("Dropping duplicate values")
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_preprocessing']['categorical_columns']
            num_cols = self.config['data_preprocessing']['numerical_columns']

            logger.info("Applying Label Encoding to categorical columns")
            label_encoder = LabelEncoder()
            mappings = {}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

            logger.info(f"Label encoding mapping: {mappings}")
            for col, mapping in mappings.items():
                logger.info(f"Column: {col}, Mapping: {mapping}")

            logger.info("Doing Skewness Handling")
            skewness_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])
                logger.info(f"Applied log transformation to {column} due to skewness of {skewness[column]}")

            return df

        except Exception as e:
            logger.error(f"Error in data preprocessing: {e}")
            raise CustomException("Error While Pre-processing step", sys)  # Fix 1: sys instead of e

    # data returned from pre_process_data function is imbalanced, so we need to balance using SMOTE
    def balance_data(self, df):
        try:
            logger.info("Handling imbalanced data using SMOTE")
            x = df.drop(columns=['booking_status'])
            y = df['booking_status']
            smote = SMOTE(random_state=42)
            x_resampled, y_resampled = smote.fit_resample(x, y)

            balance_df = pd.DataFrame(x_resampled, columns=x.columns)
            balance_df['booking_status'] = y_resampled
            logger.info(f"Data balanced using SMOTE. Class distribution after balancing: {balance_df['booking_status'].value_counts()}")
            return balance_df

        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise CustomException("Error While balancing data using SMOTE", sys)  # Fix 1: sys instead of e

    # feature selection step using RandomForest feature importances
    def select_features(self, df):
        try:
            logger.info("Starting feature selection")
            x = df.drop(columns=['booking_status'])
            y = df['booking_status']
            model = RandomForestClassifier(random_state=42)
            model.fit(x, y)

            feature_importances = pd.Series(model.feature_importances_, index=x.columns)
            feature_importance_df = pd.DataFrame({
                'feature': feature_importances.index,
                'importance': feature_importances.values
            })

            top_feature_importances_df = feature_importance_df.sort_values(by='importance', ascending=False)
            num_features_to_select = self.config["data_processing"]["no_of_features_to_select"]

            # Fix 2: top_10_features is already a list — removed wrong .to_list() call
            top_10_features = top_feature_importances_df["feature"].head(num_features_to_select).tolist()
            logger.info(f"Top {num_features_to_select} important features: {top_10_features}")

            # Fix 2: top_10_features is a list already — no .to_list() needed
            top_10_df = df[top_10_features + ['booking_status']]
            logger.info("Feature selection completed")
            return top_10_df

        except Exception as e:
            logger.error(f"Error in feature selection: {e}")
            raise CustomException("Error While Feature Selection", sys)  # Fix 1: sys instead of e

    def save_data(self, df, file_name):
        try:
            file_path = os.path.join(self.processed_data_dir, file_name)
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved successfully at: {file_path}")
        except Exception as e:
            logger.error(f"Error in saving data: {e}")
            raise CustomException("Error While Saving Data", sys)  # Fix 1: sys instead of e

    def process(self):
        try:
            logger.info("Loading data from RAW Directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            logger.info("Preprocessing training data")
            preprocessed_train_df = self.pre_process_data(train_df)

            logger.info("Preprocessing testing data")
            preprocessed_test_df = self.pre_process_data(test_df)

            # Fix 3: SMOTE only on train data — NEVER on test data
            logger.info("Balancing training data using SMOTE")
            balanced_train_df = self.balance_data(preprocessed_train_df)

            # Fix 3: test data skips SMOTE — use preprocessed directly
            logger.info("Skipping SMOTE for test data — using preprocessed test data directly")

            logger.info("Feature selection on training data")
            feature_engineered_train_df = self.select_features(balanced_train_df)

            logger.info("Feature selection on testing data")
            feature_engineered_test_df = self.select_features(preprocessed_test_df)  # Fix 3: preprocessed_test_df not balanced

            logger.info("Saving processed training data")
            self.save_data(feature_engineered_train_df, "processed_data_train.csv")

            logger.info("Saving processed testing data")
            self.save_data(feature_engineered_test_df, "processed_data_test.csv")

        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException("Error While Data Processing", sys)  # Fix 1: sys instead of e


if __name__ == "__main__":
    preprocessor = DataProcessing(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    preprocessor.process()
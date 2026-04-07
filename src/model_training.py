import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score

from config.paths_config import PROCESSED_TRAIN_FILE_PATH, PROCESSED_TEST_FILE_PATH, MODEL_OUTPUT_PATH
from config.model_params import LIGHT_PARAMS, RANDOM_SEARCH_PARAMS
from src.logger import getLogger
from src.custom_exception import CustomException
from utils.common_functions import load_data

import mlflow
import mlflow.lightgbm  # ✅ FIXED

logger = getLogger(__name__)


class model_training:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.param_dist = LIGHT_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading training data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading testing data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']

            return X_train, y_train, X_test, y_test

        except Exception as e:
            raise CustomException("Failed to load data", e)

    def train_lgbm_model(self, X_Train, y_Train):
        try:
            logger.info("Starting LightGBM training with RandomizedSearchCV")

            lgbm = lgb.LGBMClassifier(
                random_state=self.random_search_params['random_state']
            )

            random_search = RandomizedSearchCV(
                estimator=lgbm,
                param_distributions=self.param_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                n_jobs=self.random_search_params['n_jobs']
            )

            random_search.fit(X_Train, y_Train)

            best_model = random_search.best_estimator_
            best_params = random_search.best_params_

            logger.info(f"Best Params: {best_params}")

            return best_model, best_params

        except Exception as e:
            raise CustomException("Failed to train model", e)

    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating model")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            metrics = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }

            logger.info(f"Metrics: {metrics}")
            return metrics

        except Exception as e:
            raise CustomException("Failed to evaluate model", e)

    def save_model(self, model):
        try:
            logger.info(f"Saving model to {self.model_output_path}")

            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            joblib.dump(model, self.model_output_path)

            logger.info("Model saved successfully")

        except Exception as e:
            raise CustomException("Failed to save model", e)

    def run(self):
        try:
            # ✅ Optional but recommended
            #mlflow.set_tracking_uri("http://127.0.0.1:5000")

            mlflow.set_experiment("LightGBM_Experiment V2")

            with mlflow.start_run(run_name="LightGBM_Model_Training"):

                logger.info("Starting model training pipeline")

                X_train, y_train, X_test, y_test = self.load_and_split_data()

                best_model, best_params = self.train_lgbm_model(X_train, y_train)

                metrics = self.evaluate_model(best_model, X_test, y_test)

                self.save_model(best_model)

                # ✅ Log dataset
                mlflow.log_artifact(self.train_path, artifact_path="datasets")

                # ✅ Log BEST params (FIXED)
                mlflow.log_params(best_params)

                # ✅ Log metrics
                mlflow.log_metrics(metrics)

                # 🔥 MOST IMPORTANT FIX (MODEL LOGGING)
                mlflow.lightgbm.log_model(best_model, "model")

                logger.info("Model logged to MLflow successfully")
                logger.info(f"Final Metrics: {metrics}")

        except Exception as e:
            raise CustomException("Pipeline failed", e)


if __name__ == "__main__":
    model = model_training(
        PROCESSED_TRAIN_FILE_PATH,
        PROCESSED_TEST_FILE_PATH,
        MODEL_OUTPUT_PATH
    )
    model.run()
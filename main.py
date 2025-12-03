from Network_Security.Components.data_ingestion import DataIngestion
from Network_Security.Components.data_validation import DataValidation
from Network_Security.Components.data_transformation import DataTransformation
from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging
from Network_Security.Components.model_trainer import ModelTrainer
from Network_Security.Entity.config_entity import ModelTrainerConfig
from Network_Security.Entity.config_entity import TrainingPipelineConfig

from Network_Security.Entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
)


import sys

if __name__ == "__main__":
    try:
        # -----------------------------------------------------------
        # 1. Initialize the overall training pipeline configuration
        # -----------------------------------------------------------
        trainingpipelineconfig = TrainingPipelineConfig()

        # -----------------------------------------------------------
        # 2. DATA INGESTION
        #    - Reads raw data
        #    - Splits into train/test
        #    - Saves ingested files
        # -----------------------------------------------------------
        logging.info("Initializing Data Ingestion...")

        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config)

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        logging.info("Data Ingestion Completed.")
        print(data_ingestion_artifact)

        # -----------------------------------------------------------
        # 3. DATA VALIDATION
        #    - Checks schema
        #    - Validates column structure
        #    - Validates missing values, data drift, etc.
        #    - Outputs valid train/test file paths
        # -----------------------------------------------------------
        logging.info("Initializing Data Validation...")

        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(
            data_ingestion_artifact, data_validation_config  # input: ingestion results
        )

        data_validation_artifact = data_validation.initiate_data_validation()

        logging.info("Data Validation Completed.")
        print(data_validation_artifact)

        # -----------------------------------------------------------
        # 4. DATA TRANSFORMATION
        #    - Reads validated train/test CSV
        #    - Applies preprocessing (KNN imputation)
        #    - Produces transformed numpy arrays
        #    - Saves fitted preprocessor object + transformed data
        # -----------------------------------------------------------
        logging.info("Initializing Data Transformation...")

        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)

        data_transformation = DataTransformation(
            data_validation_artifact,
            data_transformation_config,
        )

        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        logging.info("Data Transformation Completed.")
        print(data_transformation_artifact)

        logging.info("Model Training Started")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact,
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

import os,sys

from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

from network_security.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValdiationConfig,
    ModelTrainerConfig
)

from network_security.constants import training_pipeline
from network_security.logging.logger import logging
from network_security.exception.CustomException import NetworkSecurityException

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_transformation import DataTransformation
from network_security.components.data_validation import Datavalidation
from network_security.components.model_trainer import ModelTrainer
from network_security.pipelines import TRAINING_BUCKET_NAME
from network_security.cloud.s3_syncer import s3sync

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.sync_obj = s3sync()
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(trainingpipelineconfig=self.training_pipeline_config)
            logging.info("Start data Ingestion")
            data_ingestion=DataIngestion(dataIngestionConfig=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = DataValdiationConfig(trainigpipelineconfig=self.training_pipeline_config)
            logging.info("Start Data Validation")
            data_validtion = Datavalidation(data_validation_config=self.data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validtion.initiate_data_validation()
            logging.info(f"Data Validation is completed and artifact :{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config = self.training_pipeline_config)
            logging.info("Start Data Transformation")
            data_transformation = DataTransformation(data_transformation_config= self.data_transformation_config, data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation is completed and artifact :{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Model trainer")
            model_trainer = ModelTrainer(modeltrainerconfig=self.model_trainer_config, datatransformationartifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model trainer is completed and artifact : {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.sync_obj.sync_folder_to_s3(self.training_pipeline_config.artifact_dir, aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.sync_obj.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
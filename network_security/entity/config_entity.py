from datetime import datetime
from network_security.constants import training_pipeline
import os

class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%d/%m/%Y")
        self.artifact_dir = os.path.join(training_pipeline.ARTIFACT_DIR)
        self.train_path = training_pipeline.TRAIN_FILE_NAME
        self.test_path = training_pipeline.TEST_FILE_NAME
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self, trainingpipelineconfig):
        self.data_ingestion_config_dir = os.path.join(
            trainingpipelineconfig.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_config_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE, training_pipeline.FILE_NAME
            )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_config_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_config_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
            )
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME

class DataValdiationConfig:
    def __init__(self, trainigpipelineconfig: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(trainigpipelineconfig.artifact_dir, training_pipeline.DATA_VALIDATION_DIR)
        self.data_validation_valid_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.data_validation_invalid_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.data_valid_train_file_path = os.path.join(self.data_validation_valid_dir, training_pipeline.TRAIN_FILE_NAME)
        self.data_valid_test_file_path = os.path.join(self.data_validation_valid_dir, training_pipeline.TEST_FILE_NAME)
        self.data_invalid_train_file_path = os.path.join(self.data_validation_invalid_dir, training_pipeline.TRAIN_FILE_NAME)
        self.data_invalid_test_file_path = os.path.join(self.data_validation_invalid_dir, training_pipeline.TEST_FILE_NAME)
        self.data_validation_drift_report_path = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )

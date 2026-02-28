from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.exception.CustomException import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataValdiationConfig
from network_security.components.data_validation import Datavalidation
import sys

if __name__ == "__main__":
    try:
        trainpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        datavalidationconfig = DataValdiationConfig(trainpipelineconfig)
        datavalidation = Datavalidation(dataingestionartifact, datavalidationconfig)
        logging.info("Initiate the data validation")
        datavalidationartifact = datavalidation.initiate_data_validation()
        logging.info("Data validation is completed")
        print(datavalidationartifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
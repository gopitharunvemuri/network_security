import pandas as pd
from sklearn.model_selection import train_test_split
from network_security.logging.logger import logging
from network_security.exception.CustomException import NetworkSecurityException
from network_security.entity.config_entity import DataIngestionConfig
import os
from dotenv import load_dotenv
import pymongo
import numpy as np
from network_security.entity.artifact_entity import DataIngestionArtifact
import sys

load_dotenv()
url = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,dataIngestionConfig:DataIngestionConfig):
        self.dataingestionconfig = dataIngestionConfig

    def convert_collection_to_csv(self):
        try:
            database_name = self.dataingestionconfig.database_name
            collection_name = self.dataingestionconfig.collection_name
            self.client = pymongo.MongoClient(url)

            collection = self.client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.tolist():
                df = df.drop(columns=["_id"])

            df.replace({"na":np.nan}, inplace = True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self, df:pd.DataFrame):
        try:
            self.feature_store_dir = self.dataingestionconfig.feature_store_file_path
            dir_name = os.path.dirname(self.feature_store_dir)
            os.makedirs(dir_name, exist_ok=True)
            df.to_csv(self.feature_store_dir, index = False, header=True)

            return df
        except Exception as e:
            raise NetworkSecurityException
        
    def split_data_as_train_test(self, df:pd.DataFrame):
        try:
            train_path = self.dataingestionconfig.training_file_path
            test_path = self.dataingestionconfig.testing_file_path
            train_set, test_set = train_test_split(
                df, test_size=self.dataingestionconfig.train_test_split_ratio
            )

            logging.info("The data has divided into train and test")
            logging.info("The data is saving in respective folders")
            dir_path = os.path.dirname(self.dataingestionconfig.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_set.to_csv(train_path, index = False, header = True)
            test_set.to_csv(test_path, index = False, header = True)

            logging.info("The data has been saved to respective paths")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.convert_collection_to_csv()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(trained_file_path=self.dataingestionconfig.training_file_path, tested_file_path=self.dataingestionconfig.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
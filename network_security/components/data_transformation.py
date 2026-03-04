import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception.CustomException import NetworkSecurityException 
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, 
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_transformer_object(self):
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            preprocessor: Pipeline = Pipeline([("imputer", imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self):
            # load the input files
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## training DataFrame
            input_feature_train = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train = train_df[TARGET_COLUMN]
            target_feature_train = target_feature_train.replace(-1, 0)

            ## testing DataFrame
            input_feature_test = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test = test_df[TARGET_COLUMN]
            target_feature_test = target_feature_test.replace(-1, 0)

            preprocessor = self.get_transformer_object()
            logging.info("fit on the train and test data")
            preprocessing_obj = preprocessor.fit(input_feature_train)
            input_feature_train = preprocessing_obj.transform(input_feature_train)
            input_feature_test = preprocessing_obj.transform(input_feature_test)

            train_arr = np.c_[input_feature_train, np.array(target_feature_train)]
            test_arr = np.c_[input_feature_test, np.array(target_feature_test)]
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessing_obj)

            save_object( "final_model/preprocessor.pkl", preprocessing_obj)
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

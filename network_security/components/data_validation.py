from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataValdiationConfig
from network_security.exception.CustomException import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
import os, sys
import pandas as pd
from scipy.stats import ks_2samp
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file

class Datavalidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValdiationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path:str)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe:pd.DataFrame)-> bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                number_of_numerical_columns = len(self._schema_config['numerical_columns'])
                numerical_in_dataframe = len([i for i in dataframe.columns if dataframe[i].dtype == "int64"])
                logging.info(f"Required number of numerical columns:{number_of_numerical_columns}")
                logging.info(f"Data frame has numerical columns:{numerical_in_dataframe}")
                if numerical_in_dataframe == numerical_in_dataframe:
                    return True
                return False
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for columns in base_df.columns:
                d1 = base_df[columns]
                d2 = current_df[columns]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    columns : {
                        "p_value" : float(is_same_dist.pvalue),
                        "drift_status" : is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.data_validation_drift_report_path

            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)

            write_yaml_file(drift_report_file_path, report)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
            

    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            trained_file_path = self.data_ingestion_artifact.trained_file_path
            tested_file_path = self.data_ingestion_artifact.tested_file_path

            # load the data as dataframe
            trained_dataframe = Datavalidation.read_data(trained_file_path)
            tested_dataframe = Datavalidation.read_data(tested_file_path)

            ## validate number of columns

            status = self.validate_number_of_columns(dataframe = trained_dataframe)
            if not status:
                error_message = "failed at validate_number_of_columns"
                raise NetworkSecurityException(error_message, sys)
            status = self.validate_number_of_columns(dataframe = tested_dataframe)
            if not status:
                error_message = "failed at validate_number_of_columns"
                raise NetworkSecurityException(error_message, sys)
            
            
            ## Detect data drift
            status = self.detect_dataset_drift(trained_dataframe, tested_dataframe)

            dir_path=os.path.dirname(self.data_validation_config.data_valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            trained_dataframe.to_csv(
                self.data_validation_config.data_valid_train_file_path, index=False, header=True

            )

            tested_dataframe.to_csv(
                self.data_validation_config.data_valid_test_file_path, index=False, header=True
            )
            data_validation_artifact = DataValidationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                    valid_test_file_path=self.data_ingestion_artifact.tested_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.data_validation_drift_report_path,
                )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
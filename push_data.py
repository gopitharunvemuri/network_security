import sys
import os
import pandas as pd
import numpy as np
import json

from dotenv import load_dotenv
import pymongo
from network_security.exception.CustomException import NetworkSecurityException
from network_security.logging.logger import logging
load_dotenv()
url = os.getenv("MONGO_DB_URL")
logging.info(f"{url}")

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e)
        
    def cv_to_json_converter(self, filepath):
        df = pd.read_csv(filepath)
        df.reset_index(drop=True, inplace=True)
        h = list(json.loads(df.T.to_json()).values())
        return h
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(url)
            self.database = self.mongo_client[self.database]
            print(self.database)
            
            self.collection=self.database[self.collection]
            print(self.collection)
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
if __name__ == "__main__":
    obj = NetworkDataExtract()
    filepath = "Network_data\phisingData.csv"
    dbname = "gopi"
    collection = "network_security"
    records = obj.cv_to_json_converter(filepath=filepath)
    length = obj.insert_data_mongodb(records=records, database=dbname, collection=collection)
    print(length)
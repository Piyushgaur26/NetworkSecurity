import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo

from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

ca = certifi.where()

from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            # Convert DataFrame to JSON string, then to Python object
            json_str = data.to_json(orient="records")  # list of dicts
            records = json.loads(json_str)
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def inser_data_mongodb(self, records, database, collections):
        try:
            self.database = database
            self.records = records
            self.collections = collections
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collections = self.database[self.collections]
            self.collections.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise (NetworkSecurityException(e, sys))
            raise (NetworkSecurityException(e, sys))


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "PiyushAi"
    COLLECTION = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.inser_data_mongodb(records, DATABASE, COLLECTION)
    print(no_of_records)

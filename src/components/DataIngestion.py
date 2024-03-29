import os, sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exception import CustomException
from src.utils import import_data_as_Dataframe
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join('artifacts','raw_data.csv')
    train_data_path = os.path.join('artifacts','train_data.csv')
    test_data_path = os.path.join('artifacts','test_data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_ingestion(self):
        try:
            logging.info('Data ingestion Starts')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df = import_data_as_Dataframe(database='database',collection='PhishingDomainDetection')

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            train_data,test_data=train_test_split(df,test_size=0.33,random_state=42)
            train_data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Data ingestion Completed')

            return self.ingestion_config.raw_data_path
        
        except Exception as e:
            logging.info('Error occurred in Data Ingestion')
            raise CustomException(e,sys)
import os, sys
from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging
from Network_Security.Constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME


class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.prerocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        try:
            x_transform = self.prerocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e, sys)

from Network_Security.Pipeline.training_pipeline import TrainingPipeline
from Network_Security.Exception.exception import NetworkSecurityException
import sys

if __name__ == "__main__":
    try:
        TrainingPipeline().run_pipeline()
    except Exception as e:
        raise NetworkSecurityException(e, sys)

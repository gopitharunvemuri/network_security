import yaml
from network_security.exception.CustomException import NetworkSecurityException
import sys
def read_yaml_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path, report):
    try:
        with open(file_path, "wb") as f:
            return yaml.safe_dump(report)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
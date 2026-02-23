import sys
from network_security.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self, error, error_details:sys):
        self.error_msg = error
        _, _, exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        message = f"Error occured in the file {self.filename} on line number {self.lineno} with message {self.error_msg}"
        return message

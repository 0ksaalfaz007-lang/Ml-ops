import traceback
import sys


class CustomException(Exception):
    def __init__(self, message, error_detail: sys):
        super().__init__(message)
        self.error_message = self.get_detailed_error_message(error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_detail: sys) -> str:
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = str(error_detail.exc_info()[1])
        detailed_message = f"Error occurred in file: {file_name} at line: {line_number} with message: {error_message}"
        return detailed_message

    def __str__(self):
        return self.error_message
import sys
import traceback
from typing import Optional


class NetworkSecurityException(Exception):
    def __init__(self, message: str, original_exception: Optional[Exception] = None):

        self.original_exception = original_exception

        # Extract traceback safely
        tb = original_exception.__traceback__ if original_exception else None
        if tb:
            self.lineno = tb.tb_lineno
            self.file_name = tb.tb_frame.f_code.co_filename
        else:
            self.lineno = None
            self.file_name = None

    def __str__(self):
        location = ""
        if self.file_name and self.lineno:
            location = f" Error Occured in [{self.file_name}] at line [{self.lineno}]"

        base = super().__str__()
        return f"{base}{location}"

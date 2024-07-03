#!/usr/bin/env python3
"""
filtered_logger module
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specified fields in a log message.
    
    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): String to replace field values.
        message (str): Log message string.
        separator (str): Character separating fields in the message.
    
    Returns:
        str: The log message with specified fields obfuscated.
    """
    pattern = '|'.join([f'{field}=[^{separator}]+' for field in fields])
    return re.sub(pattern, lambda m: f'{m.group(0).split("=")[0]}={redaction}', message)

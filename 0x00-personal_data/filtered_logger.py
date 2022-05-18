#!/usr/bin/env python3
"""function called filter_datum that returns the log message obfuscated"""
import re


def filter_datum(fields, redaction, message, separator):
    """function should use a regex to replace occurrences of certain field
    values"""
    for i in fields:
        message = re.sub(i + "=.*?" + separator, i + "=" + redaction +
                         separator, message)
    return(message)

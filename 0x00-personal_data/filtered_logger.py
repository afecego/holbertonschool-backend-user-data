#!/usr/bin/env python3
"""function called filter_datum that returns the log message obfuscated"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """function should use a regex to replace occurrences of certain field
    values"""
    new_mess = message
    for i in fields:
        new_mess = re.sub(i + "=.*?" + separator, i + "=" + redaction +
                          separator, new_mess)
    return new_mess

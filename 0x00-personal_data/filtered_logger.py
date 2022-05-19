#!/usr/bin/env python3
"""function called filter_datum that returns the log message obfuscated"""
import re
import logging


PII_FIELDS = ('name', 'email', 'phone', 'sn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """function constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """method to filter values in incoming record using filter_datum"""
        resum = filter_datum(self.fields, self.REDACTION,
                             super(RedactingFormatter, self).format(record),
                             self.SEPARATOR)
        return resum


def filter_datum(fields, redaction, message, separator):
    """function should use a regex to replace occurrences of certain field
    values"""
    for i in fields:
        message = re.sub(i + "=.*?" + separator, i + "=" + redaction +
                         separator, message)
    return(message)


def get_logger() -> logging.Logger:
    """function that takes no arguments and returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(ch)
    return logger

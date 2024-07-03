#!/usr/bin/env python3
"""
filtered_logger module
"""

import re
import logging
import os
import mysql.connector
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
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
    return re.sub(pattern, lambda m: f'{m.group(0).split("=")[0]}={redaction}',
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record by redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record with sensitive fields redacted.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Get a MySQL database connection using credentials from environment
    variables.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """
    Main function that retrieves and displays all rows from the users table
    with filtered format.
    """
    fields = ["name", "email", "phone", "ssn", "password"]

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(RedactingFormatter(fields))
    logger.addHandler(ch)

    # Get database connection
    db = get_db()
    cursor = db.cursor()

    # Execute query to retrieve all rows from the users table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Define the format of the log message
    columns = ["name", "email", "phone", "ssn", "password", "ip",
               "last_login", "user_agent"]

    # Log each row
    for row in rows:
        log_message = '; '.join([f"{columns[i]}={row[i]}"
                                 for i in range(len(columns))]) + ';'
        logger.info(log_message)

    # Close cursor and database connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

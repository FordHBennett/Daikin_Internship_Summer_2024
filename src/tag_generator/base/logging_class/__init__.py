#!/usr/bin/env python

import logging
import os

# Define a custom logging level
NAME_CHANGE = 35
logging.addLevelName(NAME_CHANGE, "NAME_CHANGE")

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;21m"
    blue = "\x1b[34;21m"
    purple = "\x1b[35;21m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
        NAME_CHANGE: purple + format + reset 
    }

    def format(self, record):
            """
            Formats the log record using the specified log format.

            Args:
                record (logging.LogRecord): The log record to be formatted.

            Returns:
                str: The formatted log record.
            """
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
            return formatter.format(record)

class Logger:
    def __init__(self, log_file='', level='INFO', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'):
        """
        Initialize the LoggingClass object.

        Args:
            log_file (str): The path to the log file. If not provided, the logger name (__name__) will be used.
            level (str): The log level. Default is 'INFO'.
            format (str): The log message format. Default is '%(asctime)s - %(levelname)s - %(message)s'.
            datefmt (str): The log message date format. Default is '%Y-%m-%d %H:%M:%S'.
        """
        self.log_file = log_file
        self.logger = logging.getLogger(log_file if log_file else __name__) 
        self.logger.setLevel(level.upper())
        self.set_format()
        if log_file:
            self.set_file_handler(log_file, format, datefmt)

    def set_format(self):
            """
            Sets the format for the logging output.

            This method creates a console handler and sets a custom formatter for the logging output.

            Parameters:
                None

            Returns:
                None
            """
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(CustomFormatter())

    def set_file_handler(self, log_file, format, datefmt):
        """
        Sets up a file handler for logging.

        Args:
            log_file (str): The path to the log file.
            format (str): The format string for log messages.
            datefmt (str): The format string for log timestamps.

        Returns:
            None
        """

        if not os.path.exists(os.path.dirname(log_file)): os.makedirs(os.path.dirname(log_file))

        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(format, datefmt)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def log_message(self, message, level='INFO'):
        """
        Logs a message with the specified log level.

        Parameters:
            message (str): The message to be logged.
            level (str, optional): The log level. Defaults to 'INFO'.

        Returns:
            None
        """
        level = level.upper()
        log_level = level.upper()
        log_switch = {
            'DEBUG': self.logger.debug,
            'INFO': self.logger.info,
            'WARNING': self.logger.warning,
            'ERROR': self.logger.error,
            'CRITICAL': self.logger.critical,
            'NAME_CHANGE': lambda msg: self.logger.log(NAME_CHANGE, msg),
        }
        log_switch.get(log_level, self.logger.info)(message)
    
    def clear(self):
        """
        Clears the contents of the log file.

        If the log file exists, it will be opened and truncated to remove all its contents.
        """

        if os.path.exists(self.log_file):
            open(self.log_file, 'w').close()

    def change_log_file(self, log_file):
        """
        Changes the log file and updates the file handler.

        Args:
            log_file (str): The path to the new log file.

        Returns:
            None
        """
        # Close and remove all current handlers
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                self.logger.removeHandler(handler)
        self.log_file = log_file
        self.set_file_handler(log_file, '%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

    def set_level(self, level):
            """
            Set the logging level for the logger and all its handlers.

            Args:
                level (str): The desired logging level. It should be one of the following:
                             'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.

            Returns:
                None
            """
            self.logger.setLevel(level.upper())
            map(lambda handler: handler.setLevel(level.upper()), self.logger.handlers)

    def log_missing_key_critical(self, key) -> None:

        self.change_log_file(os.path.join('files','logs', 'mitsubishi', 'critical.log'))
        self.set_level('CRITICAL')
        self.log_message(f"Could not find {key}.json in ignition JSON so skipping it", 'CRITICAL')


    def handle_tag_not_found(self, tag_builder, key, os_path_join) -> None:

        self.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
        self.set_level('INFO')
        self.log_message(f"Could not find tag {tag_builder['kepware_tag_name']} in CSV file {key}.csv so just leaving it as is", 'INFO')

    def handle_opc_path_not_found(self, tag, device_name, os_path_join) -> None:

        self.change_log_file(os_path_join('files','logs', 'mitsubishi', 'info.log'))
        self.set_level('INFO')
        self.log_message(f"Could not find opcItemPath or dataType in tag {tag['name']} in the file {device_name}.json so just leaving it as is", 'INFO')

        

import logging

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
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

class Logger:
    def __init__(self, log_file: str, level: str = 'INFO', format: str = '%(asctime)s - %(levelname)s - %(message)s', datefmt: str = '%Y-%m-%d %H:%M:%S'):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.set_level(level)
        self.set_format(log_file, format, datefmt)

    def set_level(self, level: str):
        level = level.upper()
        if level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)
        elif level == 'NAME_CHANGE':
            self.logger.setLevel(NAME_CHANGE)
        else:
            self.logger.setLevel(logging.INFO)

    def set_format(self, log_file: str, format: str, datefmt: str):
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(format, datefmt)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomFormatter())
        self.logger.addHandler(console_handler)

    def log_message(self, message: str, level: str = 'INFO'):
        level = level.upper()
        if level == 'DEBUG':
            self.logger.debug(message)
        elif level == 'INFO':
            self.logger.info(message)
        elif level == 'WARNING':
            self.logger.warning(message)
        elif level == 'ERROR':
            self.logger.error(message)
        elif level == 'CRITICAL':
            self.logger.critical(message)
        elif level == 'NAME_CHANGE':
            self.logger.log(NAME_CHANGE, message)
        else:
            self.logger.info(message)
    
    def clear(self):
        open(self.log_file, 'w').close()

# Usage example
# logger = Logger(log_file='tag_generation.log', level='INFO')

# logger.log_message('This is an info message.', 'INFO')
# logger.log_message('This is a warning message.', 'WARNING')
# logger.log_message('This is an error message.', 'ERROR')
# logger.log_message('This is a debug message.', 'DEBUG')
# logger.log_message('This is a critical message.', 'CRITICAL')
# logger.log_message('This is a name change message.', 'NAME_CHANGE')

# # Clear the log file
# logger.clear()

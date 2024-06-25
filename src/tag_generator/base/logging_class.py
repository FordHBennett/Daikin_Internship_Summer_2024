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
    def __init__(self, log_file: str='', level: str = 'INFO', format: str = '%(asctime)s - %(levelname)s - %(message)s', datefmt: str = '%Y-%m-%d %H:%M:%S'):
        self.log_file = log_file
        self.logger = logging.getLogger(log_file if log_file else __name__) 
        self.logger.setLevel(level.upper())
        self.set_format()
        if log_file:
            self.set_file_handler(log_file, format, datefmt)

    def set_format(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomFormatter())
        self.logger.addHandler(console_handler)

    def set_file_handler(self, log_file: str, format: str, datefmt: str):
        from os.path import exists as os_path_exists
        from os import makedirs as os_makedirs
        from os.path import dirname as os_path_dirname

        if not os_path_exists(os_path_dirname(log_file)):
            os_makedirs(os_path_dirname(log_file))

        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(format, datefmt)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

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
        from os.path import exists as os_path_exists
        if os_path_exists(self.log_file):
            open(self.log_file, 'w').close()

    def change_log_file(self, log_file: str):
        # Close and remove all current handlers
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                self.logger.removeHandler(handler)
        self.log_file = log_file
        self.set_file_handler(log_file, '%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

    def set_level(self, level: str):
        self.logger.setLevel(level.upper())
        for handler in self.logger.handlers:
            handler.setLevel(level.upper())

        

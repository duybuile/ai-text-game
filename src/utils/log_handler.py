import logging
import os

log_level = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def setup_logger(filestream_logging: bool = False, filepath: str = "", level: str = "info"):
    """
    Setup a logger for both filestream and console. By default, the logger is set to console only.
    :param filestream_logging:
    :param filepath:
    :param level:
    :return:
    """
    if not filestream_logging or filepath == "":
        return setup_console_logger(level)
    else:
        if not os.path.isdir(filepath.split("/")[0]):  # If the directory does not exist, create it
            os.mkdir(filepath.split("/")[0])
        return setup_filestream_logger(filepath, level)


def setup_console_logger(level="info"):
    """
    Setup a console logger
    :param level:
    :return:
    """
    logger = logging.getLogger()

    # Set the logging level
    logger.setLevel(log_level[level.lower()])

    # Create a console handler and set its formatter
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)
    return logger


def setup_filestream_logger(file, level="info"):
    """
    Setup a file logger
    :param file: path of a file for logging
    :param level:
    :return:
    """
    logger = logging.getLogger()

    # Set the logging level
    logger.setLevel(log_level[level.lower()])

    # Create a file handler and set its formatter
    file_handler = logging.FileHandler(file, mode="a")  # 'a' for append mode
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

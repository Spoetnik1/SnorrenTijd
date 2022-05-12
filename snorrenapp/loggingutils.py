"""Example of using root logger with different formatters."""
import logging
import sys


def configure_logger(log_level, logging_filename):
    """setting logging"""
    log_level = log_level
    logging_format = f'%(asctime)s %(levelname)s %(message)s'
    root_logger = logging.getLogger('')
    # Capture warnings from external packages and log them as well
    logging.captureWarnings(True)
    # Default loggers
    file_handler = logging.FileHandler('./logs', 'a')
    root_logger.addHandler(file_handler)
    formatter = logging.Formatter(logging_format)
    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setFormatter(formatter)
    err_handler.setLevel('ERROR')
    root_logger.addHandler(err_handler)
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setFormatter(formatter)
    out_handler.setLevel('INFO')
    root_logger.addHandler(out_handler)
    root_logger.setLevel('INFO')
    root_logger.info(f'Log level set to {log_level}')
    root_logger.setLevel(log_level)
    
    
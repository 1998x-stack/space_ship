# logger.py
import logging

def setup_logger():
    logging.basicConfig(
        filename='space_ship.log',
        filemode='a',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logging.info("Logger initialized")

def log_event(event_message: str):
    logging.info(event_message)

def log_error(error_message: str):
    logging.error(error_message)
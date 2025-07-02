import logging
import os

def get_logger(name):

    logger=logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        os.makedirs('logs',exist_ok=True)

        file_handler=logging.FileHandler('logs/pipeline_logs.txt', mode='a')
        console_handler=logging.StreamHandler()

        formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

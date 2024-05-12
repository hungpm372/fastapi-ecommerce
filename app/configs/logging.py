import os
import logging

logs_dir = os.path.join(os.getcwd(), "logs")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, "app.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_logger():
    return logging.getLogger()

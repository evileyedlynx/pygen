import logging


logging.getLogger().setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logging.getLogger().addHandler(console_handler)
console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)


def logging_in_file(log_name: str):
    file_handler = logging.FileHandler(f'{log_name}.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)


def info(message):
    logging.info(message)


def error(message, exit_app=True):
    logging.error(message)
    if exit_app:
        exit(1)


def unknown_type(message, exit_app=True):
    logging.error('Unknown type when data ' + message)
    if exit_app:
        exit(1)


def warning(message):
    logging.warning(message)


def generate_data(name, data):
    logging.info(f'for {str(name)} generated {str(data)}')

import logging
import re
from datetime import datetime

from rich.logging import RichHandler
from tabulate import tabulate

from gitbrew.exceptions import InvalidRepositoryException


def print_table(data, headers, print_format="fancy_grid", show_index=False):
    """
    Prints a table using tabulate with print_format
    Headers are optional and can be passed as a list of the same length
    as the data

    :param show_index: show index
    :param data: List of lists or tuples
    :param headers: List of headers
    :param print_format: Format to print the table in
    :return: None
    """
    if isinstance(data, (tuple, list)):
        print(
            tabulate(data, headers=headers, tablefmt=print_format, showindex=show_index)
        )
    else:
        raise TypeError("Data must be a tuple or list")


def print_dictionary(data_dict, headers, print_format="fancy_grid"):
    """
    Prints a dictionary as a table using tabulate with print_format
    :param data_dict: Dictionary
    :param headers: List of headers
    :param print_format: Format to print the table in
    :return:
    """
    for k, v in data_dict.items():
        print(f"\n{k}")
        print_table(v, headers, print_format)


def extract_repo(url):
    """
    Extracts the repository string (typically acc/repo)
     from an url
    :param url: GitHub repo url
    :return: repository string as acc/repo
    """
    if match := re.search(r"github.com/([\w-]+)/([\w-]+)", url):
        if not match[1] or not match[2]:
            raise InvalidRepositoryException("Invalid repository url")
        return f"{match[1]}/{match[2]}"


def setup_logger(save_logs=False, print_logs=False):
    """
    Setup logger for the application with rich handler
    Logs are saved if save_logs is True to gitbrew_<timestamp>.log
    Logs are printed to console if print_logs is True

    :param save_logs: Save logs to a file
    :param print_logs: Print logs to console
    :return: Logger
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if print_logs:
        rich_handler = RichHandler(show_time=True, show_path=True, markup=True)
        rich_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(rich_handler)

    if save_logs:
        file_handler = logging.FileHandler(
            f"gitbrew_{datetime.now().strftime('%Y%m%d%H%M%S')}.log", mode="w"
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(funcName)s %(message)s")
        )
        logger.addHandler(file_handler)

    return logger

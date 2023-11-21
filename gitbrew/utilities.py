import re

from tabulate import tabulate


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
            raise ValueError("Invalid repository url")
        return f"{match[1]}/{match[2]}"

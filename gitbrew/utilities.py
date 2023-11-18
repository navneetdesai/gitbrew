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

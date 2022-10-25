import re


def get_column_indices(headers, target_headers):
    """
    Given a `headers` list from a data file, generate a list of tuples
    from a list of given `target_headers` to identify the index (i.e.,
    column location) of each targeted header in the headers list.

    :param headers: list - A list of strings representing the header row
        of a csv file.
    :param target_headers: list - A list of strings representing the
        columns to locate in a csv file.
    :return: list - A modification of the original `target_headers` list
    to include a column index with each header. A list of tuples, each
    containing a target_header (str) and its index (int). A column index
    of None means the target_header was not found in the `headers` list.

    Example return: [("DATE", 1), ("NAME", 0), ("AGE", None)]
    """
    target_headers_indexed = []
    for target_header in target_headers:
        try:
            column_index = headers.index(target_header)
        except ValueError:
            print(f"Data missing from file: {target_header}")
            target_headers_indexed.append((target_header, None))
        else:
            target_headers_indexed.append((target_header, column_index))
    return target_headers_indexed


def format_station_name(unformatted_name):
    """
    Nicely formats a name string extracted from NOAA weather station
    data.

    :param unformatted_name: str - An unformatted string taken from data
    file.
    :return: str - A nicely formatted string: Name, STATE
    """
    name_parsed = re.findall("([A-Z ]+), ([A-Z]+)", unformatted_name)[0]
    location = name_parsed[0].title()
    state = name_parsed[1]
    formatted_name = f"{location}, {state}"
    return formatted_name

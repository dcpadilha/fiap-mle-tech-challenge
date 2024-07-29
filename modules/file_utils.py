import csv
import os
from datetime import datetime

import requests

from modules.user_exceptions import FileHandlingError


def read_file(filename):
    # Extracts the required dimension from the filename
    # Splits the filename on the dash
    # Gets the index 1 and removes the .csv extension)
    if filename.endswith('.csv'):
        try:
            dimension = filename.split('-')[1][:-4]

        # Raises an exception in case the file does not meet the format requirement
        except IndexError:
            raise FileHandlingError(filename, message='Wrong file name format, should be: <date>-<dimennsion>.csv)')
    else:
        # Raises an exception due to missing the correct file extension
        raise FileHandlingError(filename, message='Wrong file extension')

    result_data = {dimension: []}

    # Defaults the delimiter to a semicolon
    delimiter = ';'

    full_path = f"{os.getenv('DOWNLOAD_FOLDER')}/{filename}"

    try:
        # Infer the proper delimiter used on the file
        with open(full_path, newline='', encoding='utf-8') as csvfile:
            delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)

        # Reopening file to avoid StopIteration() exception
        with open(full_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')

            # Reads the first line to determine the keys from the dictionary
            keys = next(csvreader)

            for values in csvreader:
                # Fills the list with the values gathered from each line
                result_data[dimension].append(dict(zip(keys, values)))

    except Exception as e:
        # Redirects the exception to the original function caller
        raise FileHandlingError(filename, message=repr(e))

    return result_data


def download_file(file_link: str):
    """
    Downloads the file specified on the file_link argument

    Args:
        file_link (str): A URL which points to a file
    Returns:
        str: The customized file name prefixed with the current date and time
    """

    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')

    # Extracting the file data from the returned contest of the GET request
    if not file_link.endswith('.csv'):
        return None

    try:
        file_data = requests.get(file_link).content
    except Exception as e:
        return repr(e)

    # Assigning the current date and time to the filename
    file_name = current_datetime + '-' + file_link.split('/')[-1]

    save_path = os.getenv('DOWNLOAD_FOLDER') + file_name
    try:
        with open(save_path, 'wb') as fp:
            fp.write(file_data)
    except Exception as e:
        return f'Error saving file "{file_name}":{repr(e)}'
    
    return file_name

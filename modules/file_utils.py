import csv
import os

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

import csv
import os


def read_file(filename):

    if not filename:
        filename = '20240615172009-Producao.csv'

    # Extracts the required dimension from the filename
    # Splits the filename on the dash
    # Gets the index 1 and removes the .csv extension)
    if filename.endswith('.csv'):
        try:
            dimension = filename.split('-')[1][:-4]
        # Raises an exception in case the file does not meet the format requirement
        except IndexError:
            return {'error': 'Wrong file name format, should be: <date>-<dimennsion>.csv)'}
    else:
        return {'error': 'Wrong file extension'}

    result_data = {dimension: []}

    full_path = f"{os.getenv('DOWNLOAD_FOLDER')}/{filename}"

    try:
        with open(full_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            keys = next(csvreader)
            for values in csvreader:
                result_data[dimension].append(dict(zip(keys, values)))
    except Exception as e:
        return {'error': repr(e)}

    return result_data

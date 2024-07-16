import os
from datetime import datetime

import requests


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

    file_data = requests.get(file_link).content

    # Assigning the current date and time to the filename
    file_name = current_datetime + '-' + file_link.split('/')[-1]

    save_path = os.getenv('DOWNLOAD_FOLDER') + file_name

    with open(save_path, 'wb') as fp:
        fp.write(file_data)

    return file_name

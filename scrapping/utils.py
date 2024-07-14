import re

def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0
    
def remove_space(value: str):
    return re.sub(r'^\s+|\s+$', '',value)

def transform_data_list(value: str):

    pattern = r'\[\s*(\d{4})\s*-\s*(\d{4})\s*\]'
    match = re.search(pattern, value)

    start_year = int(match.group(1))
    end_year = int(match.group(2))

    return list(range(start_year, (end_year + 1)))


# Custom Exception for CSV File Handling


class FileHandlingError(Exception):
    def __init__(self, filename, message='Exception found'):
        self.filename = filename
        self.message = message

        if filename is None:
            message = 'Filename is missing'
            super().__init__(message)

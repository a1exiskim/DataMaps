from pathlib import Path

class Source:
    """Represents an identified data source and its associated metadata.

    Stores the source type, available data formats, source location, and the
    files grouped by their format.
    """

    def __init__(self, source_type, formats, location, files_by_format):
        if isinstance(source_type, str):
            self.source_type = source_type  # i.e. file or database
        else:
            raise TypeError('source type must be string.')

        if isinstance(formats, set):
            self.formats = formats # i.e json, postgres, parquet, etc
        else: 
            raise TypeError('format type must be set')

        if isinstance(location, str):
            self.location = location  # i.e filesystem path, database identifer 
        else:
            raise TypeError('location must be string.')   

        if isinstance(files_by_format, dict):
            self.files_by_format = files_by_format
        else:
            raise TypeError('files and their formats should be in a dictionary') 


def identify_source(location):
    """
    Identifies a file-based data source from a given location.

    Determines whether the location is a file or directory, identifies the
    formats of the files found, and groups file paths by format.

    Args:
        location: Path to a file or directory containing data files.
    """
    
    files_by_format = {}

    path_location = Path(location)

    if path_location.is_file():
        file = path_location
        file_format = file.suffix[1:].lower()

        files_by_format.setdefault(file_format, []).append(str(file))

    elif path_location.is_dir():
        for file in path_location.iterdir():
            if file.is_file():
                file_format = file.suffix[1:].lower()

                files_by_format.setdefault(file_format, []).append(str(file))

    else:
        raise ValueError("location must point to a valid file or directory")

    formats = set(files_by_format.keys())

    if len(formats) == 0:
        raise ValueError("no file formats found")

    source = Source(
        "file",
        formats,
        location,
        files_by_format
    )

    return source





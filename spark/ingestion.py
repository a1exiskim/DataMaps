from pathlib import Path

class Source:
    def __init__(self, source_type, formats, location):
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


def identify_source(location):
    file_ext = set()
    format_names = {}

    path_location = Path(location)

    if path_location.is_file():
        extension = path_location.suffix
        file_ext.add(extension)
    elif path_location.is_dir():
        for file in path_location.iterdir():
            if file.is_file():
                file_ext.add(file.suffix)
    else:
        raise ValueError("location must point to a valid file or directory")

    # create mapping of extensions to normalized extension name
    for ext in file_ext:
        format_names[ext] = ext[1:].lower()

    formats = set(format_names.values())

    if len(formats) == 0:
        raise ValueError('no file formats found')

    source = Source(
        'file',
        formats,
        location,
    )

    return source





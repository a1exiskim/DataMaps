from pathlib import Path

class Source:
    def __init__(self, source_type, supported_format, location, unsupported_format):
        if isinstance(source_type, str):
            self.source_type = source_type  # i.e. file or database
        else:
            raise TypeError('source type must be string.')

        if isinstance(format, set):
            self.supported_format = supported_format # i.e json, postgres, parquet, etc
        else: 
            raise TypeError('format type must be set')

        if isinstance(location, str):
            self.location = location  # i.e filesystem path, database identifer 
        else:
            raise TypeError('location must be string.')

        if unsupported_format is not None and isinstance(unsupported_format, set):
            self.unsupported_format = unsupported_format
        elif unsupported_format is None:
            self.unsupported_format = set()
        else:
            raise TypeError('invalid value for unsupported format')
      
        


def indentify_source(location):
    file_ext = set()
    format_names = {}
    supported_formats = {'csv', 'json', 'parquet', 'avro', 'orc', 'text'}

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

    discovered_formats = set(format_names.values())

    unsupported_format = discovered_formats - supported_formats

    supported_format = discovered_formats - unsupported_format

    if len(supported_format) == 0:
        raise ValueError('no supported file formats found')

    source = Source(
        'file',
        supported_format,
        location,
        unsupported_format
    )

    return source





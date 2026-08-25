from pathlib import Path 
from datetime import datetime

def get_source_metadata(source: Path):
    name = source.name
    path = source 
    extension = source.suffix
    size_bytes = source.stat().st_size
    recent_timestamp = source.stat().st_mtime
    recent_datetime = datetime.fromtimestamp(recent_timestamp)

    source_metadata = {
        'name': name,
        'path': path,
        'extension': extension,
        'size_bytes': size_bytes,
        'last modified': recent_datetime
    }

    return source_metadata
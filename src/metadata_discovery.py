from pathlib import Path 
from datetime import datetime
import json
import ijson

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


def get_dataset_metadata():
    pass


def get_json_metadata(json_path):
    with json_path.open(mode='r') as raw_data:
        record_count = 0

        records = ijson.items(raw_data, 'item')
        fields = set()

        collection_of_types = {}
        null_count = {}
        fields_missing_count = {}

        for record in records: 
            record_count += 1
            current_keys = set(record.keys()) # only accounts for keys found in current iteration

            # updates missing record for newly discovered fields 
            for current_key in current_keys:
                if current_key not in fields:
                    fields_missing_count[current_key] = current_keys - fields

            fields.update(record.keys()) # accounts for all keys found in each iteration
            

            for key, value in record.items():
                if key not in collection_of_types:
                    collection_of_types[key] = set() # keys can have different data types as values (2, 'two'). the set keeps track of data types. 
                    null_count[key] = 0
                

                collection_of_types[key].add(type(value))

                if value is None or value == 'null':
                    null_count[key] += 1 

            # updates missing record for already known fields
            missing_keys = fields - current_keys
            for missing_key in missing_keys:
                if missing_key not in fields_missing_count:
                    fields_missing_count[missing_key] = record_count - 1
        

    return {
        "record count": record_count,
        "fields": fields,
        "field type(s)": collection_of_types,
        "field null count": null_count,
        "count of missing per field": fields_missing_count
    }
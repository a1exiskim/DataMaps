from pathlib import Path 
from datetime import datetime
import json
import ijson

def get_source_metadata(source: Path):
    """
    Extract file-level metadata from a source file. 
    
    Args: source: Path to the source file. 
    
    Returns: A dictionary containing the file name, path, extension, size in bytes, and last modified timestamp.
    """

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


def get_dataset_metadata(dataframe):
    """
    Extract structural metadata from a Spark DataFrame. 
    
    Args: dataframe: Spark DataFrame to analyze. 
    
    Returns: A dictionary containing the total row count, column names, column count, and schema of the DataFrame.
    """

    row_count = dataframe.count()

    schema = {}

    spark_schema = dataframe.schema 
    for struct_field in spark_schema:
        schema[struct_field.name] = struct_field.dataType.simpleString()


    structural_metadata = {
        'total row count': row_count,
        'columns': dataframe.columns,
        'column count': len(dataframe.columns),
        'schema': schema
    }

    return structural_metadata


def get_quality_metadata(source, reader):
    """
    Analyze data quality for each file in a source. 
    Calculates record counts, null counts, null percentages, and fields with inconsistent data types. 
    
    Args: 
        source: Data source containing the file or directory to analyze. 
        reader: Reader used to read raw records from each file. 
        
    Returns: A dictionary containing quality metadata for each file. """

    quality_metadata = {}
    path = Path(source.location)

    if path.is_dir():
        items = [item for item in path.iterdir() if item.is_file()]
    elif path.is_file():
        items = [path]

    else:
        raise ValueError('invalid file.')

    for item in items: 
        record_count = 0
        null_counts = {}
        null_percent = {}
        observed_types = {}
        type_issues = {}

        records = reader.read_raw(item)

        for record in records:  
            record_count += 1

            if isinstance(record, dict):
                for field, value in record.items():
                    if (value is None or value == "") and field not in null_counts: 
                        null_counts[field] = 0
                        null_counts[field] += 1
                    elif (value is None or value == "") and field in null_counts:
                        null_counts[field] += 1

                    if value is not None and field not in observed_types:
                        observed_types[field] = set()
                        observed_types[field].add(type(value))
                    elif value is not None and field in observed_types:
                        observed_types[field].add(type(value))

            else:
                raise TypeError('not a dictionary.')  

        for field, types in observed_types.items():
            if len(types) > 1:
                type_issues[field] = types

        for null_field in null_counts:
            null_percent[null_field] = round((null_counts[null_field] / record_count) * 100, 2) 

        quality_metadata[item.name] = {
            'record count': record_count,
            'null counts': null_counts,
            'null percentages': null_percent,
            'type issues': type_issues
        }

    return quality_metadata
from spark.ingestion import identify_file_source
from spark.readers.generic_file_reader import GenericFileReader
from src.metadata_discovery import get_source_metadata, get_dataset_metadata, get_quality_metadata
from pathlib import Path

def run_pipeline(source_location, spark, options):
    datasets_metadata = {}

    source = identify_file_source(source_location)

    reader = GenericFileReader(spark)

    for format in source.source_info:
        for file in source.source_info[format]:
            path_file = Path(file)
            source_metadata = get_source_metadata(path_file)

            df = reader.read(file, format, options[format])
            dataset_metadata = get_dataset_metadata(df) 

            datasets_metadata[file] = {
                'source_metadata': source_metadata,
                'dataset_metadata': dataset_metadata
            }

    quality_metadata = get_quality_metadata(source, reader)

    for file in datasets_metadata:
        datasets_metadata[file]['quality_metadata'] = quality_metadata[file]

    return datasets_metadata
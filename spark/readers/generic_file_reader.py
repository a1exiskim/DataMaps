from spark.readers.reader import Reader
from pathlib import Path
import csv
import json
import ijson
import pyarrow.parquet as pq

class GenericFileReader(Reader):
    
    """
    Reader implementation for loading common file-based data formats using Spark.

    Supports CSV, JSON, Parquet, ORC, Avro, and text files. Validates that the
    requested format is available in the source and supported by this reader
    before loading the files into a Spark DataFrame.
    """

    supported_formats = {'csv', 'json', 'parquet', 'orc', 'avro', 'text'}


    def __init__(self, spark):
        self.spark = spark

        self.handlers = {
                ".csv": self._read_csv_raw,
                ".ndjson": self._read_ndjson_raw,
                ".json": self._read_json_raw,
                ".parquet": self._read_parquet_raw
        }

    def read(self, source, format, options):
        """
        Reads files from a source using the specified format and Spark options.

        Args:
            source: Data source containing files grouped by format.
            format: File format to read.
            options: Spark reader options to apply.
        """

        if format not in source.source_info:
            raise ValueError("format not found in source")

        if format not in self.supported_formats:
            raise ValueError("format not supported by GenericFileReader")

        files = source.source_info[format]
        df = self.spark.read.format(format).options(**options).load(files)


        return df


    def read_raw(self, file_path: Path):
        extension = file_path.suffix.lower()

        handler = self.handlers[extension]

        return handler(file_path)    


    def _read_csv_raw(self, file_path):
        with file_path.open("r") as file:
            rows = csv.DictReader(file)

            for row in rows:
                yield row

    def _read_ndjson_raw(self, file_path):
        with file_path.open("r") as file:
            for line in file:
                row = json.loads(line)
            
                yield row

    def _read_json_raw(self, file_path):
        """This reader only supports top-level array JSON"""
        
        with file_path.open("rb") as file:
            rows = ijson.items(file, "item")
            for row in rows:
                yield row

    def _read_parquet_raw(self, file_path):
        open_file = pq.ParquetFile(file_path)

        for batch in open_file.iter_batches():
            for row in batch.to_pylist():
                yield row

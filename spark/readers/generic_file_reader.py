from spark.readers.reader import Reader
from pathlib import Path
import csv
import json
import ijson
import pyarrow.parquet as pq

class GenericFileReader(Reader):
    
    """
    Reader implementation for loading common file-based data formats using Spark.

    Supports CSV, JSON, NDJSON, Parquet. Validates that the
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

    def read(self, file_path, format, options):
        """
        Reads file from a file path using the specified format and Spark options.

        Args:
            file_path: location to single file.
            format: File format to read.
            options: Spark reader options to apply.

        Returns:
            A Spark DataFrame containing the file's data.
        """

        
        if format not in self.supported_formats:
            raise ValueError("format not supported by GenericFileReader")
        if Path(file_path).suffix[1:] != format:
            raise ValueError("format and reader do not match")

        df = self.spark.read.format(format).options(**options).load(str(file_path))

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

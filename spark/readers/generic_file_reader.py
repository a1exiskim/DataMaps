from spark.readers.reader import Reader

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
            
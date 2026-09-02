from spark.readers.reader import Reader

class GenericFileReader(Reader):
    supported_formats = {'csv', 'json', 'parquet', 'orc', 'avro', 'text'}

    def __init__(self, spark):
        self.spark = spark

    def read(self, source, format, options):
        if format not in source.formats:
            raise ValueError("format not found in source")

        if format not in self.supported_formats:
            raise ValueError("format not supported by GenericFileReader")

        files = source.files_by_format[format]
        df = self.spark.read.format(format).options(**options).load(files)


        return df
            
from spark.readers.reader import Reader
from spark.ingestion import Source
from pyspark.sql import SparkSession

class CSVReader(Reader):
    def __init__(self, spark):
        self.spark = spark # spark is a SparkSession

    def read(self, source):
        if "csv" not in source.supported_format:
            raise ValueError("Source does not contain CSV format")

        df = self.spark.read.csv(source.location, header=True, inferSchema=True )

        return df
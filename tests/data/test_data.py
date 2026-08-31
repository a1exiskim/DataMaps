import pytest
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql import Row
from spark.ingestion import Source
from spark.readers.csv_reader import CSVReader

spark = SparkSession.builder \
    .appName("DataMaps Tests") \
    .master("local[*]") \
    .getOrCreate()

def test_csv_reader():
    test_file = Path(__file__).parent / "test.csv"
    source = Source("file", {"csv"}, str(test_file), set())

    reader = CSVReader(spark)

    df = reader.read(source)

    assert isinstance(df, DataFrame)

    assert df.columns == ['name','age', 'city']

    assert df.collect() == [Row(name='Alice', age=20, city='Toronto'), 
                            Row(name='Bob', age=25, city='Waterloo'),
                            Row(name='Charlie', age=22, city='Ottawa')]
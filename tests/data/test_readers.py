import pytest
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql import Row
from spark.ingestion import Source
from spark.readers.csv_reader import CSVReader
from spark.readers.json_reader import JSONReader
from spark.readers.generic_file_reader import GenericFileReader

spark = SparkSession.builder \
    .appName("DataMaps Tests") \
    .master("local[*]") \
    .getOrCreate()


def test_generic_reader():
    test_file = Path(__file__).parent / "test.csv"
    source = Source("file", 
                    {"csv"}, 
                    str(test_file), 
                    {"csv": [str(test_file)]}
    )
    
    reader = GenericFileReader(spark)

    df = reader.read(source, "csv", {'header': 'true',
                                     'inferSchema': 'true'})

    assert isinstance(df, DataFrame)
    assert df.columns == ['name','age', 'city']
    assert df.collect() == [Row(name='Alice', age=20, city='Toronto'), 
                                Row(name='Bob', age=25, city='Waterloo'),
                                Row(name='Charlie', age=22, city='Ottawa')
                                ]
    

def test_generic_reader_invalid_format():
    test_file = Path(__file__).parent / "test.csv"

    source = Source(
        "file",
        {"csv"},
        str(test_file),
        {"csv": [str(test_file)]}
    )

    reader = GenericFileReader(spark)

    with pytest.raises(ValueError):
        reader.read(source, "json", {})


def test_generic_reader_unsupported_format():
    source = Source(
        "file",
        {"xml"},
        "test.xml",
        {"xml": ["test.xml"]}
    )

    reader = GenericFileReader(spark)

    with pytest.raises(ValueError):
        reader.read(source, "xml", {})
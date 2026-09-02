import pytest
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql import Row
from spark.ingestion import Source
from spark.ingestion import identify_file_source
from spark.readers.generic_file_reader import GenericFileReader

spark = (
    SparkSession.builder
    .appName("DataMaps Tests")
    .master("local[*]")
    .config("spark.driver.host", "localhost")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

def test_generic_reader():
    test_file = Path(__file__).parent / "test.csv"

    source = Source(
        "file",
        str(test_file),
        {"csv": [str(test_file)]}
    )

    reader = GenericFileReader(spark)

    df = reader.read(
        source,
        "csv",
        {'header': 'true', 'inferSchema': 'true'}
    )

    assert isinstance(df, DataFrame)
    assert df.columns == ['name', 'age', 'city']
    assert df.collect() == [
        Row(name='Alice', age=20, city='Toronto'),
        Row(name='Bob', age=25, city='Waterloo'),
        Row(name='Charlie', age=22, city='Ottawa')
    ]


def test_generic_reader_invalid_format():
    test_file = Path(__file__).parent / "test.csv"

    source = Source(
        "file",
        str(test_file),
        {"csv": [str(test_file)]}
    )

    reader = GenericFileReader(spark)

    with pytest.raises(ValueError):
        reader.read(source, "json", {})


def test_generic_reader_unsupported_format():
    source = Source(
        "file",
        "test.xml",
        {"xml": ["test.xml"]}
    )

    reader = GenericFileReader(spark)

    with pytest.raises(ValueError):
        reader.read(source, "xml", {})


def test_Source():
    source_info = {
        "csv": ["/data/test.csv"],
        "json": ["/data/test.json"]
    }

    source = Source(
        "file",
        "/data",
        source_info
    )

    assert source.source_type == "file"
    assert source.location == "/data"
    assert source.source_info == source_info



def test_identify_file_source():
    location = Path(__file__).parent / "test.csv"

    test_identification = identify_file_source(location)

    assert test_identification.source_type == 'file'
    assert test_identification.location == str(location)
    assert test_identification.source_info == {"csv": [str(location)]}


def test_identify_file_from_directory_source(tmp_path):
    csv_file = tmp_path / "test.csv"
    json_file = tmp_path / "test.json"

    csv_file.write_text("name,age\nAlice,20\n")
    json_file.write_text('{"name": "Alice", "age": 20}\n')

    source = identify_file_source(str(tmp_path))

    assert source.source_type == "file"
    assert source.location == str(tmp_path)
    assert source.source_info == {
        "csv": [str(csv_file)],
        "json": [str(json_file)]
    }


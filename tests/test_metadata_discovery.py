import pytest
from src.metadata_discovery import get_source_metadata
from src.metadata_discovery import get_dataset_metadata
from src.metadata_discovery import get_quality_metadata
from spark.readers.generic_file_reader import GenericFileReader
from spark.ingestion import identify_file_source
from spark.ingestion import Source
from datetime import datetime
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("DataMaps Tests")
    .master("local[*]")
    .config("spark.driver.host", "localhost")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
    )


def test_correct_return(tmp_path):
    test_file = tmp_path/ "test.json"
    test_file.touch()

    test_file_timestamp = test_file.stat().st_mtime
    result = get_source_metadata(test_file)

    assert result == {"name": "test.json",
                      "path": test_file,
                      "extension": ".json",
                      "size_bytes": test_file.stat().st_size,
                      "last modified": datetime.fromtimestamp(test_file_timestamp)
                      }


def test_directory_metadata(tmp_path):
    test_dir = tmp_path/ "test folder"
    test_dir.mkdir()

    test_dir_timestamp = test_dir.stat().st_mtime

    result = get_source_metadata(test_dir)

    assert result == {"name": "test folder",
                      "path": test_dir,
                      "extension": "",
                      "size_bytes": test_dir.stat().st_size,
                      "last modified": datetime.fromtimestamp(test_dir_timestamp)}


def test_get_dataset_metadata():
    dataframe = spark.createDataFrame(
        [
            ("Alice", 20),
            ("Bob", 25),
        ],
        ["name", "age"]
    )

    metadata = get_dataset_metadata(dataframe)

    assert metadata["total row count"] == 2
    assert metadata["columns"] == ["name", "age"]
    assert metadata["column count"] == 2
    assert metadata["schema"] == {
        "name": "string",
        "age": "bigint"
    }


def test_get_quality_metadata_directory(tmp_path):
    file_1 = tmp_path / "customers.csv"
    file_1.write_text(
        "name,age,city\n"
        "Alice,20,Toronto\n"
        "Bob,,Toronto\n"
        "Charlie,25,\n"
    )

    file_2 = tmp_path / "orders.csv"
    file_2.write_text(
        "order_id,amount\n"
        "1,100\n"
        "2,invalid\n"
        "3,200\n"
    )

    source = identify_file_source(tmp_path)
    reader = GenericFileReader(spark)

    metadata = get_quality_metadata(source, reader)

    assert metadata[str(file_1)]["record_count"] == 3
    assert metadata[str(file_1)]["null_counts"] == {
        "age": 1,
        "city": 1
    }
    assert metadata[str(file_1)]["null percentages"] == {
        "age": 33.33,
        "city": 33.33
    }
    assert metadata[str(file_1)]["type_issues"] == {}

    assert metadata[str(file_2)]["record_count"] == 3
    assert metadata[str(file_2)]["null_counts"] == {}
    assert metadata[str(file_2)]["null percentages"] == {}
    assert metadata[str(file_2)]["type_issues"] == {} 


def test_get_quality_metadata_file(tmp_path):
    file_path = tmp_path / "customers.csv"
    file_path.write_text(
        "name,age,city\n"
        "Alice,20,Toronto\n"
        "Bob,,Toronto\n"
        "Charlie,25,\n"
    )

    source = identify_file_source(file_path)
    reader = GenericFileReader(spark)

    metadata = get_quality_metadata(source, reader)

    assert metadata[str(file_path)]["record_count"] == 3
    assert metadata[str(file_path)]["null_counts"] == {
        "age": 1,
        "city": 1
    }
    assert metadata[str(file_path)]["null percentages"] == {
        "age": 33.33,
        "city": 33.33
    }
    assert metadata[str(file_path)]["type_issues"] == {}


def test_get_quality_metadata_invalid_location(tmp_path):
    invalid_path = tmp_path / "does_not_exist.csv"

    source = Source(
        "file",
        str(invalid_path),
        {}
    )

    reader = GenericFileReader(spark)

    with pytest.raises(ValueError, match="invalid file."):
        get_quality_metadata(source, reader)

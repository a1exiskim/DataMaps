from spark.pipeline import run_pipeline
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("DataMaps Tests")
    .master("local[*]")
    .config("spark.driver.host", "localhost")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
    )

def test_run_pipeline_multiple_csv_files(tmp_path):
    customers = tmp_path / "customers.csv"
    customers.write_text(
        "name,age\n"
        "Alice,20\n"
        "Bob,25\n"
    )

    orders = tmp_path / "orders.csv"
    orders.write_text(
        "id,amount\n"
        "1,100\n"
        "2,200\n"
    )

    options = {
        "csv": {
            "header": "true",
            "inferSchema": "true"
        }
    }

    result = run_pipeline(tmp_path, spark, options)

    assert set(result.keys()) == {str(customers), str(orders)}

    assert "source_metadata" in result[str(customers)]
    assert "dataset_metadata" in result[str(customers)]
    assert "quality_metadata" in result[str(customers)]

    assert "source_metadata" in result[str(orders)]
    assert "dataset_metadata" in result[str(orders)]
    assert "quality_metadata" in result[str(orders)]

    assert result[str(customers)]["dataset_metadata"]["total row count"] == 2
    assert result[str(orders)]["dataset_metadata"]["total row count"] == 2
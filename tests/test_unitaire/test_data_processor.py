import pytest
from src.dbperf.utils.spark_session import spark

from src.dbperf.traitements.transformations.data_processor import process_data



def test_data_processor():
    # Create test data
    test_data = [
        {"value": 10},
        {"value": -5},
        {"value": 0}
    ]

    df = spark.createDataFrame(test_data)

    # Process data
    processed_df = process_data(df)

    # Collect results
    results = processed_df.collect()

    # Assertions
    assert len(results) == 3
    assert results[0]["processed_column"] == "positive"
    assert results[1]["processed_column"] == "negative"
    assert results[2]["processed_column"] == "zero"
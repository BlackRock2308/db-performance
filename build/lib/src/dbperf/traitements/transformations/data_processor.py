from random import random

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, IntegerType

from src.dbperf.utils.spark_session import spark


def data_processor() -> None:

    # Create test data
    data = [
        {"value": 10},
        {"value": -5},
        {"value": 0}
    ]

    df = spark.createDataFrame(data)

    # Process the data
    processed_df = process_data(df)

    # Show the processed DataFrame
    processed_df.show()


def process_data(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "processed_column",
        when(col("value") > 0, "positive")
        .when(col("value") < 0, "negative")
        .otherwise("zero")
    )
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when


def process_data(df: DataFrame) -> DataFrame:

    return df.withColumn(
            "processed_column",
            when(col("value") > 0, "positive")
            .when(col("value") < 0, "negative")
            .otherwise("zero")
    )
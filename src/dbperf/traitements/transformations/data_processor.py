from random import random

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when

from src.dbperf.utils.spark_session import spark
import src.dbperf.traitements.constants as C
import pyspark.sql.functions as F
from src.dbperf.utils.logger import logger

hdfs_path = "hdfs://namenode:8020/user/spark/app/demande_pret_immo"


def data_processor() -> None:

    logger.info("Starting data processor")

    data_test_df , demande_pret_immo = load_data()

    process_data_test(data_test_df)

    logger.info("Calling process_data_BanquePrincipaleEmp__c")

    final_df = process_data_BanquePrincipaleEmp__c(demande_pret_immo)






def load_data() -> (DataFrame, DataFrame):
    # Create test data
    data = [
        {"value": 10},
        {"value": -5},
        {"value": 0}
    ]

    df_data_test = spark.createDataFrame(data)

    demande_pret_immo_df = (
        spark.read.options(header="True", sep=",")
        .csv(C.BASE_DIR + "/data/demande_pret_immo.csv")
        .drop("index")
    )

    return df_data_test, demande_pret_immo_df



def process_data_test(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "processed_column",
        when(F.col("value") > 0, "positive")
        .when(F.col("value") < 0, "negative")
        .otherwise("zero")
    )


def process_data_BanquePrincipaleEmp__c(df: DataFrame) -> DataFrame:

    filter_condition = F.col("BanquePrincipaleEmp__c") == "BNP PARIBAS"

    df_filtered = df.filter(filter_condition).select(
        F.col("Id"),
        F.col("MensuSouhaitePret__c"),
        F.col("Age_emprunteur__c"),
        F.col("CreatedDate"),
        F.col("DurSouhaitePret__c"),
        F.col("MontAppPerso__c"),
        F.col("TechMail_CategorieProfessionnelleEmpru__c"),
        F.col("TypBien__c")
    )

    df_filtered.show()
    logger.info(df_filtered.show(truncate=False))

    return df_filtered

# def save_to_hdfs(df: DataFrame, hdfs_path: str) -> None:
#     df.write.mode("overwrite").parquet(hdfs_path)

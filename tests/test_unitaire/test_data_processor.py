import pytest
from src.dbperf.utils.spark_session import spark

from src.dbperf.traitements.transformations.data_processor import process_data_test, process_data_BanquePrincipaleEmp__c
import src.dbperf.traitements.constants as C

def test_data_processor():
    # Create test data
    test_data = [
        {"value": 10},
        {"value": -5},
        {"value": 0}
    ]

    demande_pret_iommo_df = (
        spark.read.options(header="True", sep=",")
        .csv(C.BASE_DIR + "/data/demande_pret_immo.csv")
        .drop("index")
    )

    df = spark.createDataFrame(test_data)

    # Process data test
    processed_df = process_data_test(df)

    # Process csv data
    process_data_BanquePrincipaleEmp__c(demande_pret_iommo_df)

    # Collect results
    results = processed_df.collect()

    # Assertions
    assert len(results) == 3
    assert results[0]["processed_column"] == "positive"
    assert results[1]["processed_column"] == "negative"
    assert results[2]["processed_column"] == "zero"
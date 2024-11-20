import os
import sys
import pytest
from src.dbperf.utils.spark_session import spark


# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def spark_session():
    return spark

@pytest.fixture(scope="session")
def stop_spark_session():
    yield
    spark.stop()
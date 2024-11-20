from pyspark import SparkConf

#from great_expectations import DataContext

config = (
    SparkConf()
    .set("spark.pyspark.python", "/opt/anaconda3/envs/dbperf_env/bin/python")
    .set("spark.pyspark.driver.python", "/opt/anaconda3/envs/dbperf_env/bin/python")
)


# Initialisation du context great_expectations
#context = DataContext("src/great_expectations")

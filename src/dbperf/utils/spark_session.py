from pyspark.sql import SparkSession

def get_spark_session(app_name="DbPerf App"):
    return (SparkSession.builder
            .appName(app_name)
            .master("local[*]")
            .config("spark.sql.warehouse.dir", "spark-warehouse")
            .config("spark.sql.crossJoin.enabled", "true")
            .config("spark.pyspark.python", "/opt/anaconda3/envs/dbperf_env/bin/python")
            .config("spark.pyspark.driver.python", "/opt/anaconda3/envs/dbperf_env/bin/python")
            .enableHiveSupport()
            .getOrCreate())

spark = get_spark_session()



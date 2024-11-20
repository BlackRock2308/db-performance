"""
Logger

~~~~~~~~~~~~~

Ce module contient l'objet log4j instancié
par le SparkContext actif, permettant la journalisation Log4j pour PySpark.
"""
from src.dbperf.utils.configurations import config
from src.dbperf.utils.spark_session import spark

# get spark app details with which to prefix all messages

app_name = config.get("spark.app.name", "DBPERF-TRAITEMENTS")

log4j = spark._jvm.org.apache.log4j
message_prefix = f"{app_name}"
logger = log4j.LogManager.getLogger(message_prefix)

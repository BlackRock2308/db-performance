#!/bin/bash

# Project configuration
PROJECT_ROOT="/Users/macbookpro/Documents/db-perf-project"
TMP_DIR="/tmp/db-perf-spark"
APP_SCRIPT="dbperf-app.py"
HDFS_DIR="/user/spark/app"

# Prepare distribution and temporary directory
mkdir -p $TMP_DIR

# Create distribution if it doesn't exist
if [ ! -d "dist" ]; then
    echo "Creating wheel distribution..."
    python setup.py bdist_wheel
fi

# Get the wheel file name
WHEEL_FILE=$(ls dist/*.whl | head -n 1)
WHEEL_FILENAME=$(basename $WHEEL_FILE)

# Validate required files
if [ ! -f "$PROJECT_ROOT/conf/dbperf.conf" ]; then
    echo "Configuration file not found: $PROJECT_ROOT/conf/dbperf.conf"
    exit 1
fi

if [ ! -f "$PROJECT_ROOT/$APP_SCRIPT" ]; then
    echo "Application script not found: $PROJECT_ROOT/$APP_SCRIPT"
    exit 1
fi

# Upload files to HDFS
docker exec -it namenode hdfs dfs -mkdir -p $HDFS_DIR
docker exec -it namenode hdfs dfs -put -f /project/dist/dbperf-0.1.0-py3-none-any.whl $HDFS_DIR/
docker exec -it namenode hdfs dfs -put -f /project/conf/dbperf.conf $HDFS_DIR/
docker exec -it namenode hdfs dfs -put -f /project/dbperf-app.py $HDFS_DIR/

# Create the Spark events directory in HDFS
docker exec -it namenode hdfs dfs -mkdir -p /tmp/spark-events

# Set proper permissions
docker exec -it namenode hdfs dfs -chmod 777 /tmp/spark-events


# Submit Spark job
docker exec -it spark-master /spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    --conf spark.eventLog.enabled=true \
    --conf spark.eventLog.dir=hdfs://namenode:8020/tmp/spark-events \
    --conf spark.ui.port=4040 \
    --conf spark.driver.host=0.0.0.0 \
    --conf spark.driver.bindAddress=0.0.0.0 \
    --conf spark.eventLog.enabled=true \
    --conf spark.eventLog.dir=hdfs://namenode:8020/tmp/spark-events \
    --conf spark.history.fs.logDirectory=hdfs://namenode:8020/tmp/spark-events \
    --name "DBPERF-TRAITEMENT" \
    --py-files hdfs://namenode:8020${HDFS_DIR}/$(basename $WHEEL_FILE) \
    --files hdfs://namenode:8020${HDFS_DIR}/dbperf.conf \
    hdfs://namenode:8020${HDFS_DIR}/$APP_SCRIPT -t data_processor


# Check job submission status
if [ $? -eq 0 ]; then
    echo "Spark job submitted successfully!"
else
    echo "Error submitting Spark job."
fi

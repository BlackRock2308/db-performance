#!/bin/bash

# Project configuration
PROJECT_ROOT="/Users/macbookpro/Documents/db-perf-project"
TMP_DIR="/tmp/db-perf-spark"
APP_SCRIPT="dbperf-app.py"

# Prepare distribution and temporary directory
mkdir -p $TMP_DIR
python3 setup.py bdist_wheel
WHEEL_FILE=$(ls dist/*.whl | head -n 1)
WHEEL_FILENAME=$(basename $WHEEL_FILE)

# Copy necessary files
cp $PROJECT_ROOT/conf/dbperf.conf $TMP_DIR/
cp $PROJECT_ROOT/conf/log4j.properties $TMP_DIR/
cp $WHEEL_FILE $TMP_DIR/
cp $PROJECT_ROOT/$APP_SCRIPT $TMP_DIR/

# Submit Spark job
docker run --rm \
    --network host \
    --volume $TMP_DIR:/opt/spark/work-dir \
    bde2020/spark-submit:3.1.1-hadoop3.2 \
    /spark/bin/spark-submit \
    --master local[*] \
    --deploy-mode client \
    --conf "spark.app.name=DBPERF-TRAITEMENT" \
    --py-files /opt/spark/work-dir/${WHEEL_FILENAME} \
    --files /opt/spark/work-dir/log4j.properties \
    --files /opt/spark/work-dir/dbperf.conf \
    /opt/spark/work-dir/$APP_SCRIPT -t data_processor

# Check job submission status
if [ $? -eq 0 ]; then
    echo "Spark job submitted successfully!"
else
    echo "Error submitting Spark job."
fi

# Clean up
rm -rf $TMP_DIR
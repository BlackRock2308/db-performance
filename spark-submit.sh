#!/bin/bash

# Set the project root directory
PROJECT_ROOT="/Users/macbookpro/Documents/db-perf-project"

# Create distribution if it doesn't exist
if [ ! -d "dist" ]; then
    echo "Creating wheel distribution..."
    python setup.py bdist_wheel
fi

# Get the wheel file name
WHEEL_FILE=$(ls dist/*.whl | head -n 1)
WHEEL_FILENAME=$(basename $WHEEL_FILE)

# Copy necessary files to a temporary directory that will be mounted
TMP_DIR="/tmp/db-perf-spark"
echo "Creating temporary directory at $TMP_DIR..."
mkdir -p $TMP_DIR
cp $PROJECT_ROOT/conf/dbperf.conf $TMP_DIR/
cp $PROJECT_ROOT/conf/log4j.properties $TMP_DIR/
cp $WHEEL_FILE $TMP_DIR/
cp -r $PROJECT_ROOT/src $TMP_DIR/

# Set environment variables to tell Spark to use the Hadoop configuration from the container
export HADOOP_CONF_DIR=/etc/hadoop
export YARN_CONF_DIR=/etc/hadoop

# Set YARN ResourceManager address (replace with actual hostname or IP address if needed)
YARN_RESOURCE_MANAGER_URI="yarn://172.28.0.4:8032"  # Update with the correct IP address or hostname

echo "Submitting Spark job..."
docker run --network hadoop-local_default \
    --volume $TMP_DIR:/opt/spark/work-dir \
    --volume /etc/hadoop:/etc/hadoop \
    -e HADOOP_CONF_DIR=/etc/hadoop \
    -e YARN_CONF_DIR=/etc/hadoop \
    -e SPARK_YARN_RESOURCEMANAGER=$YARN_RESOURCE_MANAGER_URI \
    bde2020/spark-submit:3.1.1-hadoop3.2 \
    /spark/bin/spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --conf "spark.app.name=DBPERF-TRAITEMENT" \
    --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=python3 \
    --conf spark.executor.memory=4g \
    --conf spark.executor.cores=2 \
    --conf spark.yarn.resourcemanager.address=$YARN_RESOURCE_MANAGER_URI \
    --py-files /opt/spark/work-dir/${WHEEL_FILENAME} \
    --files /opt/spark/work-dir/log4j.properties \
    --properties-file /opt/spark/work-dir/dbperf.conf \
    /opt/spark/work-dir/src/dbperf-app.py -t process_data

SUBMIT_STATUS=$?

# Check if the submission was successful
if [ $SUBMIT_STATUS -eq 0 ]; then
    echo "Spark job submitted successfully!"
    echo "You can monitor the job at:"
    echo "- YARN UI: http://localhost:8088"
    echo "- Spark History Server: http://localhost:18080"
else
    echo "Error submitting Spark job. Exit code: $SUBMIT_STATUS"
fi

# Clean up
echo "Cleaning up temporary files..."
rm -rf $TMP_DIR

echo "Done!"

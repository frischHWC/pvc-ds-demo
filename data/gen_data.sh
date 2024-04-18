#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#!/usr/bin/env bash

# DATAGEN_URL should be in this form: https://bootcamp-1.vpc.cloudera.com:4242
DATAGEN_URL="https://localhost:4242"
DATAGEN_USER="admin"
DATAGEN_PASSWORD="admin"
DATA_SIZE="small"

. ./logger.sh

generate_data() {
local SINK=$1
local MODEL_FILE=$2
local BATCHES=$3
local ROWS=$4
local THREADS=$5

logger info "Generating data from model #bold:${MODEL_FILE}#end_bold to #bold:${SINK}#end_bold with #bold:${BATCHES}#end_bold batches of #bold:${ROWS}#end_bold rows each"

COMMAND_ID=$(curl -s -k -X POST -H "Accept: */*" -H "Content-Type: multipart/form-data ; boundary=toto" \
    -F "model_file=@${MODEL_FILE}" -u ${DATAGEN_USER}:${DATAGEN_PASSWORD} \
    "${DATAGEN_URL}/datagen/${SINK}/?batches=${BATCHES}&rows=${ROWS}&threads=${THREADS}" | jq -r '.commandUuid' )

logger info "Checking status of the command"
while true
do
    STATUS=$(curl -s -k -X POST -H "Accept: application/json" -u ${DATAGEN_USER}:${DATAGEN_PASSWORD} \
        "${DATAGEN_URL}/command/getCommandStatus?commandUuid=${COMMAND_ID}" | jq -r ".status")
    printf '.'
    if [ "${STATUS}" == "FINISHED" ]
    then
        echo ""
        logger success "SUCCESS: Command for model ${MODEL_FILE}" 
        break
    elif [ "${STATUS}" == "FAILED" ]
    then 
        echo ""
        logger error "FAILURE: Command for model ${MODEL_FILE}"
        exit 1
    else
        sleep 5
    fi           
done


}

if [ ! -z $1 ]; then
    DATA_SIZE=$1
fi

cp resources/stock_names.csv /tmp/

logger info "Data generation size is: #bold:$DATA_SIZE"
logger info "Datagen server used is at: #underline:${DATAGEN_URL}#end_underline"

case $DATA_SIZE in 
    "small")
        generate_data hdfs-parquet models/weather.json 10 100000 10
        generate_data hdfs-parquet models/bank-account.json 10 1000000 10
        generate_data hive models/bank-account.json 10 1000000 10
        generate_data hive models/atm.json 10 100000 10
        generate_data hive models/stock-price.json 1 100 1
        generate_data hive models/stock-transaction.json 10 100000 10
        generate_data hive models/traders.json 1 1000 1
        generate_data hdfs-parquet models/plant.json 1 1000 1
        generate_data hdfs-parquet models/sensor.json 10 10000 10
        generate_data hdfs-parquet models/sensor-data.json 10 100000 10
    ;;
    "medium")
        generate_data hdfs-parquet models/weather-model.json 10 100000 10
    ;;
    "large")
        generate_data hdfs-parquet models/weather-model.json 10 100000 10
    ;;
    "extra-large")
        generate_data hdfs-parquet models/weather-model.json 10 100000 10
    ;;
    *)
        logger warn "$DATA_SIZE not recognized as not among: small, medium, large, extra-large"
        exit 0
    ;;
esac


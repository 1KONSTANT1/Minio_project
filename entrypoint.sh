#!/bin/bash

until mc alias set myminio http://minio:9000 ${MINIO_USER} ${MINIO_PASSWORD}; do
    echo "Failed to set mc alias. Retrying in 5 seconds..."
    echo $?
    sleep 1
done

mc mb myminio/testbucket

mc quota set myminio/testbucket --size 5m
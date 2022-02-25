#!/usr/bin/env bash

set -euo pipefail

HOST="${1-"http://0.0.0.0"}"
PORT="${2-"5000"}"

echo "Running server on ${HOST}:${PORT}"
function test_hello {
    HELLO=$(curl --location --request GET "${HOST}:${PORT}/")

    HELLO_TEST=$(echo "${HELLO}" | grep -i "Hello")
}

function test_ping {
    PING=$(curl --location --request GET "${HOST}:${PORT}/ping")

    PING_TEST=$(echo "${PING}" | grep -i "pong")
}

function test_batch {
    BATCH_PREDICTIONS=$(curl --location --request POST "${HOST}:${PORT}/batch" \
        --header 'Content-Type: application/json' \
        --data-raw '{
                    "instances": [[0.077863387626902], [-0.0396181284261162], [0.0110390390462862]]
                }')

    BATCH_PREDICTIONS_TEST=$(echo "${BATCH_PREDICTIONS}" | grep -i "predictions")
}

function test_stream {
    STREAM_PREDICTIONS=$(curl --location --request POST "${HOST}:${PORT}/stream" \
        --header 'Content-Type: application/json' \
        --data-raw '{
                    "instance": 0.0110390390462862
                }')

    STREAM_PREDICTIONS_TEST=$(echo "${BATCH_PREDICTIONS}" | grep -i "prediction")
}

function run_tests {

    RETRIES=5
    echo "$RETRIES"

    for ATTEMP_NUMBER in $(seq 1 "${RETRIES}"); do
        echo "Attempt $ATTEMP_NUMBER of ${RETRIES}"
        test_hello || echo "Hello test failed!"
        test_ping || echo "Ping test failed!"
        test_batch || echo "BATCH_PREDICTIONS test failed!"
        test_stream || echo "STREAM_PREDICTIONS test failed!"

        if [ -z "${HELLO_TEST}" ] || [ -z "${PING_TEST-}" ] || [ -z "${BATCH_PREDICTIONS_TEST-}" ] || [ -z "${STREAM_PREDICTIONS_TEST-}" ]; then
            echo "One of the tests failed"
            echo "HELLO = ${HELLO}"
            echo "PING = ${PING}"
            echo "BATCH_PREDICTIONS = ${BATCH_PREDICTIONS}"
            echo "STREAM_PREDICTIONS = ${STREAM_PREDICTIONS}"

            echo "Sleeping for 15sec... and retry"

            sleep 15
        else
            echo "HELLO: ${HELLO}"
            echo "PING: ${PING}"
            echo "BATCH_PREDICTIONS: ${BATCH_PREDICTIONS}"
            echo "STREAM_PREDICTIONS: ${STREAM_PREDICTIONS}"
            echo "Tests Passed!"
            exit 0
        fi

    done

    echo "Max retries reached!"
    echo "Exiting..."
    exit 1
}
echo "args $1 $2"
run_tests "$@"

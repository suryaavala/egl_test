from flask import Flask, request, jsonify
import os
import json
from linear_regressor.predict import get_predictions
import jsonschema
from typing import Dict, Any
import logging

log = logging.getLogger(__name__)

app = Flask(__name__)

# NOTE ideally would be definied as a openapi spec file but hardcoding for now
BATCH_REQUEST_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "instances": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number",
                },
                "minItems": 1,
                "maxItems": 1,
            },
        },
    },
    "required": ["instances"],
}

STREAM_REQUEST_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "instance": {
            "type": "number",
        },
    },
    "required": ["instance"],
}


@app.route("/")
def hello_world():
    return f"<p>Hello from {os.environ.get('NAME', __name__)}!</p>"


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong!"})


@app.route("/batch", methods=["POST"])
@app.route("/stream", methods=["POST"])
def predict(
    predict_request_data_schemas: Dict[str, Dict[str, Any]] = {
        "/batch": BATCH_REQUEST_SCHEMA,
        "/stream": STREAM_REQUEST_SCHEMA,
    }
):
    try:
        data = json.loads(request.get_data())
        log.info(f"Payload: {json.dumps(data, indent=2)}")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    is_data_schema_valid = _validate_predict_req_data(
        predict_request_data_schemas[request.path], data
    )
    if is_data_schema_valid is not True:
        return (
            json.dumps(
                {
                    "explanation": "Invalid request data. Data should be a valid json of the following schema.",
                    "validation_error": str(is_data_schema_valid),
                    "schema": predict_request_data_schemas[request.path],
                },
                indent=4,
            ),
            400,
        )
    if request.path == "/batch":
        predictions = get_predictions(data["instances"])
        return jsonify({"predictions": predictions})
    elif request.path == "/stream":
        predictions = get_predictions([data["instance"]])
        return jsonify({"prediction": predictions[0]})
    else:
        return jsonify({"error": "Invalid request path."}), 400


# @app.route("/stream", methods=["POST"])
# def stream(predict_request_data_schema: Dict[str, Any] = STREAM_REQUEST_SCHEMA):
#     try:
#         data = json.loads(request.get_data())
#         log.info(type(data), data)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

#     is_data_schema_valid = _validate_predict_req_data(predict_request_data_schema, data)
#     if is_data_schema_valid is not True:
#         return (
#             json.dumps(
#                 {
#                     "explanation": "Invalid request data. Data should be a valid json of the following schema.",
#                     "validation_error": str(is_data_schema_valid),
#                     "schema": predict_request_data_schema,
#                 },
#                 indent=4,
#             ),
#             400,
#         )
#     predictions = get_predictions([data["instances"]])
#     return jsonify({"prediction": predictions})


def _validate_predict_req_data(schema: Dict[str, Any], data: Dict[str, Any]) -> bool:
    jsonschema.Draft202012Validator.check_schema(schema)
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        return e
    return True


if __name__ == "__main__":
    app.run()

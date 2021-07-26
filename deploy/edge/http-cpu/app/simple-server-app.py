# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import json
import logging
from datetime import datetime, timezone

from flask import Flask, Response, Request, abort, request
from azure.iot.device import IoTHubModuleClient

from exception_handler import PrintGetExceptionDetails


def init_logging():
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger != None:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

app = Flask(__name__)
init_logging()

try:
    # The client object is used to interact with your Azure IoT hub.
    logging.info("Creating iot hub module client from edge env")
    module_client = IoTHubModuleClient.create_from_edge_environment()
    # connect the client
    logging.info("Connecting to iot hub module client")
    module_client.connect()
except Exception as err:
    # PrintGetExceptionDetails()
    logging.error("Execption in creating and connecting to iot hub module client: {}".format(err))

# / routes to the default function
@app.route('/', methods=['GET'])
def default_page():
    """Default route/page"""
    return Response(response='Hello from simple server!', status=200)

# /score routes to scoring function 
@app.route("/score", methods=['POST'])
def score():
    """This function returns a JSON object with inference duration and detected objects"""
    # Current date and time
    now = datetime.now()
    utc_now = datetime.now(timezone.utc).timestamp()
    try:
        input_message = module_client.receive_message_on_input("input1")  # blocking call
        if input_message.data:
            print("{} The data in the message received on azureeyemodule was {}".format(now, input_message.data))
            print("{} Custom properties are {}".format(now, input_message.custom_properties))

            # Gather inferences from azureeyemodule to correspond with when AVA is sending data
            # NB:  AVA is still sending images, but we are ignoring them
            inference_list = json.loads(input_message.data)['NEURAL_NETWORK']
            detected_objects = []
            if isinstance(inference_list, list):
                for item in inference_list:
                    xmin, ymin, xmax, ymax = [float(x) for x in item["bbox"]]
                    json_data = {
                        "type": "entity",
                        "entity" : {
                            "tag" : {
                                "value" : item["label"],
                                "confidence": float(item["confidence"])
                            },
                            "box": {
                                "l": xmin,
                                "t": ymin,
                                "w": xmax-xmin,
                                "h": ymax-ymin
                            }
                        }
                    }
                    detected_objects.append(json_data)

            if len(detected_objects) > 0:
                respBody = {
                    "timestamp" : utc_now,
                    "inferences" : detected_objects
                }
                respBody = json.dumps(respBody)
                return Response(respBody, status=200, mimetype='application/json')
            else:
                logging.info("No detections from azureeyemodule")
                respBody = {
                    "timestamp" : utc_now,
                    "inferences" : []
                }
                respBody = json.dumps(respBody)
                return Response(respBody, status=200, mimetype='application/json')               
        else:
            logging.info("No data in message from azureeyemodule")
            return Response(json.dumps({'No data from azureyemodule'}),
                            status=204, 
                            mimetype='application/json')
    except Exception as err:
        # PrintGetExceptionDetails()
        logging.error("Exception in score function.")
        return Response(json.dumps({"Execption in score function: {}".format(err)}), status=500)

# /score-debug routes to score_debug
# This function scores the image and stores an annotated image for debugging purposes
@app.route('/score-debug', methods=['POST'])
def score_debug():
    pass

if __name__ == '__main__':
    # Running the file directly
    app.run(host='0.0.0.0', port=8888)
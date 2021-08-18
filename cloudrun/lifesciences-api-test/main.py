from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from pprint import pprint
import os
import json
import sys

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('lifesciences', 'v2beta', credentials=credentials)
    parent = 'projects/maximal-dynamo-308105/locations/us-central1'

    with open(os.path.join(sys.path[0], "pipeline.json"), "r") as f:
        run_pipeline_request_body = json.load(f)

    request = service.projects().locations().pipelines().run(parent=parent, body=run_pipeline_request_body)
    response = request.execute()

    pprint(response)

    return ("", 204)

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)

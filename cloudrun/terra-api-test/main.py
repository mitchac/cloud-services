from pprint import pprint

from flask import Flask, request

import importlib.util

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    
    spec = importlib.util.spec_from_file_location("terra_api", "terra-api.py")
    terra_api = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(terra_api)

    workflow_config_response = terra_api.get_workflow_config("firstterrabillingaccount", "singlem-pilot-2", "singlem", "singlem-single-task")

    pprint(workflow_config_response)

    return ("", 204)

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
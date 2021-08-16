from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    from pprint import pprint

    credentials = GoogleCredentials.get_application_default()

    service = discovery.build('lifesciences', 'v2beta', credentials=credentials)

    # The name of the operation's parent resource.
    name = 'projects/maximal-dynamo-308105/locations/us-central1'  # TODO: Update placeholder value.

    request = service.projects().locations().operations().list(name=name)
    while True:
        response = request.execute()

        for operation in response.get('operations', []):
            pprint(operation['name'])

        request = service.projects().locations().operations().list_next(previous_request=request, previous_response=response)
        if request is None:
            break

    return ("", 204)

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)

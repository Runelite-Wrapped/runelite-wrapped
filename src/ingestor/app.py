from flask import Flask, request
from collections import defaultdict
import json

app = Flask(__name__)

_recieved_data = defaultdict(list)

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def handle_post_request(path):
    request_data = request.get_data()

    data = json.loads(request_data.decode('utf-8'))

    print(f"Sender IP: {request.remote_addr}")
    print(f"Path: {path}")
    print(f"Request body:\n{json.dumps(data, indent=4)}")

    _recieved_data[path].append(data)

    return "Request received", 200


@app.route('/<path:path>', methods=['GET'])
def handle_get_request(path):
    print(f"Sender IP: {request.remote_addr}")
    print(f"Path: {path}")

    if path in _recieved_data:
        return json.dumps(_recieved_data[path], indent=4).encode("utf-8"), 200
    else:
        return "No data found", 404


@app.route('/<path:path>', methods=['DELETE'])
def handle_delete_request(path):
    print(f"Sender IP: {request.remote_addr}")
    print(f"Path: {path}")

    if path in _recieved_data:
        del _recieved_data[path]
        return "Data deleted", 200
    else:
        return "No data found", 404


if __name__ == "__main__":
    app.run(debug=True)

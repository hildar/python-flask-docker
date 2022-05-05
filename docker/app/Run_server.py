#  USAGE
#  Start the server:
#  python Run_server.py
#  Submit a request via Python:
#  "Client.ipynb" or "Run_front_server.py"

#  import the necessary packages

#  module string is using into model.dill
import string
import pandas as pd
import os
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import dill

# type definition use for more than one working servers
dill._dill._reverse_typemap['ClassType'] = type

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

# initialize logging
handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# load the pre-trained model
def load_model(path):
    global model
    with open(path, 'rb') as f:
        model = dill.load(f)
    print(model)


model_path = "models/logreg_pipeline.dill"
load_model(model_path)


# Index page
@app.route("/", methods=["GET"])
def general():
    return """Welcome to Toxic comment prediction process. \
    Please use address 'http://localhost:8181/predict' with POST method"""


# POST request handler function
@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the view
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # ensure the text was properly uploaded to our endpoint
    if flask.request.method == "POST":
        comment_text = ""
        request_json = flask.request.get_json()
        if request_json["comment_text"]:
            comment_text = request_json['comment_text']

        logger.info(f'{dt} Data: comment_text={comment_text}')

        try:
            frame = pd.DataFrame({"comment_text": [comment_text]})
            preds = model.predict_proba(frame)
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = preds[0].tolist()
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print("* Loading the model and Flask starting server..."
          "please wait until server has fully started")
    port = int(os.environ.get('PORT', 8181))
    print(f'Port:{port}')
    app.run(host='0.0.0.0', debug=True, port=port)

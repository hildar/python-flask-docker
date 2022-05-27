# USAGE
# Start the server:
# pyrhon Run_front_server.py
# Go to the http://localhost:8180
# Enjoy

# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import StringField
from wtforms.validators import DataRequired
import urllib.request
import json
# import matplotlib.pyplot as plt
# import numpy as np


# create form fo text input and validate not empty field
class ClientDataForm(FlaskForm):
    comment_text = StringField("Type some text:", validators=[DataRequired()])


# initialize Flask
app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


# get predictions from main server (there is a model.dill)
def get_prediction(comment_text):
    body = {'comment_text': comment_text}
    # make url to main server
    myurl = "http://0.0.0.0:8181/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    # encode json
    jsondata = json.dumps(body)
    # needs to be bytes
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', str(len(jsondataasbytes)))
    # get response from main server
    response = urllib.request.urlopen(req, jsondataasbytes)
    # decode json and return predictions list
    return json.loads(response.read())['predictions']


# create index.html
@app.route("/")
def index():
    return render_template('index.html')


# create predicted.html
@app.route('/predicted/<response>')
def predicted(response):
    # decode json
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


# create predict_form.html
@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        # get comment text from request
        data['comment_text'] = request.form.get('comment_text')

        # try if not errors
        try:
            # get predictions list from main server
            preds = get_prediction(data['comment_text'])

            # Draw probabilities distribution.
            # It is working in my machine, but not work into docker.
            # color = ['red', 'blue', 'green', 'yellow', 'black', 'orange']
            # columns = np.array(['tx', 's_tx', 'obs', 'thr', 'ins', 'i_ht'])
            # plt.ioff()
            # plt.subplots(figsize=(4, 2))
            # plt.ylim(0, 1)
            # plt.bar(columns, np.array(preds), color=color)
            # plt.title('Probabilities')
            # plt.savefig('static/probabilities.png')
            # plt.close()

            # round predictions
            preds = [round(i, 2) for i in preds]
            # convert to dict
            response = {i: preds[i] for i in range(len(preds))}
            response['comment_text'] = data['comment_text']
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})

        # go to predicted.html
        return redirect(url_for('predicted', response=json.dumps(response)))

    # render predict_form.html
    return render_template('form.html', form=form)


# initialize front server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8180, debug=True)

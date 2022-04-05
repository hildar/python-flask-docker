import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import StringField
from wtforms.validators import DataRequired
# import matplotlib.pyplot as plt
# import numpy as np

import urllib.request
import json


class ClientDataForm(FlaskForm):
    comment_text = StringField("Type some text:", validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(comment_text):
    body = {'comment_text': comment_text}

    myurl = "http://0.0.0.0:8181/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['comment_text'] = request.form.get('comment_text')

        try:
            preds = get_prediction(data['comment_text'])

            # Draw probabilities distribution.
            # It is working in my machine, but not work in docker.
            # color = ['red', 'blue', 'green', 'yellow', 'black', 'orange']
            # columns = np.array(['tx', 's_tx', 'obs', 'thr', 'ins', 'i_ht'])
            # plt.ioff()
            # plt.subplots(figsize=(4, 2))
            # plt.ylim(0, 1)
            # plt.bar(columns, np.array(preds), color=color)
            # plt.title('Probabilities')
            # plt.savefig('static/probabilities.png')
            # plt.close()

            response = str([round(i, 2) for i in preds])
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})

        return redirect(url_for('predicted', response=response))

    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8180, debug=True)

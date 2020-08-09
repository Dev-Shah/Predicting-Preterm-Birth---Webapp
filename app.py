import flask
import pickle
import pandas as pd
import csv
import io
import os
import numpy as np
from flask import Flask, flash, request, redirect, url_for

from werkzeug.utils import secure_filename

# Use pickle to load in the pre-trained model
with open(f'model/model_sptd.pickle', 'rb') as f:
    model_sptd = pickle.load(f)
with open(f'model/model_pprom.pickle', 'rb') as f:
    model_pprom = pickle.load(f)
UPLOAD_FOLDER = '/home/xyz/Documents/webapp/uploads'
# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        # Extract the input
        #f=flask.request.files['SampleData']
        f=(request.files['SampleData'])
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_csv(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return str(df.shape)
        else:
            return 'Failure'
        # if not f:
        #     return "No file"
        # if f:
        #     f.save(secure_filename(f.filename))
        #     return 'file uploaded successfully'

        # temperature = flask.request.form['temperature']
        # humidity = flask.request.form['humidity']
        # windspeed = flask.request.form['windspeed']
        #
        # # Make DataFrame for model
        # input_variables = pd.DataFrame([[temperature, humidity, windspeed]],
        #                                columns=['temperature', 'humidity', 'windspeed'],
        #                                dtype=float,
        #                                index=['input'])
        #
        # # Get the model's prediction

        X_sptd=df[['80204_at','649446_at','4874_at','102723878_at','105370297_at','105372561_at','105377323_at','105377514_at','105379158_at','107984171_at','394_at','4124_at']].values
        X_sptd=X_sptd[0,:]
        X_pprom=df[['401285_at','101927434_at','26025_at','339175_at']].values
        X_pprom=X_pprom[0,:]
        model_sptd.n_jobs = 1
        model_pprom.n_jobs = 1

        prediction_sptd = np.around(model_sptd.predict_proba(X_sptd.reshape(1,-1)),decimals=2)
        print(prediction_sptd)
        prediction_pprom = np.around(model_pprom.predict_proba(X_pprom.reshape(1,-1)),decimals=2)
        print(prediction_pprom)


        # #
        # # # Render the form again, but add in the prediction and remind user
        # # # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'Probability of Spontaneous Preterm Birth is ':0,'Probability of PPROM is ':1},
                                     result=[prediction_sptd[:,1][0],prediction_pprom[:,1][0]],
                                     )

if __name__ == '__main__':
    app.run()

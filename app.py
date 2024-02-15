import pickle
from flask import Flask, request, app, jsonify, url_for, render_template

import numpy as np
import pandas as pd
import statsmodels

app=Flask(__name__)

#Load the model
v4model=pickle.load(open('SARIMAv4.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/forecast_api', methods=['POST'])
def forecast_api():
    try:
        data = request.get_json()
        #lower and upper range for a forecasting window
        value1 = data['value1']
        value2 = data['value2']
        hours = 8766 #number of hours in a year, this will further be refined to take the dates an input
      
        #Make predictions
        forecast = v4model.forecast(steps=hours)
        output = forecast.iloc[value1:value2].to_dict()

        # Convert Timestamp keys to strings
        output = {str(key): value for key, value in output.items()}

        return jsonify({'Energy consumption forecast': output})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
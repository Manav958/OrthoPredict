from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Function to train the linear regression model
def train_linear_regression_model():
    # Configure the credentials and access Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('iot-fracture-recovery-32774b3e943d.json', scope)
    client = gspread.authorize(credentials)

    # Read the training data from Google Sheets
    train_sheet = client.open('TraingSheet1 ').sheet1  # Replace with your training sheet name
    train_data = pd.DataFrame(train_sheet.get_all_records())

    # Split the data into input features (X) and target variable (y)
    X_train = train_data[['X_angle', 'Y_angle', 'Z_angle']]
    y_train = train_data['Recovery_rate']

    # Create an instance of the LinearRegression model
    model = LinearRegression()

    # Fit the model to the training data
    model.fit(X_train, y_train)

    return model

# Train the model when the application starts
trained_model = train_linear_regression_model()

@app.route('/predict', methods=['POST'])
def predict_recovery():
    try:
        # Read the testing data from Google Sheets
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('iot-fracture-recovery-32774b3e943d.json', scope)
        client = gspread.authorize(credentials)
        test_sheet = client.open('Testing_data').sheet1  # Replace with your testing sheet name
        test_data = pd.DataFrame(test_sheet.get_all_records())

        # Extract the input features (X_test)
        X_test = test_data[['X_angle', 'Y_angle', 'Z_angle']]

        
        predicted_recovery_rate = trained_model.predict(X_test)

        
        total_recovery_rate = predicted_recovery_rate.mean()

        return jsonify({'predicted_recovery_rate': total_recovery_rate})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    train_linear_regression_model()
    
    app.run(debug=True)

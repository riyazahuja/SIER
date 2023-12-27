import numpy as np
import pandas as pd
import joblib
from keras.models import load_model
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import json
# Load the model and scalers
model = load_model('../tech_model.keras')
scaler_features = joblib.load('../scaler_features.pkl')
scaler_target = joblib.load('../scaler_target.pkl')


# Prepare the sequence data
def create_sequences(input_data, target_data, window_size):
    X, y = [], []
    for i in range(window_size, len(input_data)):
        X.append(input_data[i-window_size:i])  # Get the past 'window_size' days
        y.append(target_data[i, 0])  # Predict the next 'close' value
    return np.array(X), np.array(y)


# Load the same dataset used for training
# Preprocess the dataset identically to how it was done in the training script

f = open('../../data/processed/AAPL_data.json')
data_json = json.load(f)
IBM_data = data_json['AAPL']
f.close()


df = pd.DataFrame(IBM_data)
df= df.T 


scaled_features = scaler_features.fit_transform(df)
scaled_target = scaler_target.fit_transform(df[['close']])


# Recreate the sequences for the test set
# Remember to use the same 'window_size' as in the training

window_size = 60  # Use last 60 days of data to predict the next day
X, y = create_sequences(scaled_features, scaled_target, window_size)
# Train-test split
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]




# Use the model to predict the test set
predicted_stock_price = model.predict(X_test)

# Inverse transform the predicted 'close' prices and the actual 'close' prices
predicted_stock_price = scaler_target.inverse_transform(predicted_stock_price)
actual_prices = scaler_target.inverse_transform(y_test.reshape(-1, 1))

# Calculate RMSE for evaluation
rmse = sqrt(mean_squared_error(actual_prices, predicted_stock_price))
print(f"Test RMSE: {rmse}")

# Plot the results for visualization
plt.figure(figsize=(15, 5))
plt.plot(actual_prices, label='Actual Prices')
plt.plot(predicted_stock_price, label='Predicted Prices', alpha=0.7)
plt.title('Actual vs Predicted Stock Prices')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import json
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import joblib


f = open('../../data/processed/IBM_data.json')
data_json = json.load(f)
IBM_data = data_json['IBM']
f.close()


df = pd.DataFrame(IBM_data)
df= df.T  



# Initialize a scaler for the features
scaler_features = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler_features.fit_transform(df)

# Separate the target feature (close price) and scale it
scaler_target = MinMaxScaler(feature_range=(0, 1))
scaled_target = scaler_target.fit_transform(df[['close']])

# Prepare the sequence data
def create_sequences(input_data, target_data, window_size):
    X, y = [], []
    for i in range(window_size, len(input_data)):
        X.append(input_data[i-window_size:i])  # Get the past 'window_size' days
        y.append(target_data[i, 0])  # Predict the next 'close' value
    return np.array(X), np.array(y)

window_size = 60  # Use last 60 days of data to predict the next day
X, y = create_sequences(scaled_features, scaled_target, window_size)

# Train-test split
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Build LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))  # Output layer predicts the 'close' price

# Compile and fit model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))


model.save('../tech_model.keras')


joblib.dump(scaler_features, '../scaler_features.pkl')
joblib.dump(scaler_target, '../scaler_target.pkl')



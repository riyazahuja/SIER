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


df1 = pd.DataFrame(IBM_data)
df1= df1.T

f = open('../../data/processed/AAPL_data.json')
data_json = json.load(f)
AAPL_data = data_json['AAPL']
f.close()


df2 = pd.DataFrame(AAPL_data)
df2= df2.T

df1 = df1.reset_index().rename(columns={'index': 'Date'})
df2 = df2.reset_index().rename(columns={'index': 'Date'})

df1['Symbol'] = 'IBM'
df2['Symbol'] = 'AAPL'

df = pd.concat([df1, df2], axis=0)
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace=True)
df.reset_index(drop=True, inplace=True)


numeric_features = df.drop(columns=['Symbol','Date']).columns


# Initialize scalers for the features and target
scaler_features = MinMaxScaler(feature_range=(0, 1))
scaler_target = MinMaxScaler(feature_range=(0, 1))

scaled_features = scaler_features.fit_transform(df[numeric_features])
scaled_target = scaler_target.fit_transform(df[['close']])

# Function to create sequences, ensuring data consistency within each stock

def create_sequences(input_data, target_data, symbols, window_size):
    X, y = [], []
    unique_symbols = np.unique(symbols)  # Get unique stock symbols

    for symbol in unique_symbols:
        symbol_indices = np.where(symbols == symbol)[0]  # Get indices for each stock
        symbol_data = input_data[symbol_indices]
        symbol_target = target_data[symbol_indices]

        # Create sequences for each stock separately
        for i in range(window_size, len(symbol_data)):
            # Extract the sequence and corresponding target
            seq = symbol_data[i-window_size:i]
            target = symbol_target[i, 0]

            # Ensure sequence is for the same stock without mixing data across different stocks
            if len(np.unique(symbols[symbol_indices[i-window_size:i]])) == 1:
                X.append(seq)
                y.append(target)

    return np.array(X), np.array(y)


# Create sequences with symbol information
symbols = df['Symbol'].values
window_size = 60
X, y = create_sequences(scaled_features, scaled_target, symbols, window_size)

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
model.fit(X_train, y_train, epochs=25, batch_size=32, validation_data=(X_test, y_test))

# Save the model and scalers
model.save('../tech_model_combined.keras')
joblib.dump(scaler_features, '../scaler_features_combined.pkl')
joblib.dump(scaler_target, '../scaler_target_combined.pkl')



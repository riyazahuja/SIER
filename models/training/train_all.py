import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model
from keras.layers import Input, LSTM, Dense, RepeatVector, TimeDistributed
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import json
import joblib



tickers = ['IBM','AAPL']
dfs = []

for ticker in tickers:
    # Load data for a single ticker
    f = open(f'../../data/processed/{ticker}_data.json')  
    data_json = json.load(f)
    ticker_data = data_json[ticker]  # Replace TICKER with your actual ticker
    f.close()

    df = pd.DataFrame(ticker_data).T
    df = df.reset_index().rename(columns={'index': 'Date'})
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
#     df.reset_index(drop=True, inplace=True)
    df['Symbol'] = ticker

    #numeric_features = df.drop(columns=['Date','Symbol']).columns
    dfs.append(df)


df = pd.concat(dfs, axis=0)
#df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace=True)
df.reset_index(drop=True, inplace=True)
numeric_features = df.drop(columns=['Date','Symbol']).columns


# Initialize scalers for the features and target
scaler_features = MinMaxScaler(feature_range=(0, 1))
scaler_target = MinMaxScaler(feature_range=(0, 1))

scaled_features = scaler_features.fit_transform(df[numeric_features])
scaled_target = scaler_target.fit_transform(df[['close']])


def create_sequences(input_data, target_data, symbols, window_size, forecast_horizon):
    X, y = [], []
    unique_symbols = np.unique(symbols)  # Get unique stock symbols

    for symbol in unique_symbols:
        symbol_indices = np.where(symbols == symbol)[0]  # Get indices for each stock
        symbol_data = input_data[symbol_indices]
        symbol_target = target_data[symbol_indices]

        # Create sequences for each stock separately
        for i in range(window_size, len(symbol_data) - forecast_horizon + 1):
            X.append(symbol_data[i-window_size:i])
            y.append(symbol_target[i:i+forecast_horizon])

    return np.array(X), np.array(y)


symbols = df['Symbol'].values
window_size = 120
forecast_horizon = 30
X, y = create_sequences(scaled_features, scaled_target, symbols, window_size, forecast_horizon)

# Split data into training and test sets
split = int(0.9 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Define the seq2seq model architecture
encoder_inputs = Input(shape=(window_size, X.shape[2]))
encoder = LSTM(50, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
decoder_inputs = RepeatVector(forecast_horizon)(encoder_outputs)
decoder_lstm = LSTM(50, return_sequences=True)
decoder_outputs = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = TimeDistributed(Dense(1))
decoder_outputs = decoder_dense(decoder_outputs)

model = Model(encoder_inputs, decoder_outputs)

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Save the model and scalers
model.save('../lstm_model_all.keras')
joblib.dump(scaler_features, '../scaler_features_all.pkl')
joblib.dump(scaler_target, '../scaler_target_all.pkl')

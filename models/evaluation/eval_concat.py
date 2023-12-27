import numpy as np
import pandas as pd
import joblib
from keras.models import load_model
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import json
# Load the model and scalers
model = load_model('../tech_model_combined.keras')
scaler_features = joblib.load('../scaler_features_combined.pkl')
scaler_target = joblib.load('../scaler_target_combined.pkl')


# Prepare the sequence data
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


# Load the same dataset used for training
# Preprocess the dataset identically to how it was done in the training script

ticker = 'AAPL'

f = open(f'../../data/processed/{ticker}_data.json')
data_json = json.load(f)
data = data_json[ticker]
f.close()


df = pd.DataFrame(data)
df= df.T 
df = df.reset_index().rename(columns={'index': 'Date'})
df['Symbol'] = ticker
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace=True)
df.reset_index(drop=True, inplace=True)

symbols = np.array([ticker for _ in range(len(df))])


numeric_features = df.drop(columns=['Symbol','Date']).columns


scaled_features = scaler_features.fit_transform(df[numeric_features])
scaled_target = scaler_target.fit_transform(df[['close']])


# Recreate the sequences for the test set
# Remember to use the same 'window_size' as in the training

window_size = 60  # Use last 60 days of data to predict the next day
X, y = create_sequences(scaled_features, scaled_target, symbols, window_size)
# Train-test split
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]




# Use the model to predict the test set
#predicted_stock_price = model.predict(X_test)
predicted_stock_price = model.predict(X)

# Inverse transform the predicted 'close' prices and the actual 'close' prices
predicted_stock_price = scaler_target.inverse_transform(predicted_stock_price)
#actual_prices = scaler_target.inverse_transform(y_test.reshape(-1, 1))
actual_prices = scaler_target.inverse_transform(y.reshape(-1, 1))

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

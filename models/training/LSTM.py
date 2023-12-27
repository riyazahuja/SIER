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

# Transpose the DataFrame so that dates are rows and indicators are columns
df= df.T  # or d = d.transpose()


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



# Predictions
predicted_stock_price = model.predict(X_test)

# Since we are predicting 'close' values, we only inverse transform the predictions
predicted_stock_price = predicted_stock_price.reshape(-1, 1)
predicted_stock_price = scaler_target.inverse_transform(predicted_stock_price)  # Only for 'close' values
print(predicted_stock_price)







'''
# Assuming 'data' is a pandas DataFrame containing your time series and technical indicators
# Prepare the sequence data
def create_sequences(data, window_size):
    sequences = []
    for i in range(window_size, len(data)):
        # Use values to ensure you're working with numpy arrays
        sequences.append(data[i-window_size:i])  
    return np.array(sequences)

window_size = 60  # Use last 60 days of data to predict the next day
scaler = MinMaxScaler(feature_range=(0, 1))

# Assuming 'df' is your DataFrame and 'close' is the column you want to predict
scaled_data = scaler.fit_transform(df)
X = create_sequences(scaled_data, window_size)
y = scaled_data[window_size:]

# Train-test split
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Build LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# Compile and fit model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

# Predictions
predicted_stock_price = model.predict(X_test)
predicted_stock_price = scaler.inverse_transform(predicted_stock_price)  # Inverse scaling

# Evaluate model
# ... (use metrics like RMSE, or financial performance metrics)


rmse = sqrt(mean_squared_error(y_test, predicted_stock_price))
print("Test RMSE: ", rmse)



# Plotting the results
plt.figure(figsize=(10,6))
plt.plot(df['date'][-len(y_test):], scaler.inverse_transform(y_test.reshape(-1,1)), color='red', label='Real IBM Stock Price')
plt.plot(df['date'][-len(y_test):], predicted_stock_price, color='blue', label='Predicted IBM Stock Price')
plt.xticks(np.arange(0,y_test.shape[0],50), rotation=45)
plt.title('IBM Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('IBM Stock Price')
plt.legend()
plt.show()

'''
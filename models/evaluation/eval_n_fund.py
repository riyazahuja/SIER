import joblib
from keras.models import load_model
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json


# Load the model and scalers
model = load_model('../lstm_model_fund.keras')
scaler_features = joblib.load('../scaler_features_fund.pkl')
scaler_target = joblib.load('../scaler_target_fund.pkl')

ticker = 'IBM'

# Load data for a single ticker
f = open(f'../../data/processed/{ticker}_data_fund.json')  
data_json = json.load(f)
ticker_data = data_json[ticker]  # Replace TICKER with your actual ticker
f.close()

df = pd.DataFrame(ticker_data).T
df = df.reset_index().rename(columns={'index': 'Date'})
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace=True)
df.reset_index(drop=True, inplace=True)

numeric_features = df.drop(columns=['Date']).columns

scaled_features = scaler_features.fit_transform(df[numeric_features])
scaled_target = scaler_target.fit_transform(df[['close']])

# Create sequences for single ticker
def create_sequences(input_data, target_data, window_size, forecast_horizon):
    X, y = [], []
    for i in range(window_size, len(input_data) - forecast_horizon + 1):
        X.append(input_data[i-window_size:i])
        y.append(target_data[i:i+forecast_horizon])
    return np.array(X), np.array(y)

window_size = 120
forecast_horizon = 30

def predict(start_date):

    
    X, y = create_sequences(scaled_features, scaled_target, window_size, forecast_horizon)

    # Split data into training and test sets
    split = int(0.9 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]





    # Set your forecast start date
    #start_date = '2023-10-01'  # Replace with your actual start date

    if (type(start_date) == str):
        dt = pd.to_datetime(start_date)
    else:
        dt = start_date

    #print(f'{dt}:{type(dt)}')
    #print(df['Date'])
    while(len(df.index[df['Date'] == dt].tolist()) == 0):
        dt = dt + pd.Timedelta(1, unit='d')


    start_date= dt


    # Find the index of the start date
    start_idx = df.index[df['Date'] == pd.to_datetime(start_date)].tolist()[0]

    # Prepare the input sequence for the model
    input_sequence = scaled_features[start_idx - window_size:start_idx]
    input_sequence = input_sequence.reshape((1, window_size, -1))

    # Predict the next 30 days
    predicted_prices_scaled = model.predict(input_sequence)
    #print(predicted_prices_scaled.shape)
    #print(predicted_prices_scaled)

    # Inverse transform the predicted scaled prices to the original price scale
    predicted_prices = scaler_target.inverse_transform(predicted_prices_scaled.reshape(-1, 1)).reshape(-1, forecast_horizon)
    predicted_prices=predicted_prices.flatten()




# print('PREDICTED PRICES:')
# print(predicted_prices.shape)
# print(predicted_prices)


# Extract the actual prices for the same 30-day period
    actual_prices_scaled = scaled_target[start_idx:start_idx + forecast_horizon]
    actual_prices = scaler_target.inverse_transform(actual_prices_scaled)
# print('\nACTUAL PRICES:')
# print(actual_prices.shape)
# print(actual_prices)


    actual_prices=actual_prices.flatten()
    rmse = np.sqrt(mean_squared_error(actual_prices, predicted_prices))
    dates_full = pd.to_datetime(df['Date'])
    forecast_dates = dates_full[start_idx:start_idx + forecast_horizon]

    return (forecast_dates, predicted_prices, rmse)
    


dates_full = pd.to_datetime(df['Date'])
days = [dates_full[i] for i in range(window_size, len(dates_full)-forecast_horizon) if (i % (forecast_horizon // 3) == 0)]
#print(days)
#days = ['2023-10-02','2023-11-01']
# print('\nFLATTEN\n')
# print(predicted_prices)
# print(actual_prices)

actual_prices_full_scaled = scaled_target
actual_prices_full = scaler_target.inverse_transform(actual_prices_full_scaled)

# forecast_dates = dates_full[start_idx:start_idx + forecast_horizon]

# # Calculate RMSE for the 30-day forecast
# rmse = np.sqrt(mean_squared_error(actual_prices, predicted_prices))
# print(f'RMSE for the {forecast_horizon}-day forecast:', rmse)

# Visualize the results

def visualize(dates_full, actual_prices_full, predictions):

    rmses = [x for _,_,x in predictions]
    print(f'Average RMSE for the {forecast_horizon}-day forecast:', sum(rmses)/len(rmses))


    plt.figure(figsize=(15, 7))
    plt.plot(dates_full,actual_prices_full, label='Actual Prices', color='blue')
    f0, p0, _ = predictions[0]
    plt.plot(f0,p0, label='Predicted Prices', color='red')
    for forecast_dates, predicted_prices, _ in predictions:
        plt.plot(forecast_dates,predicted_prices, color='red')
    plt.title(f'Actual vs Predicted Stock Prices for the next {forecast_horizon} days')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


predictions = [predict(day) for day in days]

visualize(dates_full,actual_prices_full, predictions)
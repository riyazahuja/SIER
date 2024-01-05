import joblib
from keras.models import load_model
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import sys
from datetime import datetime, timedelta
import os

# Create sequences for single ticker
def create_sequences(input_data, target_data, window_size, forecast_horizon):
    X, y = [], []
    for i in range(window_size, len(input_data) - forecast_horizon + 1):
        X.append(input_data[i-window_size:i])
        y.append(target_data[i:i+forecast_horizon])
    return np.array(X), np.array(y)


def load(ticker, window_size, forecast_horizon, root_path):
    
    model_path = os.path.join(root_path, f'models/bin/{ticker}/{forecast_horizon}f_{window_size}w_model.keras')
    feat_path = os.path.join(root_path, f'models/bin/{ticker}/{forecast_horizon}f_{window_size}w_scaler_features.pkl')
    target_path = os.path.join(root_path, f'models/bin/{ticker}/{forecast_horizon}f_{window_size}w_scaler_target.pkl')

    model = load_model(model_path)
    scaler_features = joblib.load(feat_path)
    scaler_target = joblib.load(target_path)

    #model = load_model(f'../bin/{ticker}/{forecast_horizon}f_{window_size}w_model.keras')
    #scaler_features = joblib.load(f'/models/bin/{ticker}/{forecast_horizon}f_{window_size}w_scaler_features.pkl')
    #scaler_target = joblib.load(f'/models/bin/{ticker}/{forecast_horizon}f_{window_size}w_scaler_target.pkl')
    return (model, scaler_features, scaler_target)


def calculate_rmspe(y_true, y_pred):
    # Ensure no zero denominators; add a small value, epsilon, to avoid division by zero errors.
    epsilon = 1e-10
    # Calculate percentage errors
    percentage_errors = ((y_true - y_pred) / (y_true + epsilon)) ** 2
    # Calculate mean of percentage errors
    mean_percentage_error = np.mean(percentage_errors)
    # Return RMSPE
    return np.sqrt(mean_percentage_error) * 100



def predict(ticker, window_size, forecast_horizon, start_date, cached_model, root_path):


    # Load the model and scalers
    #model = load_model(f'../bin/{ticker}/{forecast_horizon}f_{window_size}w_model.keras')
    #scaler_features = joblib.load(f'../bin/{ticker}/{forecast_horizon}f_{window_size}w_scaler_features.pkl')
    #scaler_target = joblib.load(f'../bin/{ticker}/{forecast_horizon}f_{window_size}w_scaler_target.pkl')

    model, scaler_features, scaler_target = cached_model

    # Load data for a single ticker
    data_path = os.path.join(root_path, f'data/processed/data.json')
    f = open(data_path)  
    data_json = json.load(f)
    ticker_data = data_json[ticker]['Time Series (Daily)']  # Replace TICKER with your actual ticker
    f.close()

    df = pd.DataFrame(ticker_data).T
    df = df.reset_index().rename(columns={'index': 'Date'})
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    numeric_features = df.drop(columns=['Date']).columns

    scaled_features = scaler_features.fit_transform(df[numeric_features])
    scaled_target = scaler_target.fit_transform(df[['close']])


    dates_full = pd.to_datetime(df['Date'])


    X, y = create_sequences(scaled_features, scaled_target, window_size, forecast_horizon)

    # Split data into training and test sets
    split = int(0.9 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    if (type(start_date) == str):
        dt = pd.to_datetime(start_date)
    else:
        dt = start_date


    #print(df['Date'])
    #print(dt)

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

    # Inverse transform the predicted scaled prices to the original price scale
    predicted_prices = scaler_target.inverse_transform(predicted_prices_scaled.reshape(-1, 1)).reshape(-1, forecast_horizon)
    predicted_prices=predicted_prices.flatten()


    actual_prices_scaled = scaled_target[start_idx:start_idx + forecast_horizon]
    actual_prices = scaler_target.inverse_transform(actual_prices_scaled)


    actual_prices_full_scaled = scaled_target
    actual_prices_full = scaler_target.inverse_transform(actual_prices_full_scaled)


    actual_prices=actual_prices.flatten()
    rmse = np.sqrt(mean_squared_error(actual_prices, predicted_prices))
    rmspe = calculate_rmspe(actual_prices, predicted_prices)

    dates_full = pd.to_datetime(df['Date'])
    forecast_dates = dates_full[start_idx:start_idx + forecast_horizon]


    return {
        'ticker': ticker,
        'window_size': window_size,
        'forecast_horizon': forecast_horizon,
        'start_date': start_date,
        'predicted_prices' : predicted_prices,
        'forecast_dates': forecast_dates,
        'dates_full' : dates_full,
        'actual_prices': actual_prices,
        'actual_prices_full': actual_prices_full,        
        'rmse': rmse,
        'rmspe' : rmspe
    }


# Visualize the results

def visualize(predictions):

    rmses = [p['rmse'] for p in predictions]
    rmspes = [p['rmspe'] for p in predictions]

    print(f'Average RMSE:', sum(rmses)/len(rmses))
    print(f'Average RMSPE:', sum(rmspes)/len(rmspes))

    p0 = predictions[0]

    plt.figure(figsize=(15, 7))
    plt.plot(p0['dates_full'],p0['actual_prices_full'], label='Actual Prices', color='blue')
    plt.plot(p0['forecast_dates'],p0['predicted_prices'], label='Predicted Prices', color='red')
    for p in predictions:
        plt.plot(p['forecast_dates'],p['predicted_prices'], color='red')
    plt.title(f'Actual vs Predicted Stock Prices for the next {p["forecast_horizon"]} days')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()



def get_all_dates(ticker, forecast_horizon, window_size):
        cm = load(ticker, window_size, forecast_horizon, '../..')
        td = timedelta(days=5 * forecast_horizon)
        temp_dt = (datetime.today() - td).strftime(r'%Y-%m-%d')
        temp = predict(ticker, window_size, forecast_horizon, temp_dt,cm,'../..')
        dates_full = temp['dates_full']
        start_dates = [dates_full[i] for i in range(window_size, len(dates_full)-forecast_horizon) if (i % (forecast_horizon // 3) == 0)]
        return start_dates
    

if __name__ == '__main__':
    ticker = sys.argv[1]
    forecast_horizon = int(sys.argv[2])
    window_size = 4 * forecast_horizon
    if len(sys.argv) > 3 and sys.argv[3].isnumeric():
        window_size = int(sys.argv[3])
        if len(sys.argv) > 4:
            start_dates = sys.argv[4:]
        else:
            start_dates = get_all_dates(ticker, forecast_horizon, window_size)
    elif len(sys.argv) > 3:
        start_dates = sys.argv[3:]
    else:
        start_dates = get_all_dates(ticker, forecast_horizon, window_size)

    cached_model = load(ticker, window_size, forecast_horizon,'../..')
    
    predictions = [predict(ticker, window_size, forecast_horizon, date, cached_model, '../..') for date in start_dates]
    visualize(predictions)

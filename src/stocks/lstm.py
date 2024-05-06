from ...models.evaluation.predict import load, predict


def run_prediction(ticker, window_size, forecast_horizon, start_date):
    root_path = '..'
    cm = load(ticker, window_size, forecast_horizon,root_path)
    predictions = predict(ticker, window_size, forecast_horizon, start_date, cm, root_path)

    return predictions
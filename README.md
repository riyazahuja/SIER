# SIER

## Introduction
Welcome to SIER, a cutting-edge platform designed to revolutionize the way individuals and small institutions engage with the financial markets. Utilizing advanced AI and machine learning techniques, SIER aims to provide personalized, accurate, and intuitive financial forecasting and portfolio management.

## Project Goals
SIER aims to:

- **Democratize Financial Forecasting**: Make advanced financial analysis tools accessible to a broader audience, beyond big institutions.
- **Personalize Investment Strategies**: Offer customizable strategies that match the user's risk profile, investment goals, and preferences.
- **Incorporate Alternative Data**: Leverage non-traditional data sources for more comprehensive and unique market insights.
- **Promote Ethical Investing**: Provide options for users interested in ESG and sustainable investing.
- **Ensure Transparency**: Make AI decisions understandable and transparent, building trust and knowledge among users.
- **Foster a Collaborative Community**: Create a space where users can learn from and collaborate with each other.
- **Adapt and Innovate**: Continuously improve and innovate the platform based on user feedback and market changes.

## Overview
SIER is a cutting-edge stock prediction system that utilizes an attention-based seq2seq LSTM model with LIME to offer transparent and understandable investment predictions. This system is designed to provide users with highly accurate short to medium term financial forecasts, aiding in more informed investment decisions.

## Features
- **Pre-loaded Data**: Includes data for 5 stock tickers as standard, each with 5 years of historical information.
- **Prediction Horizons**: Capable of generating forecasts over 7, 30, and 90 days.
- **Accuracy**: Delivers predictions with historical RMSPE accuracies of 96%, 93%, and 90% for 7, 30, and 90 day forecasts, respectively.
- **API Integration**: Easily connects to larger datasets through financial data APIs for extended analysis.
- **Transparent Predictions**: Utilizes LIME to explain the factors influencing each prediction, enhancing user trust and understanding.

## Installation

- Clone the repository:
    ```bash
    git clone <repository-url>
    ```

- Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Evaluating Predictions
To evaluate the stock predictions, run:
    ```
    python models/evaluation/predict.py <TICKER> <Forecast Horizon> <Window Size>
    ```

### Running the Web Application
To launch the full Django website:
    ```
    python manage.py runserver
    ```

## Directory Structure
Outlined below is the key directory structure of the SIER project:
- `/stocks`: Contains the models and views for stock prediction management.
- `/models`: Includes model definitions and training/evaluation scripts.
- `/templates`: Houses Django templates for the web interface.
- `/static`: Stores CSS files for the web styling.
- `/data`: Consists of scripts and JSON data for stocks.

## License
Specify your license or if the project is open-sourced, provide details here.


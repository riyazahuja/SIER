import json
from datetime import datetime, timedelta

'''
GOAL:

TODO: ADD OPEN,LOW,HIGH,etc
{IBM:
    {
    Fundamentals: {
        news_sentiment: [(relevance, sentiment), (relavence, sentiment), ...],
        "PERatio": "20.92",
        "PEGRatio": "0.429",
        "BookValue": "25.28",
        "DividendPerShare": "6.62",
        "DividendYield": "0.041",
        "EPS": "7.75",
        "RevenuePerShareTTM": "67.3",
        "ProfitMargin": "0.113",
        "OperatingMarginTTM": "0.145",
        "ReturnOnAssetsTTM": "0.0455",
        "ReturnOnEquityTTM": "0.328",
        "DilutedEPSTTM": "7.75",
        "QuarterlyEarningsGrowthYOY": "0.126",
        "QuarterlyRevenueGrowthYOY": "0.046",
        "TrailingPE": "20.92",
        "ForwardPE": "16.1",
        "PriceToSalesRatioTTM": "2.389",
        "PriceToBookRatio": "6.33",
        "EVToRevenue": "3.166",
        "EVToEBITDA": "13.7",
        "Beta": "0.772",
        "52WeekHigh": "166.34",
        "52WeekLow": "117.38",
        "50DayMovingAverage": "151.83",
        "200DayMovingAverage": "139.26",


        last 4 quarterly earnings (delta)

        last 4 quarterly income (delta)

        last 4 q cashflow (delta)

        last 4 q balance (delta)

    },

    Time Series: {
        "2023-12-22": {
            "close": "4.0500",
            "volume": "4200",
            ADX
            BBAND
            MACD
            OBV
            RSI
        },
    
    ...
    }


}

'''

def interpolate(data):
    sorted_dates = sorted(data.keys(), key=lambda x: datetime.strptime(x, r"%Y-%m-%d"), reverse=True)
    return fill_daily_data(sorted_dates,data)


def fill_daily_data(sorted_dates, weekly_data):
    daily_data = {}
    for i in range(len(sorted_dates)-1):
        start_date = datetime.strptime(sorted_dates[i], r"%Y-%m-%d")
        end_date = datetime.strptime(sorted_dates[i+1], r"%Y-%m-%d")
        delta = start_date - end_date

        # Filling in the days with the value of the start date
        for j in range(delta.days):
            current_date = (start_date - timedelta(days=j)).strftime(r"%Y-%m-%d")
            daily_data[current_date] = weekly_data[sorted_dates[i]]

    # Adding the last known value for the earliest date in the input
    earliest_date = datetime.strptime(sorted_dates[-1], r"%Y-%m-%d")
    daily_data[earliest_date.strftime(r"%Y-%m-%d")] = weekly_data[sorted_dates[-1]]

    return daily_data

ticker = 'IBM'

price_f = open(f'../raw/downloads/{ticker}_full_raw.json')
#overview_f = open(f'../raw/downloads/{ticker}_overview.json')
#news_f= open(f'../raw/downloads/{ticker}_news.json')
earnings_f= open(f'../raw/downloads/{ticker}_earnings.json')
cash_f =  open(f'../raw/downloads/{ticker}_cashflow.json')
balance_f = open(f'../raw/downloads/{ticker}_balance.json')

ADX_f= open(f'../raw/downloads/tech/{ticker}_ADX.json')
BBAND_f= open(f'../raw/downloads/tech/{ticker}_BBAND.json')
MACD_f= open(f'../raw/downloads/tech/{ticker}_EMA.json') #CHANGE BACK TO MACD WHEN PREMIUM
OBV_f= open(f'../raw/downloads/tech/{ticker}_OBV.json')
RSI_f= open(f'../raw/downloads/tech/{ticker}_RSI.json')

price = json.load(price_f)
#overview = json.load(overview_f)
#news= json.load(news_f)
earnings = json.load(earnings_f)
cash = json.load(cash_f)
balance = json.load(balance_f)
ADX = json.load(ADX_f)
BBAND = json.load(BBAND_f)
MACD = json.load(MACD_f)
OBV = json.load(OBV_f)
RSI = json.load(RSI_f)

price_f.close()
#overview_f.close()
#news_f.close()
earnings_f.close()
cash_f.close()
balance_f.close()
ADX_f.close()
BBAND_f.close()
MACD_f.close()
OBV_f.close()
RSI_f.close()




#TODO IMPLEMENT FUNDAMENTALS INTO MULTI-INPUT MODEL
#fundamenals = dict()
#fundamenals['news_sentiment']
#...



time_series_daily = dict()

price = price[ticker]
ADX = ADX['Technical Analysis: ADX']
#MACD = MACD['Technical Analysis: MACD']
MACD = MACD['Technical Analysis: EMA']

BBAND = BBAND['Technical Analysis: BBANDS']
OBV = OBV['Technical Analysis: OBV']
RSI = RSI['Technical Analysis: RSI']

cash = cash['quarterlyReports']
earnings = earnings['quarterlyReports']
balance = balance['quarterlyReports']

#price = interpolate(price)
ADX = interpolate(ADX)
MACD = interpolate(MACD)
BBAND = interpolate(BBAND)
OBV = interpolate(OBV)
RSI = interpolate(RSI)



#TECHNICAL ANALYSIS

for date, pd in price.items():
    entry = dict()
    
    for dt, d in pd.items():
        entry[dt] = float(d)

    try:
        metrics = [ADX[date],MACD[date],BBAND[date],OBV[date],RSI[date]]
        #metrics = [ADX[date],BBAND[date],OBV[date],RSI[date]]
    except KeyError:
        continue


    for metric in metrics:
        for k, v in metric.items():
            entry[k] = float(v)
    
    time_series_daily[date] = entry


#FUNDAMENTAL ANALYSIS




result = {ticker : time_series_daily}

out_file = open(f"../processed/{ticker}_data.json", "w") 

json.dump(result, out_file, indent = 6) 
out_file.close() 
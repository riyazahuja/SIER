import json
from datetime import datetime, timedelta
import pandas as pd
import sys


def interpolate(data, convert = False, flag = None):

    if convert:
        assert (type(data) == list)

        temp = {}

        for d in data:
            if 'fiscalDateEnding' not in d.keys():
                raise KeyError('Invalid json data')
            date = d['fiscalDateEnding']
            entry = {}
            for k,v in d.items():
                if(k!= 'fiscalDateEnding' and k!= 'reportedCurrency'):
                    try:
                        entry[k] = float(v)
                    except:
                        continue
            temp[date] = entry
        
        data = temp
    

    sorted_dates = sorted(data.keys(), key=lambda x: datetime.strptime(x, r"%Y-%m-%d"), reverse=True)
    return fill_daily_data(sorted_dates,data, flag)


def fill_daily_data(sorted_dates, sparse_data, flag=None):
    daily_data = {}
    current_value = None

    # Iterate through all possible dates in the range
    all_dates = pd.date_range(start=sorted_dates[-1], end=sorted_dates[0], freq='D').strftime('%Y-%m-%d')

    # Initialize the data with the values from the latest report
    for date in all_dates:
        if date in sparse_data:
            current_value = sparse_data[date]  # Update the current value to the new report
            if flag:
                current_value[flag] = 1  # Set flag as 1 for the new report date
        else:
            if current_value and flag:
                # Copy the current value to prevent modifying the original report data
                current_value = current_value.copy()  
                current_value[flag] = 0  # Set flag as 0 for non-report dates

        if current_value:
            daily_data[date] = current_value  # Assign the current value

    return daily_data



def trim_fund(cash,earnings,balance):
    fund = {}
    '''
    ReportedEPS": "2.2", // Most recent quarterly value, carry forward until new EPS is reported
    "SurprisePercentage": "3.2864", // Most recent quarterly value
    "OperatingCashflow": 3056000000, // Most recent quarterly value
    "FreeCashFlow": 2776000000, // Most recent quarterly value (OperatingCashflow - CapitalExpenditures)
    "TotalAssets": 129321000000, // Most recent quarterly value
    "TotalLiabilities": 106165000000, // Most recent quarterly value
    "CurrentRatio": 0.9, // Most recent quarterly value (TotalCurrentAssets/TotalCurrentLiabilities)
    "DebtToEquityRatio": 0.8 // Most recent quarterly value (TotalLiabilities/TotalShareholderEquity)
    "EPSChangePercentQoQ": 4.5, // EPS percentage change quarter over quarter
    "RevenueChangePercentYoY": 3.2, // Revenue percentage change year over year
    "TotalAssetsChangePercentQoQ": 2.1,
    '''

    for date in cash.keys():
        
        c = cash[date]
        e = earnings[date]
        b = balance[date]
        dt = datetime.strptime(date, r'%Y-%m-%d')
        delta = timedelta(days = 1)
        
        ct = dt
        et = dt
        bt = dt
        

        while (cash[ct.strftime(r"%Y-%m-%d")]['NewCashflowStatement'] != 1):
            ct = ct - delta
        while (earnings[et.strftime(r"%Y-%m-%d")]['NewEarningsReport'] != 1):
            et = et - delta
        while (balance[bt.strftime(r"%Y-%m-%d")]['NewBalanceSheet'] != 1):
            bt = bt - delta


        pd = ct if ct < et else (et if et < bt else bt)
        pd = pd-delta
        prev_date = pd.strftime(r"%Y-%m-%d")

        if prev_date not in cash.keys():
            EPSChangePercent = 1
            cashflowChangePercent = 1
            totalAssetsChangePercent = 1
        else:
            
            c_prev=cash[prev_date]
            e_prev=earnings[prev_date]
            b_prev=balance[prev_date]

            EPSChangePercent = (e['reportedEPS'] - e_prev['reportedEPS'])/(e_prev['reportedEPS']) 
            cashflowChangePercent = (c['operatingCashflow'] - c_prev['operatingCashflow']) / (c_prev['operatingCashflow'])
            totalAssetsChangePercent = (b['totalAssets'] - b_prev['totalAssets']) / (b_prev['totalAssets'])


        reportedEPS = e['reportedEPS']
        surprisePercentage = e['surprisePercentage']
        operatingCashflow = c['operatingCashflow']
        freeCashflow = c['operatingCashflow'] - c['capitalExpenditures']
        totalAssets = b['totalAssets']
        totalLiabilities = b['totalLiabilities']
        currentRatio = b['totalCurrentAssets'] / b['totalCurrentLiabilities']
        debtToEquityRatio = b['totalLiabilities'] / b['totalShareholderEquity']
        

        entry = {
            'reportedEPS': reportedEPS,
            'surprisePercentage': surprisePercentage,
            'operatingCashflow' : operatingCashflow,
            'freeCashflow' : freeCashflow,
            'totalAssets' : totalAssets,
            'totalLiabilities' : totalLiabilities,
            'currentRatio' : currentRatio,
            'debtToEquityRatio' : debtToEquityRatio,
            'EPSChangePercent' : EPSChangePercent,
            'cashflowChangePercent' : cashflowChangePercent,
            'totalAssetsChangePercent' : totalAssetsChangePercent,
            'newCashflowStatement' : c['NewCashflowStatement'],
            'newEarningsReport' : e['NewEarningsReport'],
            'newBalanceSheet' : b['NewBalanceSheet']

        }

        fund[date]= entry
    return fund


def parse(tickers):
    for ticker in tickers:

        price_f = open(f'../raw/{ticker}/{ticker}_prices.json')

        earnings_f= open(f'../raw/{ticker}/{ticker}_earnings.json')
        cash_f =  open(f'../raw/{ticker}/{ticker}_cashflow.json')
        balance_f = open(f'../raw/{ticker}/{ticker}_balance.json')

        ADX_f= open(f'../raw/{ticker}/{ticker}_ADX.json')
        BBAND_f= open(f'../raw/{ticker}/{ticker}_BBAND.json')
        MACD_f= open(f'../raw/{ticker}/{ticker}_EMA.json') #CHANGE BACK TO MACD WHEN PREMIUM
        OBV_f= open(f'../raw/{ticker}/{ticker}_OBV.json')
        RSI_f= open(f'../raw/{ticker}/{ticker}_RSI.json')

        price = json.load(price_f)
        earnings = json.load(earnings_f)
        cash = json.load(cash_f)
        balance = json.load(balance_f)
        ADX = json.load(ADX_f)
        BBAND = json.load(BBAND_f)
        MACD = json.load(MACD_f)
        OBV = json.load(OBV_f)
        RSI = json.load(RSI_f)

        price_f.close()
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

        price = price['Time Series (Daily)']

        ADX = ADX['Technical Analysis: ADX']
        #MACD = MACD['Technical Analysis: MACD']
        MACD = MACD['Technical Analysis: EMA']

        BBAND = BBAND['Technical Analysis: BBANDS']
        OBV = OBV['Technical Analysis: OBV']
        RSI = RSI['Technical Analysis: RSI']

        cash = cash['quarterlyReports']
        earnings = earnings['quarterlyEarnings']
        balance = balance['quarterlyReports']

        #price = interpolate(price)
        ADX = interpolate(ADX)
        MACD = interpolate(MACD)
        BBAND = interpolate(BBAND)
        OBV = interpolate(OBV)
        RSI = interpolate(RSI)

        cash = interpolate(cash, convert = True, flag = 'NewCashflowStatement')
        earnings = interpolate(earnings, convert = True, flag = 'NewEarningsReport')
        balance = interpolate(balance, convert = True, flag = 'NewBalanceSheet')



        funds = trim_fund(cash,earnings,balance)

        for date, pd in price.items():
            entry = dict()
            
            for dt, d in pd.items():
            
                entry[dt] = float(d)

            try:
                metrics = [ADX[date],MACD[date],BBAND[date],OBV[date],RSI[date],funds[date]]
            except KeyError:
                continue


            for metric in metrics:
                for k, v in metric.items():
                    entry[k] = float(v)
            
            time_series_daily[date] = entry

        result = time_series_daily

        out_file = open(f"../processed/{ticker}_data.json", "w") 

        json.dump(result, out_file, indent = 6) 
        out_file.close() 


def merge(tickers):
    all_data = {}
    for ticker in tickers:
        f = open(f'../processed/{ticker}_data.json')
        all_data[ticker] = json.load(f)
        f.close()
    
    out_file = open(f"../processed/data.json", "w") 

    json.dump(all_data, out_file, indent = 6) 
    out_file.close() 


if __name__== '__main__':
    tickers = sys.argv[1:]
    parse(tickers)
    merge(tickers)


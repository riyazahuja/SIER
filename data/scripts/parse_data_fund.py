import json
from datetime import datetime, timedelta
import pandas as pd

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

'''
def fill_daily_data(sorted_dates, sparse_data, flag="rm"):
    daily_data = {}
    # Iterate over all dates and initially set the flag to 0
    all_dates = pd.date_range(start=sorted_dates[-1], end=sorted_dates[0], freq='D').strftime('%Y-%m-%d')
    for date in all_dates:
        daily_data[date] = {**sparse_data[sorted_dates[-1]], flag: 0}  # Use the earliest date as the base and set flag to 0

    # Now iterate through the sorted dates to carry forward the data and set flag to 1 on report dates
    for i in range(len(sorted_dates)):
        report_date = sorted_dates[i]
        for k in sparse_data[report_date]:
            if k != flag:  # Don't carry forward the flag, only the data
                for date in daily_data:
                    daily_data[date][k] = sparse_data[report_date][k]

        # On the actual report date, set the flag to 1
        daily_data[report_date][flag] = 1

    return daily_data
'''


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
        #print(f'\n{date} : {e["reportedEPS"]}\n')
        dt = datetime.strptime(date, r'%Y-%m-%d')
        delta = timedelta(days = 1)
        
        ct = dt
        et = dt
        bt = dt
        

        while (cash[ct.strftime(r"%Y-%m-%d")]['NewCashflowStatement'] != 1):
            ct = ct - delta
            #print(f'\t\tct={ct.strftime(r"%Y-%m-%d")} : {cash[ct.strftime(r"%Y-%m-%d")]["NewCashflowStatement"]}')
        while (earnings[et.strftime(r"%Y-%m-%d")]['NewEarningsReport'] != 1):
            et = et - delta
        while (balance[bt.strftime(r"%Y-%m-%d")]['NewBalanceSheet'] != 1):
            bt = bt - delta

        # print(f'\tct:{ct}')
        # print(f'\tet:{et}')
        # print(f'\tbt:{bt}')

        pd = ct if ct < et else (et if et < bt else bt)
        pd = pd-delta
        prev_date = pd.strftime(r"%Y-%m-%d")
        #print(f'{date} : {prev_date}')
        if prev_date not in cash.keys():
            #print('\tNOT IN')
            #print(cash.keys())
            #print(prev_date)


            EPSChangePercent = 1
            cashflowChangePercent = 1
            totalAssetsChangePercent = 1
        else:
            
            c_prev=cash[prev_date]
            e_prev=earnings[prev_date]
            b_prev=balance[prev_date]
            #print(f'\tINNNNNNN: {e_prev["reportedEPS"]}\n\t\t {e["reportedEPS"]}')

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

        #print(f'\t\tDelta EPS : {EPSChangePercent}')

        fund[date]= entry
    return fund









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
earnings = earnings['quarterlyEarnings']
balance = balance['quarterlyReports']

#price = interpolate(price)
ADX = interpolate(ADX)
MACD = interpolate(MACD)
BBAND = interpolate(BBAND)
OBV = interpolate(OBV)
RSI = interpolate(RSI)

cash = interpolate(cash, convert = True, flag = 'NewCashflowStatement')

for k,v in cash.items():
    #print(f'{k}: NewCashflowStatement = {v["NewCashflowStatement"]}{"!!!!" if v["NewCashflowStatement"] == 1 else ""}')
    pass


earnings = interpolate(earnings, convert = True, flag = 'NewEarningsReport')
balance = interpolate(balance, convert = True, flag = 'NewBalanceSheet')



funds = trim_fund(cash,earnings,balance)

#TECHNICAL ANALYSIS

for date, pd in price.items():
    entry = dict()
    
    for dt, d in pd.items():
    
        entry[dt] = float(d)

    try:
        metrics = [ADX[date],MACD[date],BBAND[date],OBV[date],RSI[date],funds[date]]
        #metrics = [ADX[date],BBAND[date],OBV[date],RSI[date]]
    except KeyError:
        continue


    for metric in metrics:
        for k, v in metric.items():
            entry[k] = float(v)
    
    time_series_daily[date] = entry


#FUNDAMENTAL ANALYSIS




result = {ticker : time_series_daily}

out_file = open(f"../processed/{ticker}_data_fund.json", "w") 

json.dump(result, out_file, indent = 6) 
out_file.close() 
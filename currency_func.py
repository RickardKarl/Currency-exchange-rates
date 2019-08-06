"""
    Author: Rickard Karlsson
"""
import json
import pprint
import requests
import datetime
import pandas as pd
from dateutil.parser import parse
import numpy as np

"""
 Get today's date and initialize pprint
"""
pp = pprint.PrettyPrinter()
today_date = str(datetime.datetime.today()).split()[0]


__available_base_currencies = ['USD', 'GBP', 'EUR', 'JPY', 'CZK', 'DKK', 'HUF',
                        'PLN', 'SEK', 'CHF', 'NOK', 'AUD', 'CAD', 'HKD', 'KRW',
                        'NZD', 'SGD', 'ZAR']

__available_ref_currencies = ['USD', 'GBP', 'EUR', 'JPY', 'BGN', 'CZK', 'DKK', 'HUF', 'PLN',
                'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'HRK', 'RUB', 'TRY', 'AUD',
                'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN',
                'MYR', 'NZD', 'BHP', 'SGD', 'THB', 'ZAR']
"""
 Function which returns exchange rate for a curreny, with a another
 (compare) currency as reference
 start_date has to be given in the format YYYY-MM-DD
 end_date is optional, it will otherwise take the lattest available date

 Outputs:
 numpy array of available exchange rates
 list of dates for each exchange rate
"""
def request_exchange_rate(base_currency, ref_currency, start_date,
                            end_date = today_date):


    """
        Error handling of arguments
    """
    if type(base_currency) != str or type(ref_currency) != str:
        raise ValueError("base_currency or ref_currency are not string.")
    if len(base_currency) != 3 or len(ref_currency) != 3:
        raise ValueError("Invalid currency.")

    try:
        parse(start_date)
        parse(end_date)
    except ValueError as e:
        raise e("Invalid date format, should YYYY-MM-DD.")


    """
        Requesting data from API (https://exchangeratesapi.io/)
    """
    period = "start_at=" + start_date + "&end_at=" + end_date
    api_url = "https://api.exchangeratesapi.io/history?" + period
    api_url =  api_url + "&base=" + base_currency
    historic_exch_rate = requests.get(api_url).json()
    """
        Allocating available dates in the data for future reference
    """
    dates_in_data = {}
    for date in historic_exch_rate['rates']:
        dates_in_data[date] = True

    """
     Looping over the entire period and saving the wanted exchange rates
    """
    daterange = pd.date_range(start_date, end_date)
    exchange_rates = []
    exchange_dates = []
    print("Scanning the period ...")
    for date in daterange.date:
        if dates_in_data.get(str(date)) is True:
            exchange_rates.append(historic_exch_rate['rates'][str(date)][ref_currency])
            exchange_dates.append(pd.Timestamp(str(date)))
        else:
            pass
    print("Done!")



    print("Returned exchange rate for", ref_currency,"between", start_date, "and",
            end_date, "with", base_currency,"as base currency." )

    # Turn exchange_rates to numpy array
    exchange_rates = np.asarray(exchange_rates)
    exchange_dates = np.asarray(exchange_dates)
    return exchange_rates, exchange_dates

def get_latest_exchange_rate():
    return requests.get("https://api.exchangeratesapi.io/latest").json()

def get_available_base_currencies():
    return __available_base_currencies.copy()

def get_available_ref_currencies():
    return __available_ref_currencies.copy()

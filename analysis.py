import json
import pprint
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from currency_func import *
from currency_plot import *
import sys

base_currencies = get_available_base_currencies()
ref_currency = 'SEK'
base_currencies.remove(ref_currency)

exchange_rates = {} # Will contain tuple of exchange rate, dates
normalised_exchange_rates = {}
start_date = "2000-01-01"

for curr in base_currencies:
    exchange_rates[curr] = request_exchange_rate(curr,ref_currency, start_date)
    normalised = np.true_divide(exchange_rates.get(curr)[0],
                                np.max(exchange_rates.get(curr)[0]))
    normalised_exchange_rates[curr] = np.transpose(normalised)

plot_exchange_rate(exchange_rates.get('USD')[1], normalised_exchange_rates.get('USD'), 'USD',
                    ref_currency, plot_show = False)
plot_exchange_rate(exchange_rates.get('EUR')[1], normalised_exchange_rates.get('EUR'), 'EUR',
                    ref_currency, plot_show = False)
USD_EUR_SEK = np.array((exchange_rates.get('USD')[1],
                        normalised_exchange_rates.get('USD'),
                        normalised_exchange_rates.get('EUR')))
plt.show()

plt.plot(normalised_exchange_rates.get('USD'), normalised_exchange_rates.get('EUR'))
plt.plot(normalised_exchange_rates.get('USD'), normalised_exchange_rates.get('GBP'))
plt.show()

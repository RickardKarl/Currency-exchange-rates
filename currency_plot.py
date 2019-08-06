"""
    Author: Rickard Karlsson
"""
import json
import pprint
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from currency_func import request_exchange_rate
import sys

def plot_exchange_rate(exchange_dates, exchange_rates, base_currency,
                        ref_currency, plot_show = True):
    if plot_show == True:
        print("Plotting the result")
    plt.plot(exchange_dates, exchange_rates)

    start_date = exchange_dates[0]

    # Setting scale on x-axis with the dates (assumed format is YYYY-MM-DD)
    ticks = []
    ticks_label = []
    start_year = str(start_date)[0:4]
    i = 0
    for date in exchange_dates:
        date = str(date)
        if date[0:4] == start_year:
            if i%3 == 0:
                ticks.append(date)
                ticks_label.append(date[0:4])
            start_year = str(int(start_year) + 1)
            i += 1
    plt.xticks(ticks, ticks_label)

    # Setting labels
    plt.xlabel("Time period")
    plt.ylabel(ref_currency)
    plt.title("Exchange rate of " + base_currency)

    # Show plot
    if plot_show == True:
        plt.show()

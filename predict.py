import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
import os

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Dense, GRU, Embedding
from tensorflow.python.keras.optimizers import RMSprop
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau

from currency_func import *
from currency_plot import *



ref_currency = 'SEK'
target_current = 'USD'
start_date = "2000-01-01"


'''
Data retrieval
'''
curr_data = {}
available_currencies = get_available_base_currencies()

# Loop through all currencies
for curr in available_currencies:
    # Convert to time series
    data = request_exchange_rate(curr, ref_currency, start_date, end_date = today_date)
    series = pd.Series(data[0], index = data[1])

    # Resampling for a daily value of the time series
    curr_data[curr] = series.resample('D').pad()

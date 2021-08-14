import pandas as pd
import time
import os
from functions import *

# Misc. Setup
pd.set_option('display.max_rows', None)  # Display all rows

# Create instances
initial_balance = 1000000
Crypto = Crypto('btc', 'usd', initial_balance)  # interval for time at the end
OrderBook = OrderFlow()  # backtesting orderflow
#OrderBook = OrderFlow()

# outputsize and timeinterval // UTC Timezone
# Crypto.df_historical('full', 1)  # get data
df = pd.read_csv("backtest.csv", index_col=0)
# OrderBook.update_highest(df)  # After every iteration - for trailling stop loss


# Initialize indicators - since its backtesting its outside the loop
MACD(df)
RSI(df, 14)  # Shorter = More trades
EMA(df, 2)

print(df)  # to read and debug, delete later
# df.to_csv('backtest.csv')

# Backtest
filename, csv_file_name = log_new(None)
for index, row in df.iterrows():

    # retrieve current row data
    time = row['time']
    close = row['4. close']
    rsi = row['RSI']
    macd = row['MACD']
    macd_ema = row['MACDEMA']
    ema = row['2EMA']

    # signal calculations | True = Buy & False = Sell

    # indicator signals (backtesting)
    macd_signal = TA_B_MACD(macd, macd_ema)
    rsi_signal = TA_B_RSI(rsi, 75, 30)
    ema_signal = TA_B_EMA(close, ema)

    # Strat: sell at RSI and buy at MACD
    # Case 1: When no order exists, if asset is not overbought and macd is over macd ema (buy signal) place an buy order
    if not OrderBook.filled:  # if no order exists - buy order to be placed
        # RSI, MACD and 2 EMA
        if rsi_signal != False:  # if not overbought
            if macd_signal and ema_signal:
                OrderBook.buy(close, time, Crypto.balance)
                OrderBook.updateHighest(close)

    # Case 2: When an order exists, check if its overbought, trailling stop loss or macd indicates sell, if true sell
    else:  # if an order exists - sell order to be placed
        # Trailling stop loss - Call every iteration
        OrderBook.updateHighest(close)
        traillingStopLoss = TA_TRAILLING(
            OrderBook.highest, close, 0.01)  # trailling stop loss with 1% trigger
        # RSI, MACD and Trailling stop loss
        # if oversold or macd sell or trailling stop
        if not rsi_signal or not macd_signal or not ema_signal or traillingStopLoss:
            Crypto.balance, log_data = OrderBook.sell(
                close, time, Crypto.balance)
            log_sell(filename, log_data, csv_file_name)

final_balance = copy.deepcopy(Crypto.balance)
log_close(filename, initial_balance, final_balance)
tradedf = pd.read_csv(csv_file_name)

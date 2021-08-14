# pretty much same as backtest crypto but for stocks
from functions import *
import pandas as pd
import copy
import matplotlib.pyplot as plt

# replace with automated pick from scraped screener
pd.set_option('display.max_rows', None)  # Display all rows
ScreenerDf = MidRiskScreenerVOL()
initial_balance = 1000000  # 1 milli
Stocks = Stock('tsla', initial_balance)  # create an instance
OrderBook = OrderFlow()  # create order book instance

# create new log file (none = use date as file name)
filename, csv_file_name = log_new(None)
df = Stocks.df_historical_intraday(1, 'compact')

# Initialize Indicators (for live init inside while loop)
RSI(df, 6)
BOLBANDS(df, 20)  # 20 MEAN(SMA) and STD

print(df)
print()

for index, row in df.iterrows():
    time = row['time']
    close = row['4. close']
    rsi = row['RSI']
    upperband = row['upper_bolband']
    lowerband = row['lower_bolband']

    rsi_signal = TA_B_RSI(rsi, 70, 30)
    bol_signal = TA_B_BB(close, upperband, lowerband)

    if not OrderBook.filled:
        if rsi_signal and bol_signal:
            OrderBook.buy(close, time, Stocks.balance)
    else:
        if rsi_signal == False and bol_signal == False:
            Stocks.balance, log_data = OrderBook.sell(
                close, time, Stocks.balance)
            log_sell(filename, log_data, csv_file_name)


final_balance = copy.deepcopy(Stocks.balance)
log_close(filename, initial_balance, final_balance)
trade_data = pd.read_csv(csv_file_name)
print(final_balance)
print(trade_data)
# Graphing
'''
plt.figure(figsize=(10, 5))
plt.grid(True)
plt.plot(df['4. close'], label='CLOSE', color='blue')
#plt.plot(df['RSI'], label='RSI', color='blue')
#plt.plot(df['MACD'], label='MACD', color='green')
#plt.plot(df['MACDEMA'], label='MACD SIGNAL', color='red')
plt.legend(loc=2)
plt.show()
'''

from functions import *
import pandas as pd
import copy
import matplotlib.pyplot as plt
import copy
import streamlit as st
import time
# For sending email
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
# For time in the live functions that wait for the market to open and sleep when closed
import datetime as dt
import pytz  # for timezone


# Utilities
def SendEmail(subject, to, content):
    app_pass = 'enkdtoceszszupsh'
    app_email = 'ProfiTradeAlgo@gmail.com'

    msg = EmailMessage()  # Message Object
    msg['Subject'] = subject
    msg['From'] = app_email
    msg['To'] = to
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:  # mail server and port number
        smtp.login(app_email, app_pass)  # login (use env vars)
        smtp.send_message(msg)  # sends out the message


def EasternTime(ReturnList):
    dt_utcnow = dt.datetime.now(tz=pytz.UTC)
    dt_est = dt_utcnow.astimezone(pytz.timezone('US/Eastern'))
    hourmin = dt_est.strftime('%H,%M').split(',')
    date = dt_est.strftime('%D').split('/')
    return hourmin, date


# Low risk
def low_risk_backtest(ticker, init_balance, data_range):
    Stocks = Stock(ticker, init_balance)  # Init stock class (from functions)
    OrderBook = OrderFlow()  # create order book instance

    # create new log file (none = use date as file name)
    filename, csv_file_name = log_new(None)

    df = Stocks.df_historical_daily(data_range)  # gets from alpha vantage
    RSI(df, 2)  # Add RSI period 2 to the df provided
    for index, row in df.iterrows():  # iterate through the df
        # Set variables
        time = row['time']
        close = row['4. close']
        rsi = row['RSI']

        # Perform signal functions
        # Calculates signal range based on parameters
        rsi_signal = TA_B_RSI(rsi, 90, 10)

        # Main Strategy
        if not OrderBook.filled:  # To avoid stacking orders
            if rsi_signal:
                OrderBook.buy(close, time, Stocks.balance)
        else:
            # OrderBook.updateHighest(close)
            # traillingStopLoss = TA_TRAILLING(OrderBook.highest, close, 0.001)  # 1k trailling stop loss
            if rsi_signal == False:
                Stocks.balance, log_data = OrderBook.sell(
                    close, time, Stocks.balance)
                log_sell(filename, log_data, csv_file_name)

    final_balance = copy.deepcopy(Stocks.balance)
    # Adds the final balance and delta
    log_close(filename, init_balance, final_balance)
    trade_data = pd.read_csv(csv_file_name)
    return final_balance, df, trade_data


def low_risk_live(init_balance, ticker, UserEmail):
    # Constants
    outputsize = 'compact'
    ticker = ticker.upper()  # just to be safe, convert to uppercase

    # Init classes
    Stocks = Stock(ticker, init_balance)
    OrderBook = OrderFlow()  # Live Order Flow (Buy, Sell)

    # Get historical price data
    prevDf = Stocks.df_historical_daily(outputsize)
    # Create new log file (none = use date as file name)
    filename, csv_file_name = log_new(None)  # filename is an xl file

    # Start new loop
    while True:
        print("INSIDE LOOP")
        # Get historical data
        currentDf = Stocks.df_historical_daily(outputsize)
        # Check if the dataframe isnt updated with the new price
        if currentDf.iloc[-1]['4. close'] != prevDf.iloc[-1]['4. close']:
            RSI(currentDf, 2)  # Calculate RSI
            # Set variables
            _time_ = currentDf.iloc[-1]['time']
            close = currentDf.iloc[-1]['4. close']
            rsi = currentDf.iloc[-1]['RSI']
            # Func RSI Signal
            rsi_signal = TA_RSI(df, 10, 90)

            # Main Strategy
            if not OrderBook.filled:  # To avoid stacking orders
                if rsi_signal:  # if RSI signals buy
                    OrderBook.buy(close, _time_, Stocks.balance)  # place order
                    # Send email notification with ticker and company etc
                    SendEmail('{} ALERT: PLACE BUY ORDER'.format(ticker), UserEmail, "Please place a BUY ORDER for {} | Time: {} | Closing Price: {}".format(
                        ticker, _time_, close))  # subject, to, content
            else:
                if rsi_signal == False:
                    Stocks.balance, log_data = OrderBook.sell(
                        close, _time_, Stocks.balance)
                    log_sell(filename, log_data, csv_file_name)
                    # Send email notification
                    SendEmail('{} ALERT: PLACE SELL ORDER'.format(ticker), UserEmail, "Please place a SELL ORDER for {} | Time: {} | Closing Price: {}".format(
                        ticker, _time_, close))  # subject, to, content
                elif rsi_signal == None:
                    # Email saying hold at current price - to notifiy the user (also means that the algorithm is working)
                    SendEmail('{} ALERT: HOLD'.format(ticker), UserEmail, "Please HOLD {} | Time: {} | Closing Price: {}".format(
                        ticker, _time_, close))  # subject, to, content

            prevDf = currentDf  # so the next day you can check if the data frame is updated

        else:  # if they have the same time stamp
            # 6 hours sleep time (pre much arbitary but 4 calls per day)
            SendEmail('{} ALERT: ACTIVATING SLEEP'.format(
                ticker), UserEmail, "Sleeping for 6 hours. Algorithm is working.")
            time.sleep(240)
    return


# Mid risk
def mid_risk_backtest(ticker, init_balance, data_range):
    Stocks = Stock(ticker, init_balance)  # Init stock class (from functions)
    OrderBook = OrderFlow()  # create order book instance

    # create new log file (none = use date as file name)
    filename, csv_file_name = log_new(None)

    df = Stocks.df_historical_intraday(
        5, data_range)  # gets from alpha vantage

    RSI(df, 2)  # Add RSI period 2 to the df provided
    for index, row in df.iterrows():  # iterate through the df
        # Set variables
        time = row['time']
        close = row['4. close']
        rsi = row['RSI']

        # Perform signal functions
        rsi_signal = TA_B_RSI(rsi, 90, 10)

        # Main Strategy
        if not OrderBook.filled:  # To avoid stacking orders
            if rsi_signal:
                OrderBook.buy(close, time, Stocks.balance)
        else:
            # OrderBook.updateHighest(close)
            # traillingStopLoss = TA_TRAILLING(OrderBook.highest, close, 0.001)  # 1k trailling stop loss
            if rsi_signal == False:
                Stocks.balance, log_data = OrderBook.sell(
                    close, time, Stocks.balance)
                log_sell(filename, log_data, csv_file_name)

    final_balance = copy.deepcopy(Stocks.balance)
    # log close adds the final balance and delta to the xl
    log_close(filename, init_balance, final_balance)
    trade_data = pd.read_csv(csv_file_name)
    return final_balance, df, trade_data


def mid_risk_live(ticker, init_balance, UserEmail):
    # Constants
    outputsize = 'compact'  # call once and then use web scraping functions
    ticker = ticker.upper()  # just in case user enters lowercase

    # Init classes
    Stocks = Stock(ticker, init_balance)
    OrderBook = OrderFlow()  # Live order Flow (Buy,Sell)

    # get previous price data
    # pull pervious 5 min intraday details
    df = Stocks.df_historical_intraday(5, 'compact')
    RSI(df, 2)  # Add RSI period 2 to the df
    # Create new log file (none == use date as file name)
    filename, csv_file_name = log_new(None)

    SendEmail('{} ALERT: ALGO STARTED'.format(ticker),
              UserEmail, 'The algorithm is working sucessfully')
    # start while loop
    while True:
        # get eastern time
        dt_utcnow = dt.datetime.now(tz=pytz.UTC)
        dt_est = dt_utcnow.astimezone(pytz.timezone('US/Eastern'))
        hourmin = dt_est.strftime('%H,%M').split(',')
        date = dt_est.strftime('%D').split('/')
        # If market already closed today
        if int(hourmin[0]) > 16 and int(hourmin[1]) > 30:
            OpenDate = int(date[1]) + 1
            marketOpen = dt.datetime(2021, 8, OpenDate, 9, 30)
            # Opens in
            OpensIn = marketOpen - dt.datetime.now()
            SendEmail('{} ALERT: MARKET TIME'.format(ticker), UserEmail,
                      "Market is closed, Opens in {}".format(OpensIn))
            OpensIn = OpensIn.total_seconds()
            time.sleep(OpensIn)
        # If market is yet to open today
        elif int(hourmin[0]) < 9 and int(hourmin[1]) < 30:
            marketOpen = dt.datetime(2021, 8, int(date[1]), 9, 30)
            # Opens in
            OpensIn = marketOpen - dt.datetime.now()
            SendEmail('{} ALERT: MARKET TIME'.format(ticker), UserEmail,
                      "Market is closed, Opens in {}".format(OpensIn))
            OpensIn = OpensIn.total_seconds()
            time.sleep(OpensIn)
        elif int(hourmin[0]) >= 9:  # If market is open
            SendEmail('{} ALERT: MARKET TIME'.format(
                ticker), UserEmail, 'Opening Bell')
            print('Inside market open period')
            df = Stocks.df_current_yahoo(df)
            RSI(df, 2)
            # SET VARIABLES
            _time_ = df.iloc[-1]['time']
            close = df.iloc[-1]['4. close']
            rsi = df.iloc[-1]['RSI']
            # Func RSI Signal
            rsi_signal = TA_B_RSI(df, 90, 10)
            # Main Strategy
            if not OrderBook.filled:  # To avoid stacking orders
                if rsi_signal:
                    OrderBook.buy(close, time, Stocks.balance)
                    SendEmail('{} ALERT: PLACE BUY ORDER'.format(ticker), UserEmail, "Please place a BUY ORDER for {} | Time: {} | Closing Price: {}".format(
                        ticker, _time_, close))  # subject, to, content
            else:
                if rsi_signal == False:
                    Stocks.balance, log_data = OrderBook.sell(
                        close, time, Stocks.balance)
                    log_sell(filename, log_data, csv_file_name)
                    SendEmail('{} ALERT: PLACE SELL ORDER'.format(ticker), UserEmail, "Please place a SELL ORDER for {} | Time: {} | Closing Price: {}".format(
                        ticker, _time_, close))  # subject, to, content
                elif rsi_signal == None:
                    SendEmail('{} ALERT: HOLD'.format(ticker), UserEmail, "Please HOLD {} | Time: {} | Closing Price: {}".format(
                        ticker, _time_, close))  # subject, to, content
            time.sleep(300)  # 5 min sleep cause thats the interval
    return


# High risk crypto
def high_risk_crypto(init_balance, UserTrailling, UserEmail):
    # interval for time at the end
    CryptoCoin = Crypto('btc', 'usd', init_balance)
    OrderBook = OrderFlow()
    filename, csv_file_name = log_new(None)
    SendEmail("BTC ALERT: RUNNNING", UserEmail, "PROGRAM IS RUNNING")
    while True:
        df = CryptoCoin.df_historical('compact', 1)
        # Calculate and add indicators
        MACD(df)
        RSI(df, 14)  # Shorter = More trades
        EMA(df, 2)
        # Pull indicator values
        _time_ = df.iloc[-1]['time']
        close = df.iloc[-1]['4. close']
        rsi = df.iloc[-1]['RSI']
        macd = df.iloc[-1]['MACD']
        macd_ema = df.iloc[-1]['MACDEMA']
        ema = df.iloc[-1]['2EMA']
        # Get trade signal (bool)
        macd_signal = TA_B_MACD(macd, macd_ema)
        rsi_signal = TA_B_RSI(rsi, 75, 30)
        ema_signal = TA_B_EMA(close, ema)

        # Case 1: When no order exists, if asset is not overbought and macd is over macd ema (buy signal) and ema place an buy order
        print("WORKING")
        if not OrderBook.filled:  # if no order exists - buy order to be placed
            # RSI, MACD and 2 EMA
            if rsi_signal != False:  # if not overbought
                if macd_signal and ema_signal:
                    OrderBook.buy(close, _time_, CryptoCoin.balance)
                    OrderBook.updateHighest(close)
                    SendEmail('BTC ALERT: PLACE BUY ORDER', UserEmail, "Please place a BUY ORDER for BTC | Time: {} | Closing Price: {}".format(
                        _time_, close))  # subject, to, content

        # Case 2: When an order exists, check if its overbought, trailling stop loss or macd or ema indicates sell, if true sell
        else:  # if an order exists - sell order to be placed
            # Trailling stop loss - Call every iteration
            OrderBook.updateHighest(close)
            traillingStopLoss = TA_TRAILLING(
                OrderBook.highest, close, UserTrailling)  # trailling stop loss with 1% trigger

            # RSI, MACD and Trailling stop loss
            # if oversold or macd sell or ema sell or trailling stop
            if not rsi_signal or not macd_signal or not ema_signal or traillingStopLoss:
                CryptoCoin.balance, log_data = OrderBook.sell(
                    close, _time_, CryptoCoin.balance)
                log_sell(filename, log_data, csv_file_name)
                SendEmail('BTC ALERT: PLACE SELL ORDER', UserEmail, "Please place a SELL ORDER for BTC | Time: {} | Closing Price: {}".format(
                    _time_, close))  # subject, to, content
            else:  # for holding
                SendEmail("BTC ALERT: HOLD", UserEmail,
                          "Please hold the asset")
        time.sleep(60)  # sleep for a min
    return


# Screening Code
def ScreenerScanning(screener_df, init_balance, filename, riskT):
    df = screener_df.head()  # isolates the first five
    # If the first five tickers are the same as the saved csv file tickers just retrun the data from that

    filename = "{}.csv".format(filename)
    # Check if the data is the same
    FinalDF = pd.read_csv(filename)
    Rescan = False

    # Check if the screener tickers are the same
    # If theyre the same no need to call API again (Optimization)
    if FinalDF.size != 0:
        for index in range(0, 4):  # for the first five tickers
            ScannedDf = FinalDF.iloc[index]['Ticker']
            ScreenerDf = df.iloc[index]['Ticker']
            if ScannedDf != ScreenerDf:  # if theyre not the same
                Rescan = True
    else:
        Rescan = True

    # If the screener tickers have changed
    if Rescan:
        NewScannerLogger(filename)  # Create new csv file
        for index, row in df.iterrows():  # iterate through the screener df
            ticker = row['Ticker']  # get ticker from the editied df

            # perform low risk backtest (Uses alpha vantage API for price data)
            if riskT == "Low":
                AlgorithmicFinalBalance, PriceData, __ = low_risk_backtest(
                    ticker, init_balance, 'compact')
            elif riskT == "Mid":
                AlgorithmicFinalBalance, PriceData, __ = mid_risk_backtest(
                    ticker, init_balance, 'compact')

            # Vars from Price Data
            InitialPrice = PriceData.iloc[0]['4. close']
            FinalPrice = PriceData.iloc[-1]['4. close']

            # Calculate respective net changes
            AlgorithmicNetChange = AlgorithmicFinalBalance - init_balance
            HodlInitQuantity = init_balance / InitialPrice
            HodlInital = HodlInitQuantity * InitialPrice
            HodlFinal = HodlInitQuantity * FinalPrice
            HodlNetChange = HodlFinal - init_balance

            # % Change Calculation
            AlgoPercentChange = (
                (AlgorithmicFinalBalance - init_balance) / init_balance) * 100
            NonAlgoPercentChange = (
                (FinalPrice - InitialPrice) / InitialPrice)*100

            # % Diff Calculation
            numerator = abs(AlgorithmicNetChange - HodlNetChange)
            denominator = (AlgorithmicNetChange + HodlNetChange) / 2
            PercentDiff = (numerator/denominator) * 100

            # Apending to CSV file
            data = [ticker, AlgorithmicNetChange, AlgoPercentChange,
                    HodlNetChange, NonAlgoPercentChange, PercentDiff]
            AppendScannerLogger(filename, data)

        FinalDF = pd.read_csv(filename)  # Read the new file name

    # Sort the ScannerDF and retrive the needed tickers
    FinalDF.sort_values(
        by=['Net % Diff'], ascending=False, inplace=True)
    InitFinalDf = copy.deepcopy(FinalDF)
    MostSucessfull = FinalDF.iloc[0]['Ticker']
    FinalDF.sort_values(
        by=['Algorithmic % Change'], ascending=False, inplace=True)
    HighestReturn = FinalDF.iloc[0]['Ticker']

    time.sleep(15)  # to avoid API errors
    return MostSucessfull, HighestReturn, InitFinalDf

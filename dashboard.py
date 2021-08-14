import streamlit as st
from functions import *
import streamlit.components as stc
import base64
from main import *
import time
import copy
import numpy as np
# https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets


# utils
def xlsxDownloader(filename):
    b64 = base64.b64encode(filename.encode()).decode()
    st.markdown('#### Download File ###')
    href = f'<a href ="data:file/xlsx;base64,{b64}" download="{filename}">Click Here!!</a>'
    st.markdown(href, unsafe_allow_html=True)


# Create a function with the basic code to optimize?
def printScannedRecomended(Screener, init_balance, filename, riskT):
    st.subheader("Recomended Ticker (Backtest First 5)")
    MostSucessfull, HighestReturn, InitFinalDf = ScreenerScanning(
        Screener, init_balance, filename, riskT)

    st.write("Most Sucessful (% Diff.): {}".format(MostSucessfull))
    i, __ = np.where(Screener == "{}".format(
        str(MostSucessfull)))  # find location of the ticker
    st.write("Company/Fund: {}".format(Screener.iloc[int(i)]["Company"]))

    st.write("Highest Net Return (%): {}".format(HighestReturn))
    i, __ = np.where(Screener == "{}".format(
        str(HighestReturn)))  # find location of the ticker
    st.write("Company/Fund: {}".format(Screener.iloc[int(i)]["Company"]))

    st.write("Data:")
    st.write(InitFinalDf)  # print the screener
    return MostSucessfull, HighestReturn


def printPostBacktest(final_balance, trade_data, price_df):
    st.subheader(
        'Final Balance: {:,} USD'.format(final_balance))
    st.text(
        "(Note: Starting AUM in sidebar is not automatically updated)")
    st.subheader('Trade Data')
    st.write(trade_data)
    st.subheader('Price Data')
    st.write(price_df)


# Sidebar code
st.sidebar.title('ProfiTrade')

PageSelector = st.sidebar.selectbox(
    "Page:", ("Home", "Trading (Risk Tolerance Model)", "Custom Dashboard", "Custom Trading (Equity)"))

if PageSelector == "Trading (Risk Tolerance Model)":

    # SIDEBAR CODE
    RiskTolerance = st.sidebar.selectbox(
        "Risk Tolerance:",
        ("Low", "Medium", "High"), help="This selection is an parameter for the trade frequency, strategy and market exposure"
    )  # To enter the respective trading scripts

    Balance = st.sidebar.number_input(
        'Starting AUM:', min_value=1, help="Your beginning asset under management. Minimum balance 1 USD")  # Initial Balance
    st.sidebar.write('Initial balance: {:,} USD'.format(Balance))

    EmailNotification = st.sidebar.radio(
        "Email Notification:", ("No", "Yes"), help="Sends trade information or notification")
    if EmailNotification == "Yes":
        UserEmail = st.sidebar.text_input(
            "Enter your email", help="Please enter your full email xyz@email.com")

    # run len for email notification entry or not (do basic .com to see if its an email)
    if RiskTolerance == "Low":

        # Common Key Variables
        init_balance = copy.deepcopy(Balance)

        # Heading and title
        st.title("Low Risk Equity Trading")
        st.write(
            'Strategy primarly consists of mean regression models that have proven effective over time. The net gain is relative to your risk tollerance. The higher the tollerance, the higher the probable return.')
        st.text(
            "(Note: Changing any parameter after commencing trading resets the entire application)")
        # Prompt version selection (Live/Backtesting)
        VersionSelector = st.radio(
            "Select a version:", ("Live", "Backtesting"))
        st.write(
            "(Note: Backtesting the algorithm prior to live trading is advised if the recomended ticker isnt chosen)")

        # Backtesting
        if VersionSelector == "Backtesting":
            st.header('Backtest:')

            # Prompt screener selection (Sideways Channel, Sideways Channel (Volume))
            ScreenerSelection = st.radio(
                "Select a screener:", ("Sideways Channel (Signal)", "Sideways Channel (Volume)"))

            # Sideways Channel (Signal)
            if ScreenerSelection == "Sideways Channel (Signal)":
                st.header("Sideways Channel (Signal)")

                # Print Screener DF
                ScreenerDF = SideChannel()
                st.write(ScreenerDF)

                # Print Screener Scanning Algorithm Results
                MostSucessfull, HighestReturn = printScannedRecomended(
                    ScreenerDF, init_balance, 'SidewaysChannel', "Low")

                # Prompt trading option (Manual/Automatic)
                Option = st.radio('Trading Option:', ('Manual', 'Automatic'))
                st.text(
                    "Note: The automatic option selects the recomended data frame range and ticker")

                if Option == "Automatic":
                    # If theyre both not the same
                    if MostSucessfull != HighestReturn:
                        st.subheader("{} produces the highest return and {} is the most sucessfull".format(
                            HighestReturn, MostSucessfull))
                    else:
                        st.subheader(
                            "{} is the recomended best ticker".format(MostSucessfull))
                    st.write(
                        "(Note: The results are based on compact historical daily closing price data)")

                if Option == "Manual":
                    # Print Trade Details
                    st.subheader('Trade Details:')
                    st.text('Initial Balance: {:,} USD'.format(init_balance))
                    # Ticker prompt
                    ticker = st.text_input(
                        'Ticker:', max_chars=10, help="Manually choose a ticker for the dataframe above to trade using the algorithm")
                    if len(ticker) > 0:  # if an ticker is entered
                        # try finding the ticker on the data frame
                        ticker = ticker.upper()  # convert ticker to uppercase
                        i, __ = np.where(
                            ScreenerDF == "{}".format(str(ticker)))  # find location of the ticker
                        if i.size > 0:  # if the entered ticker exists
                            #company = str(SideWays_df.iloc[i]["Company"])
                            st.text("Ticker: {}".format(ticker))
                            st.text(
                                "Company/Fund: {}".format(ScreenerDF.iloc[int(i)]["Company"]))
                            st.text("Data Interval: 1D")

                            # Data Selection Range
                            DataRange = st.radio(
                                'Data range:', ("Compact", "Full (20+ Years)"))

                            if DataRange == "Compact":
                                st.text("Data range: Compact")
                                final_balance, price_df, trade_data = low_risk_backtest(
                                    ticker, init_balance, 'compact')
                                printPostBacktest(
                                    final_balance, trade_data, price_df)

                            if DataRange == "Full (20+ Years)":
                                st.text("Data range: Full")
                                final_balance, price_d, trade_data = low_risk_backtest(
                                    ticker, init_balance, 'full')
                                printPostBacktest(
                                    final_balance, trade_data, price_df)

                        else:  # If invalid ticker was chosen
                            st.write(
                                "Please select a valid ticker from the screener dataframe above")

            # Sideways Channel (Volume)
            if ScreenerSelection == "Sideways Channel (Volume)":
                st.header("Sideways Channel (Signal)")

                # Get screener and print the screener DF
                ScreenerDF = SidewaysHighVolume()
                st.write(ScreenerDF)

                # Print Screener Scanning Algorithm Results
                MostSucessfull, HighestReturn = printScannedRecomended(
                    ScreenerDF, init_balance, 'SideWaysVolume', "Low")

                # Promt user for trading option
                Option = st.radio('Trading Option:', ('Manual', 'Automatic'))
                st.text(
                    "Note: The automatic option selects the recomended data frame range and ticker")

                if Option == "Automatic":
                    # If theyre both not the same
                    if MostSucessfull != HighestReturn:
                        st.subheader(
                            "{} is the recomended best ticker".format(MostSucessfull))
                    else:  # not the same
                        st.subheader("{} produce the highest return and {} is the most sucessfull".format(
                            HighestReturn, MostSucessfull))
                    st.write(
                        "(Note: The results are based on compact historical daily closing price data)")

                if Option == "Manual":

                    # Start creating the debug
                    st.subheader('Trade Details:')
                    st.text('Initial Balance: {:,} USD'.format(init_balance))
                    ticker = st.text_input(
                        'Ticker:', max_chars=10, help="Recomended to manually choose a ticker for the dataframe above to trade using the algorithm")

                    if len(ticker) > 0:  # if an ticker is entered
                        ticker = ticker.upper()
                        # Find the location fo the ticker in the index
                        i, __ = np.where(SideWays_HighVolume_df ==
                                         "{}".format(str(ticker)))
                        if i.size > 0:  # find location of the ticker in df
                            #company = str(SideWays_df.iloc[i]["Company"])
                            st.text("Ticker: {}".format(ticker))
                            st.text(
                                "Company/Fund: {}".format(SideWays_HighVolume_df.iloc[int(i)]["Company"]))
                            st.text("Data Interval: 1D")

                            # Prompt user to an select data range
                            DataRange = st.radio(
                                'Data range:', ("Compact", "Full"))

                            if DataRange == "Compact":
                                st.text("Data range: Compact")
                                final_balance, price_df, trade_data = low_risk_backtest(
                                    ticker, init_balance, 'compact')
                                printPostBacktest(
                                    final_balance, trade_data, price_df)

                            if DataRange == "Full":
                                st.text("Data range: Full")
                                final_balance, price_df, trade_data = low_risk_backtest(
                                    ticker, init_balance, 'full')
                                printPostBacktest(
                                    final_balance, trade_data, price_df)

                        else:  # invalid ticker selection
                            st.write(
                                "Please select a valid ticker from the screener dataframe above")

        if VersionSelector == "Live":
            # Basic details to print
            st.header("Strategy (Brief):")
            st.write("- Low risk strategy acts on daily closing price")
            st.write(
                "- You will receive a email notification for every order with trade information")
            st.write(
                "- For the algorithm to work successfully, please do not close the browser (streamlit) unless you're running the script on a terminal")
            st.write('- An XL and a CSV file with the trading data is stored in the same folder as the script. Please do not open this untill the script is closed')

            if EmailNotification == "No":  # If email notification isnt toggled in the sidebar
                st.header(
                    "NOTE: Please opt in for the email notification and enter a valid email")
            else:  # if use opts in for email notification
                if len(UserEmail) > 0:  # if an email is entered
                    # Prompt screener selection (Sideways Channel, Sideways Channel (Volume))
                    st.header("Screening:")
                    st.write(
                        "(Note: All the screeners are based on live or last active price data information)")
                    ScreenerSelection = st.radio(
                        "Select a screener:", ("Sideways Channel (Signal)", "Sideways Channel (Volume)"))

                    # If the user selects this screener
                    if ScreenerSelection == "Sideways Channel (Signal)":
                        st.subheader("Sideways Channel (Signal)")
                        ScreenerDF = SideChannel()  # Get screener DF
                        st.write(ScreenerDF)  # Print the Screener DF
                        # Perform and print Screener Scanning Algorithm Results
                        MostSucessfull, HighestReturn = printScannedRecomended(
                            ScreenerDF, init_balance, 'SidewaysChannel', "Low")
                        ChosenStock = st.radio(
                            "Choose one of the following:", ("Highest Return", "Most sucessfull (% Diff.)"))  # let the user pick the option they prefer
                        # to avoid running while user makes up their mind since its an while loop
                        StartSignal = st.radio("Start Algo:", ("No", "Yes"))
                        if StartSignal == "Yes":
                            st.write(
                                "Running: Email notifications will be sent")  # cause it doesnt print if its after the function calling
                            # Two options: Run the function
                            if ChosenStock == "Highest Return":
                                low_risk_live(
                                    init_balance, HighestReturn, UserEmail)
                            if ChosenStock == "Most sucessfull (% Diff.)":
                                low_risk_live(
                                    init_balance, MostSucessfull, UserEmail)

                    if ScreenerSelection == "Sideways Channel (Volume)":
                        st.subheader("Sideways Channel (Volume)")
                        ScreenerDF = SidewaysHighVolume()  # Get screener DF
                        st.write(ScreenerDF)  # Print the Screener DF
                        # Perform and print Screener Scanning Algorithm Results
                        MostSucessfull, HighestReturn = printScannedRecomended(
                            ScreenerDF, init_balance, 'SideWaysVolume', "Low")
                        ChosenStock = st.radio(
                            "Choose one of the following:", ("Highest Return", "Most sucessfull (% Diff.)"))
                        # to avoid running while user makes up their mind since its an while loop
                        StartSignal = st.radio("Start Algo:", ("No", "Yes"))
                        if StartSignal == "Yes":
                            st.write(
                                "Running: Email notifications will be sent")  # cause it doesnt print if its after the function calling
                            # Two options: Run the function
                            if ChosenStock == "Highest Return":
                                low_risk_live(
                                    init_balance, HighestReturn, UserEmail)
                            if ChosenStock == "Most sucessfull (% Diff.)":
                                low_risk_live(
                                    init_balance, MostSucessfull, UserEmail)

                else:
                    st.header("NOTE: Please enter a valid email")

    if RiskTolerance == "Medium":
        # Common Key Variables
        init_balance = copy.deepcopy(Balance)
        # Title etc. for header
        st.title("Mid Risk Equity Trading")
        st.write(
            'Strategy primarly consists of a mean regression model. Uses 5 min intraday prices.')
        st.text(
            "(Note: Changing any parameter after commencing trading resets the entire application)")
        # Screening
        st.header("Screener: Horizontal Support/Resistance")
        ScreenerDF = horizontalNearSupRes()
        st.write(ScreenerDF)
        # Scanning
        MostSucessfull, HighestReturn = printScannedRecomended(
            ScreenerDF, init_balance, 'HorizontalSP', "Mid")
        st.text("(Using compact 5 min intraday price data)")
        # Prompt version selection (Live/Backtesting)
        VersionSelector = st.radio(
            "Select a version:", ("Live", "Backtesting"))
        st.write(
            "(Note: Backtesting the algorithm prior to live trading is advised if the recomended ticker isnt chosen)")

        if VersionSelector == "Backtesting":
            st.header("Backtesting:")
            Option = st.radio('Trading Option:', ('Manual', 'Automatic'))
            st.text(
                "Note: The automatic option selects the recomended data frame range and ticker")
            if Option == "Automatic":
                # If theyre both not the same
                if MostSucessfull != HighestReturn:
                    st.subheader("{} produces the highest return and {} is the most sucessfull".format(
                        HighestReturn, MostSucessfull))
                else:
                    st.subheader(
                        "{} is the recomended best ticker".format(MostSucessfull))
            if Option == "Manual":
                # Print Trade Details
                st.subheader('Trade Details:')
                st.text('Initial Balance: {:,} USD'.format(init_balance))
                # Ticker prompt
                ticker = st.text_input(
                    'Ticker:', max_chars=10, help="Manually choose a ticker from the dataframe above to trade")
                if len(ticker) > 0:  # if an ticker is entered
                    # try finding the ticker on the data frame
                    ticker = ticker.upper()  # convert ticker to uppercase
                    i, __ = np.where(ScreenerDF == "{}".format(
                        str(ticker)))  # find location of the ticker
                    if i.size > 0:  # if the entered ticker exists
                        st.text("Ticker: {}".format(ticker))
                        st.text(
                            "Company/Fund: {}".format(ScreenerDF.iloc[int(i)]["Company"]))
                        st.text("Data Interval: 5min")

                        # Data Selection Range
                        DataRange = st.radio(
                            'Data range:', ("Compact", "Full"))

                        if DataRange == "Compact":
                            st.text("Data range: Compact")
                            final_balance, price_df, trade_data = mid_risk_backtest(
                                ticker, init_balance, 'compact')
                            printPostBacktest(
                                final_balance, trade_data, price_df)

                        if DataRange == "Full":
                            st.text("Data range: Full")
                            final_balance, price_df, trade_data = mid_risk_backtest(
                                ticker, init_balance, 'full')
                            printPostBacktest(
                                final_balance, trade_data, price_df)

                    else:  # If invalid ticker was chosen
                        st.write(
                            "Please select a valid ticker from the screener dataframe above")

        # add a live version
        if VersionSelector == "Live":
            st.header("Briefing:")
            st.write("- Mid risk model acts on 5 min intraday price data")
            st.write("- You need to enter a email to use the live model")
            st.write(
                "- You will receive a email notification for every order with trade information")
            st.write("- For the algorithm to work sucessfully, please do not close the browser (streamlit) unless you're running the script on a terminal")
            st.write("- An Xl and CSV file with the trading and screener scanning data is stored in the same folder as dashboard.py. Please do not open this untill the script is closed/done.")

            if EmailNotification == "No":
                st.header(
                    "NOTE: Please opt in for the email notification and enter a valid email"
                )
            else:
                if len(UserEmail) > 0:
                    ChosenStock = st.radio(
                        "Choose one of the following:", ("Highest Return", "Most sucessfull (% Diff.)"))
                    StartSignal = st.radio('Start Algo:', ("No", "Yes"))
                    if StartSignal == "Yes":
                        st.write("Running: Email notifications will be sent")
                        if ChosenStock == "Highest Return":
                            mid_risk_live(
                                HighestReturn, init_balance, UserEmail)
                        if ChosenStock == "Most sucessfull (% Diff.)":
                            mid_risk_live(MostSucessfull,
                                          init_balance, UserEmail)
                else:
                    st.header("NOTE: Please enter a valid email")

    if RiskTolerance == 'High':
        # Common Vars
        init_balance = copy.deepcopy(Balance)
        # Title
        st.title('High Risk Trading')
        # basic info and select asset type
        AssetType = st.radio("Please select an asset category:",
                             ("Equity", "Cryptocurrency"))
        st.text(
            "(Note: Changing any parameter after commencing trading resets the entire application)")

        if AssetType == "Cryptocurrency":
            # Get stop loss input
            TraillStopLS = st.sidebar.number_input(
                "Trailling Stop Loss (%):", min_value=0.01, max_value=100.00)
            TraillingDecimalStopLoss = TraillStopLS / \
                100  # calculate the decimal stop loss
            st.sidebar.text("Decimal Trailling SL: {}".format(
                TraillingDecimalStopLoss))

            st.header(AssetType)
            st.write(
                "ProfiTrade is currently limited only to high frequency Bitcoin (BTC) trading.")
            st.subheader('Strategy:')
            st.write(
                '- The algorithm consists of mean reversion/regression models using custom proven RSI, EMA and MACD')
            st.write("- Please enter your email and select a trailling stop loss")

            if EmailNotification != "Yes":
                st.header(
                    "NOTE: YOU NEED TO OPT IN AND ENTER A EMAIL TO PROCEED")
            else:
                if len(UserEmail) > 0:
                    st.subheader(
                        "PROGRAM RUNNING: EMAIL NOTIFICATIONS WILL BE SENT")
                    high_risk_crypto(
                        init_balance, TraillingDecimalStopLoss, UserEmail)
                else:
                    st.header("NOTE: PLEASE ENTER A VALID EMAIL")

        if AssetType == "Equity":
            st.header("Currently Not Available :(")
            st.subheader("Feature comming soon")

if PageSelector == "Home":
    st.title("ProfiTrade")
    st.text('Income, Automated.')

    # Body home page
    st.header("Requirements:")
    st.write("- Fast and reliable internet connection")
    st.write(
        "- Low cost brokerage to execute trades (i.e. WealthSimple, Robinhood etc.)")

    st.header("Guide:")
    st.write("- For the complete automation of screening, selection and trading please select the Trading (Risk Tolerance Model) from the sidebar. (Recomended)")
    st.write("- For selecting a ticker of your choice and customizing the algorithm please select Custom Trading option")
    st.write("- For more customized screeners please slecet the screener page")

    st.header("Screeners (Basic):")
    st.subheader("Top Gainers:")
    st.write(TopGainers())

    st.subheader("Most Active:")
    st.write(MostActive())

    st.subheader("Most Volatile:")
    st.write(MostVolatile())

    st.text("(Note: If an unexpected/http error occurs please refresh the tab)")

    # Side bar home page
    st.sidebar.write("Future of ProfiTrade:")
    st.sidebar.write("- Launch ProfiTrade as an open source API")
    st.sidebar.write("- Add machine learning models to optimize analysis")
    st.sidebar.write("- Create a ProfiTrade mobile app")

if PageSelector == "Custom Trading (Equity)":
    st.header("COMMING SOON: CUSTOM TRADING")
    st.subheader("Build your own algorithm without code")
    st.write("(All the backend is 90 percent ready, just need to add it to the GUI)")
    st.subheader("What does it do?")
    st.write("- Select your own indicator signal options")
    st.write("- Back test custom algorithms or live test with email notifications")
    st.write("- Crypto and other features comming soon to custom too")

if PageSelector == "Custom Dashboard":
    st.title("Custom Dashboard")
    st.write("- Displays news sentiment and overview")

    ticker = st.text_input("Ticker")
    if len(ticker) > 0:
        # print the news
        overview = companyOverview(ticker)
        st.subheader("Company Overview")
        st.write(overview)
        # print news sentiment
        st.subheader("News Sentiment")
        sentiment = newsSentiment(ticker)
        st.write(sentiment)

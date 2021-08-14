# ProfiTrade
A fintech application that automates trading relative to the users' risk tolerance built entirely using Python.

## What it does
Based on the user's risk tolerance the algorithm uses mean reversion models on crypto currency and equities to place high-frequency trades or swing trades. Each trade is notified via email and a custom log is kept on an XL file.

The algorithm uses a wide variety of screeners to identify and select the right stocks which have the maximum sucess rate.

## Get Started
1. Navigate to the folder where "dashboard.py" is located using the terminal
2. Type the following command: "streamlit run dashboard.py"
3. The GUI should now open on your browser and run locally
4. Follow the instructions presented to you on the dashboard

## Additional instructions:
* To backtest your own strategy on any ticker use "terminal_backtest_stock.py" or "terminal_backtest_crypto.py"
* "main.py" simply contains primary functions used on "dashboard.py"
* Streamlit, API the front end is built upon, uses HTML, CSS and JS to run python code locally on your web browser

## APIs' Used
* Beautiful soup
* AlphaVantage
* Pandas
* openyxl
* csv
* finnhub
* datetime
* time
* smtplib
* pytz
* email.message
* email.mime
* streamlit
* matplotlib

## Future Features
1. Mobile app
2. User customized trading algorithm that does not require code
3. Secure login page for the web and mobile app

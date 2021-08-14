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

## Future Features
1. Mobile app
2. User customized trading algorithm that does not require code

## API Info
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

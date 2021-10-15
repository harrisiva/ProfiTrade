# ProfiTrade
A fintech application that automates trading relative to the users' risk tolerance built entirely using Python in the span of 48 hours.

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

## Displayed Skills
* Web Scraping
* Data Frame
* Conditoinal Operations
* Object Oriented Programing
* Application Programming Interface
* Data Mining
* Basic Error Handling

## UI
![1](https://user-images.githubusercontent.com/76477563/137539648-67eeb70f-2af9-465d-9edf-8e62dc5de5b4.PNG)
![2](https://user-images.githubusercontent.com/76477563/137539666-6bd9935f-a1f6-4103-9612-407d6f4424a3.PNG)
![3](https://user-images.githubusercontent.com/76477563/137539685-3e9f76e8-cdeb-47bb-8fba-fcc8f9ae4370.PNG)
![4](https://user-images.githubusercontent.com/76477563/137539706-323f90c7-32b4-4bad-8a6d-0d8299a90d09.PNG)
![6](https://user-images.githubusercontent.com/76477563/137539723-97195255-148c-409f-943e-9bc2eb5aeef9.PNG)

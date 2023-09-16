import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def get_stock_info(stock):

    #stock info
    stock_ticker = yf.Ticker(stock)
    # stock = "AAPL"

    #current price
    current_price = stock_ticker.history(period="1d")["Close"].iloc[0]

    #historical data
    end_date = datetime.now().strftime('%Y-%m-%d')
    historical_data = stock_ticker.history(period='max',end=end_date,interval='3mo')

    #High
    year_high = stock_ticker.info["fiftyTwoWeekHigh"]

    #Low
    year_low = stock_ticker.info["fiftyTwoWeekLow"]

    #market cap
    market_cap = stock_ticker.info["marketCap"]

    data = yf.download(stock,'2022-09-16','2023-09-15')
    print(type(data))
    # data['Adj Close'].plot()
    # plt.show()

    # print(stock_dict)

    stock_dict = {'stock ticker': stock, 'current price': current_price, '52 week high': year_high, 
                  '52 week low': year_low, 'market cap': market_cap, 'past_year': data['Open'].values.tolist()}
    return stock_dict
    
# print(get_stock_info('META'))
# plt.plot(get_stock_info('META')['past_year'])
# plt.show()
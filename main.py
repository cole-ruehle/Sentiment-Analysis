from flask import Flask, render_template, jsonify

from stock_info import get_stock_info

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/top_bottom')
def get_best_worst():
   pass

@app.route('/reddit_sent')
def get_reddit_sent():
   pass

@app.route('/get_ticker_info/<ticker>')
def get_info(ticker):
   info_dict = get_stock_info(ticker)
   res = jsonify(info_dict)
   res.headers.add('Access-Control-Allow-Origin', '*')
   return res



if __name__ == '__main__':
   app.run()
from flask import Flask, render_template, jsonify
import json

from stock_info import get_stock_info
result_file = open('result_all.json')
result_dict = json.load(result_file)
result_list = []
for key, value in result_dict.items():
   if value[1] > 0:
      result_list.append((key, value[0] / value[1]))
result_list = sorted(result_list, key=lambda x: x[1])

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/top_bottom')
def get_best_worst():
   res = {'best': result_list[-10:], 'worst': result_list[:10]}
   res = jsonify(res)
   res.headers.add('Access-Control-Allow-Origin', '*')
   return res

@app.route('/reddit_sent')
def get_reddit_sent():
   pass

@app.route('/get_ticker_info/<ticker>')
def get_info(ticker):
   info_dict = get_stock_info(ticker)
   if result_dict[ticker][1] > 0:
      info_dict['sentiment'] = result_dict[ticker][0] / result_dict[ticker][1]
   else:
      info_dict['sentiment'] = -1
   res = jsonify(info_dict)
   res.headers.add('Access-Control-Allow-Origin', '*')
   return res



if __name__ == '__main__':
   app.run()
import os
import openai
from tqdm import tqdm
import json
from base64 import b64decode
from pathlib import Path
import json
import pandas as pd
openai.api_key = "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" #ask cole before using this, or replace with your own key.
import json

comp_table_temp = pd.read_csv('company_table.csv')
key = comp_table_temp['key'].tolist()
values = comp_table_temp['value'].tolist()
values2=[]
for value in values:
    value = value.replace("{","")
    value = value.replace("}","")
    value = value.replace("\'", "")

    value = set(value.split(","))
    values2.append(value)

company_table = dict(zip(key, values2))
print(type(values2[0]))

def filter_posts(post):
    output = []
    for ticker, name_set in company_table.items():
        # print(type(name_set))
        for sentence in post['title']:
            sentence_combined = ''.join(sentence)
            if any([x in sentence_combined for x in name_set]):
                output.append((ticker,sentence))
                break
            
        for sentence in post['text']:
            if any([x in sentence_combined for x in name_set]):
                output.append((ticker,sentence))
                break
    return output

def get_sentiment(text):
    content = f" Classes: [`positive`, 'very positive', 'very negative', `negative`, `neutral`] Text:{text} Classify the text into one of the above classes."
    response = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        temperature= 0.6,
        messages = [{
            "role": "user", "content": content}],
        max_tokens = 100,
    )
    sentiment = response.choices[0].message["content"].replace("Class: ", "")
    if sentiment == "very negative":
        return 0
    elif sentiment =="negative":
        return 0.25
    elif sentiment == "neutral":
        return 0.5
    elif sentiment == "positive":
        return 0.75
    elif sentiment == "very positive":
        return 1
    return None



if __name__ == "__main__":
    #Import list
    
    #Identify strings with companies,. 
    analysis_text = []
    sentement_dict = {}
    for ticker, sentence in analysis_text:
        temp = sentement_dict.setdefault(ticker, (0,0))
        sentiment = get_sentiment(sentence)
        if sentiment:
            temp = (temp[0]+sentiment, temp[1]+1)
        sentement_dict[ticker] = temp
    with open('result.json', 'w') as fp:
        json.dump(sentement_dict, fp)

    bad_test_string= "I fucking hate this"
    happy_test_string ="Recently noticed that TSM has been downtrodden, however it still seems undervalued to me at a glance sitting at a P/E of 15. Just curious about everyones thoughts on TSM and the possible dangers that investing in the company may pose, ignoring the obvious Geopolitical issues with being located in Taiwan, and the threat of China. Other then that what other issues are pushing this stock down?d"
    print(get_sentiment(happy_test_string))
    
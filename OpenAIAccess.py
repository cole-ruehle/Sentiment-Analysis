import os
import openai
from tqdm import tqdm
import json
from base64 import b64decode
from pathlib import Path

openai.api_key = "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" #ask cole before using this, or replace with your own key.


def filter_posts(post):
    output = []
    for ticker, phrase1, phrase2  in company_table:
        for sentence in post.title:
            if phrase1 in sentence or phrase2 in sentence or ticker in sentence:
                output.append((ticker,sentence))
                break
            
        for sentence in post.text:
            if phrase1 in sentence or phrase2 in sentence or ticker in sentence:
                output.append((ticker,sentence))
                break
            
                



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
    print(get_sentiment(bad_test_string))
    
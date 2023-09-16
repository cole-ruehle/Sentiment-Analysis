from OpenAIAccess import filter_posts, get_sentiment
import json
from tqdm import tqdm

reddit_file = open('reddit_sentences_all.json')
reddit_data = json.load(reddit_file)

analysis_text = []

for post in reddit_data:
    filtered = filter_posts(post)
    analysis_text += filtered
    # break

print((analysis_text))

with open('analysis_text.json', 'w') as fp:
    json.dump(analysis_text, fp)

sentement_dict = {}
i = 0
for ticker, sentence in tqdm(analysis_text):
    temp = sentement_dict.setdefault(ticker, (0,0))
    sentiment = get_sentiment(sentence)
    if sentiment:
        temp = (temp[0]+sentiment, temp[1]+1)
    sentement_dict[ticker] = temp
    if i % 10 == 0:
        with open('result_all.json', 'w') as fp:
            json.dump(sentement_dict, fp)
    i += 1


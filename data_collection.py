import praw
import json
import re
from nltk import tokenize

reddit = praw.Reddit(
    client_id="duKrwJVKWB0I5yvfDY_pKg",
    client_secret="dls3zcNCTgDxuyzT52rnKTxAZiDMWA",
    user_agent="android:com.example.myredditapp:v1.2.3 (by u/kemitche)",
)

output = []
for submission in reddit.subreddit("stocks+wallstreetbets").top(time_filter="month", limit=2000):
    # print(re.split(".|?|!", submission.title))
    print(re.split(". | ? | !",submission.selftext))

    output.append({"title": tokenize.sent_tokenize(submission.title), "text": tokenize.sent_tokenize(submission.selftext)})

out_file = open("reddit_sentences_all.json", "w")
json.dump(output, out_file)
out_file.close()
    # for comment in submission.comments[:10]:
    #     print(comment.body)

import os
import openai
from tqdm import tqdm
import json
from base64 import b64decode
from pathlib import Path
import pandas as pd

openai.api_key = "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"

def get_common_name(text):
    content = f"Text:{text} Provide me with the name that people normally call this company in one or 2 words. The response must be under 3 words!!!!"
    content = f"Text:{text} What is this company's common name. Use one or two words only"

    response = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        temperature= 0.6,
        messages = [{
            "role": "user", "content": content}],
        max_tokens = 25,
    )
    
    return response.choices[0]["message"]["content"]

companies = pd.read_csv("Final_combined_tickers.csv")
security_names = companies["Security Name"].tolist()
common_names = {}

for i, company in tqdm(enumerate(security_names)):
    if i<96:
        continue
    common_names[i] = (get_common_name(company))
    j =0 
    while  any(x in bad_names for x in common_names[i].split()) and j <10 :
        common_names[i] = get_common_name(company)
        j+=1
    if j == 10:
        common_names[i] = ""
]



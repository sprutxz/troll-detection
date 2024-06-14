import pandas as pd
from langdetect import detect
import re

dataset = pd.read_csv('datasets/metootweets.csv', on_bad_lines='skip')

# dropping empty rows
dataset.dropna(subset=['text'], inplace=True)

# dropping columns with majority empty values
dataset.drop(columns=['lastcontactdate',
                      'lasttimelinepull',
                      'lasttimetweetsanalyzed',
                      'numberoftweetsanalysed',
                      'numberoftweetsabouthash',
                      'actualtwitterdate'], inplace=True)

# Finding links in 'text', adding them to a new column, and removing them from 'text'
url_pattern = re.compile(r"(?:(?:https?://)?pic.twitter.com/|https?://t\S+|https?://\S+)")

dataset['link_type'] = 'None'

for index, value in dataset['text'].items():
    urls = url_pattern.findall(value)
    for url in urls:
        if re.match(r"https?://t\S+", url):
            dataset.at[index, 'link_type'] = 'tweet_link'
        elif re.match(r"(?:https?://)?pic.twitter.com/", url):
            dataset.at[index, 'link_type'] = 'picture_link'
        elif re.match(r"https?://\S+", url):
            dataset.at[index, 'link_type'] = 'other_link'
            
    if len(urls) == 0:
            dataset.at[index, 'link_type'] = 'no_link'
            
for index, value in dataset['text'].items():
    dataset.at[index, 'text'] = url_pattern.sub('', value)
    
for index, value in dataset['text'].items():
    dataset.at[index, 'text'] = re.sub(r"RT @\w+:", '', value)
    
# dropping rows that are not english or only contain whitespace
for index, value in dataset['text'].items():
    try:
        if detect(value) != 'en':
            dataset.drop(index, inplace=True)
    except Exception as e:
        print(f"{e} at {index}: {value}")
        dataset.drop(index, inplace=True)

dataset.to_csv('datasets/cleaned/metootweets-cleaned.csv', index=False)
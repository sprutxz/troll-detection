import pandas as pd
import re

dataset = pd.read_csv('../datasets/wh-tweets/WHtweets.csv')

#dropping columns with majority NA values
for column in dataset.columns:
    if (dataset[column].isna().sum()):
        dataset.drop(columns = [column], inplace=True)
        
        
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


# removing emojis
emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002500-\U00002BEF"  # chinese char
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            u"\U0001f926-\U0001f937"
                            u"\U00010000-\U0010ffff"
                            u"\u2640-\u2642"
                            u"\u2600-\u2B55"
                            u"\u200d"
                            u"\u23cf"
                            u"\u23e9"
                            u"\u231a"
                            u"\ufe0f"  # dingbats
                            u"\u3030"
                            u"\u2190-\u21FF"  # Arrows
                            "]+", flags=re.UNICODE)

for index, value in dataset['text'].items():
    dataset.at[index, 'text'] = emoji_pattern.sub('', value)

# dropping columns that are not required
dataset.drop(columns = ['source', 'timestamp'], inplace=True)

dataset.to_csv('datasets/cleaned/WHtweets-cleaned.csv', index=False)
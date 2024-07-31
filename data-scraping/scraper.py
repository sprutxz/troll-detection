from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_tweets(username, max_scrolls=5):
    # Set up Selenium WebDriver with options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open the Twitter page
    url = f'https://twitter.com/{username}'
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    # Scroll to load more tweets
    scrolls = 0
    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the new content to load
        scrolls += 1

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extract tweets
    tweets = []
    for tweet in soup.find_all('div', {'data-testid': 'tweet'}):
        tweet_text = tweet.find('div', {'lang': True})
        if tweet_text:
            tweets.append(tweet_text.text)

    return tweets

# Usage
twitter_handle = 'twitter_handle'  # Replace with the target user's handle
tweets = scrape_tweets(twitter_handle, max_scrolls=5)

# Output tweets
for i, tweet in enumerate(tweets, 1):
    print(f"{i}: {tweet}")

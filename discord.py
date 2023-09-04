import os
import openai
import time 

from parse_twitter import ParseTwitter
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv

class TwitterToDiscord:

    def __init__(self, webhook_url, users, tweets):
        load_dotenv()
        openai.organization = "org-zeOV533K5hdpS1CFEc4Ph8Mh"
        openai.api_key = os.getenv("OPENAI_KEY")
        
        self.tweets = tweets
        self.webhook_url = webhook_url
        self.users = users
        self.get_user_tweets()

    def get_user_tweets(self):
        for user in self.users:
            parser = ParseTwitter(user)
            parser.initAction(parser.getLastTweetAction)
            
            tweet_url = parser.tweet_info["tweet_url"]
            tweet_text = parser.tweet_info["text"]
            tweet_date = parser.tweet_info["date"]

            # only fwd tweets not in dict & only after dict is initialized w/ n items
            if tweet_text and tweet_url and not self.tweets.get(tweet_url):
                self.tweets[tweet_url] = True
                if len(self.tweets) >= len(self.users):
                    print(datetime.now())
                    print(f"FORWARDING CONTENT -- USER: {user}")
                    self.fwd_tweet(tweet_url)
                    self.fwd_tweet(self.ask_gpt(tweet_text))


    def ask_gpt(self, tweet_text):
        prompt = "Elaborate on people mentioned in the following tweet and expand any acronyms. \
                 Don't summarize or rephrase the content. Be as concise as possible. \
                 Use bullet points in your reply: \n\n"
        messages = [{"role": "user", "content": prompt + tweet_text}]
        
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except: 
            print("ChatGPT API endpoint failure\n")
            return ''

        return chat.choices[0].message.content
                   

    def fwd_tweet(self, content):
        print(f"CONTENT:\n {content}\n")
        DiscordWebhook(url=self.webhook_url, content=content).execute()

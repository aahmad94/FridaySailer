from parse_twitter import ParseTwitter
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

class TwitterToDiscord:
    def __init__(self, webhook_url, users, tweets):
        self.tweets = tweets
        self.webhook_url = webhook_url
        self.users = users
        self.get_user_tweets()

    def get_user_tweets(self):
        for user in self.users:
            tweet = ParseTwitter(user)
            tweet.initAction(tweet.getLastTweetAction)
            
            tweet_url = tweet.tweet_info["tweet_url"]
            tweet_date = tweet.tweet_info["date"]
            content = tweet.tweet_info["text"]

            # format text content to send
            content = None
            if tweet_url:
                content = user + f" {tweet_date}" + \
                    "\n" + tweet_text + "\n\n" + tweet_url + "\n"
                print(content)
                print("-------------------------------------------------")

            # only fwd tweets not in dict & only after dict is initialized w/ n items
            if tweet_url and not self.tweets.get(tweet_url):
                self.tweets[tweet_url] = True
                if len(self.tweets) > len(self.users):
                    self.fwd_tweet(user, tweet_date, content)

                   
    def fwd_tweet(self, user, tweet_date, content):
        date = datetime.now()
        month = date.strftime('%b')
        last_month = (date - timedelta(days=30)).strftime('%b')

        # if posted within last few hours, tweet won't have month in header
        if month not in tweet_date and last_month not in tweet_date:
            print(f"forwarding tweet -- user: {user}, date: {tweet_date}")
            webhook = DiscordWebhook(url=self.webhook_url, content=content)
            webhook.execute()



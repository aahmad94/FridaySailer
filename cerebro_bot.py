import time

from discord import TwitterToDiscord

with open('assets/webhook_urls.txt', 'r') as file:
    file_contents = file.read()

cerebro_index = file_contents.find('cerebro_url=')
# fridaysailer_index = file_contents.find('fridaysailer_url=')

cerebro_webhook_url = file_contents[cerebro_index + len('cerebro_url='):].split('\n', 1)[0]
# fridaysailer_url = file_contents[fridaysailer_index +
                            #  len('fridaysailer_url='):].split('\n', 1)[0]



cerebro_users = ["garyblack00", "sawyermerritt", "lizannsonders",
                 "unusual_whales", "elonmusk", "ICannot_Enough", "jpr007", "troyteslike", "marionawfal"]
friday_sailer_users = ["fridaysailer"]

while True:
    cerebro = TwitterToDiscord(cerebro_webhook_url, cerebro_users)
    fridaysailer = TwitterToDiscord(cerebro_webhook_url, friday_sailer_users)
    time.sleep(300)



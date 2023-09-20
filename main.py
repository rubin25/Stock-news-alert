import requests
import datetime
import math
from twilio.rest import Client

account_sid = YOUR TWILIO ACCOUNT SID
auth_token = YOUR TWILIO AUTH TOKEN

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API = "YOUR OWN API KEY FROM ALPHAVANTAGE"
NEWS_API = "YOUR OWN API KEY FROM NEWSAPI"

today = datetime.date.today()
yesterday = str(today - datetime.timedelta(days=1))
day_before_yesterday = str(today - datetime.timedelta(days=2))

stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API,
}
news_params = {
    "qInTitle":COMPANY_NAME,
    "apiKey": NEWS_API,
}

news_condition = False

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()
daily_data = [value for (key, value) in stock_data.items()]
yest_close_stock = float(daily_data[1][yesterday]["4. close"])

dby_close_stock = float(daily_data[1][day_before_yesterday]["4. close"])

close_stock_diff = abs(yest_close_stock-dby_close_stock)

percent_diff = (close_stock_diff/yest_close_stock)*100

if percent_diff> 0:
    news_condition=True
    graph = ""
if yest_close_stock-dby_close_stock>0:
    graph = f"{STOCK_NAME}: 🔺{math.floor(percent_diff)}%"
else:
    graph = f"{STOCK_NAME}: 🔻{math.floor(percent_diff)}%"

if news_condition:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    article_data = news_data["articles"][:3]
    article_title = [article["title"] for article in article_data]
    article_description = [article["description"] for article in article_data]
    client = Client(account_sid, auth_token)
    for i in range(len(article_title)):
        message = client.messages \
            .create(
            body=f"{graph}\n\rHeadline:{article_title[i]}\n\rBrief:{article_description[i]}",
            from_ = VIRTUAL_TWILIO_NUMBER,
            to = VERIFIED_NUMBER
        )

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import pandas as pd
import numpy as np
import time
import requests
import bs4
from bs4 import BeautifulSoup

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('9NhM9T/hqkfOTxe948TOcxfQ03ULDuEOLHU+5a8Sg+gn1RLi0WA5uLYyonllvsChQUX+QKtSfSIk+OJDK/6jzx7wJt4Vc4VZOeoVU5bX5nLkKVD8kmm8P1Uc43Y9i+U7PuOp+vRA1MBh12xC4EgC5QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c85380d3381de7083a760583b49e9bd6')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def get_pnd_ranking():
    url = "https://pad.skyozora.com/pets/statistics/"
    r = requests.get(url, timeout=20).text
    soup = BeautifulSoup(r, "html.parser")

    content = ""
    table = soup.find_all(name="table")[3]
    for i in range(20):
        trs = table.find_all(name="tr")[i+1]
        tds = trs.find_all(name="td")

        pet_name = tds[1].find(name="a").get("title")
        pet_name = pet_name.split("- ")[1]

        link = tds[1].find(name="a").get("href")
        link = "https://pad.skyozora.com/" + link

        review = tds[2].find_all(text=True)
        review = "".join(review)

        data = 'TOP{}\t{}\n'.format(i+1, pet_name)
        content += data

    content = "龍族拼圖玩家評分中整體評分最高的寵物\n\n" + content
    return content

def get_movie():
    url = "http://www.atmovies.com.tw/showtime/t04407/a04/"
    r = requests.get(url, timeout=20).text
    soup = BeautifulSoup(r, "html.parser")

    content = ""
    div = soup.find_all(name="li", attrs={"class": "filmTitle"})
    for i in range(len(div)):
        movie_name = div[i].find(name="a").string
        data = "{}\t{}\n".format(i+1, movie_name)
        content += data
        
    content = "台中大遠百威秀影城\n\n" + content
    return content

def get_currency():
    url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
    r = requests.get(url, timeout=20).text
    soup = BeautifulSoup(r, "html.parser")
    
    update_time = soup.find(name="span", attrs={"class": "time"}).string
    table = soup.find(name="table", attrs={"class": "table table-striped table-bordered table-condensed table-hover"})
    td1 = table.find_all(name="td", attrs={"class": "currency phone-small-font"})
    td2 = table.find_all(name="td", attrs={"data-table": "本行現金賣出"})
    
    content = ""
    for i in range(len(td1)):
        cur = td1[i].find(name="div", attrs={"class": "visible-phone print_hide"}).string
        cur = cur.replace(" ", "").replace("\n", "")
        price = td2[2*i].string

        data = "{}\t{}\n".format(str(cur), str(price))
        content += data
        
    content = "牌價最新掛牌時間：{}\n\n".format(update_time) + content
        
    return content

def get_github():
    url = "https://github.com/penguinwang96825?tab=repositories"
    r = requests.get(url, timeout=20).text
    soup = BeautifulSoup(r, "html.parser")
    rl = soup.find(name="div", attrs={"id": "user-repositories-list"})
    rl = rl.find_all(name="li", attrs={"class": "col-12 d-flex width-full py-4 border-bottom public source"})

    content = ""
    for i in range(len(rl)):
        repository = rl[i].find(name="a").string
        repository = repository.replace(" ", "").replace("\n", "")

        link = rl[i].find(name="a").get("href")
        link = "https://github.com/" + link

        data = "{}. {}:\n{}\n".format(i+1, repository, link)
        content += data
        
    return content

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text.lower() == "pnd":
        content = get_pnd_ranking()
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if event.message.text.lower() == "movie":
        content = get_movie()
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if event.message.text.lower() == "currency":
        content = get_currency()
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if event.message.text.lower() == "github":
        content = get_github()
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    message = TextSendMessage(text="You can only type in the following:\n1. pnd\n2. movie\n3. currency\n4. github")
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

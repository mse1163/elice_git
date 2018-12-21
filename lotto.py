# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = "xoxp-506652758256-506881860785-508585051063-724279b1860346515fce5efa097f55bd"
slack_client_id = "506652758256.506928399521"
slack_client_secret = "6a162bd9a197c8bb890d9af61222c21c"
slack_verification = "oi995MXWgi9X1mQkBUj2JJqO"
sc = SlackClient(slack_token)

# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    
    #여기에 함수를 구현해봅시다.

    url = "https://comic.naver.com/webtoon/weekdayList.nhn?week="+text[16:19]

    req = urllib.request.Request(url)

    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    keywords=[]
    
    if "mon" in text:
        data = soup.find("div", class_="list_area daily_img")
        title = [dt_data.get_text().strip('\n') for dt_data in data.find_all("dt")]
        artist = [dd_data.get_text().strip('\n') for dd_data in data.find_all("dd", class_="desc")]
        score = [sc_data.get_text().strip('\n') for sc_data in data.find_all("strong")]
        #title.append(data.find_all("dt").get_text().strip('\n'))
        keywords.append("월요웹툰 순위\n")

        for i in range(10):
            if len(keywords) >= 11:
                break
            keywords.append(str(i+1)+"위 : "+ title[i] +" / "+ artist[i] + " / 평점 : " + score[i] )

    elif "tue" in text:
        
        data = soup.find("div", class_="list_area daily_img")
        title = [dt_data.get_text().strip('\n') for dt_data in data.find_all("dt")]
        artist = [dd_data.get_text().strip('\n') for dd_data in data.find_all("dd", class_="desc")]
        score = [sc_data.get_text().strip('\n') for sc_data in data.find_all("strong")]
        keywords.append("화요웹툰 순위\n")
    
        for i in range(10):
            if len(keywords) >= 11:
                break
            keywords.append(str(i+1)+"위 : "+ title[i] +" / "+ artist[i] + " / 평점 : " + score[i] )

    elif "wed" in text:
        data = soup.find("div", class_="list_area daily_img")
        title = [dt_data.get_text().strip('\n') for dt_data in data.find_all("dt")]
        artist = [dd_data.get_text().strip('\n') for dd_data in data.find_all("dd", class_="desc")]
        score = [sc_data.get_text().strip('\n') for sc_data in data.find_all("strong")]
        keywords.append("수요웹툰 순위\n")
    
        for i in range(10):
            if len(keywords) >= 11:
                break
            keywords.append(str(i+1)+"위 : "+ title[i] +" / "+ artist[i] + " / 평점 : " + score[i] )

    elif "thu" in text:
        data = soup.find("div", class_="list_area daily_img")
        title = [dt_data.get_text().strip('\n') for dt_data in data.find_all("dt")]
        artist = [dd_data.get_text().strip('\n') for dd_data in data.find_all("dd", class_="desc")]
        score = [sc_data.get_text().strip('\n') for sc_data in data.find_all("strong")]
        keywords.append("목요웹툰 순위\n")
    
        for i in range(10):
            if len(keywords) >= 11:
                break
            keywords.append(str(i+1)+"위 : "+ title[i] +" / "+ artist[i] + " / 평점 : " + score[i] )

    elif "fri" in text:
        data = soup.find("div", class_="list_area daily_img")
        title = [dt_data.get_text().strip('\n') for dt_data in data.find_all("dt")]
        artist = [dd_data.get_text().strip('\n') for dd_data in data.find_all("dd", class_="desc")]
        score = [sc_data.get_text().strip('\n') for sc_data in data.find_all("strong")]
        keywords.append("금요웹툰 순위\n")
    
        for i in range(10):
            if len(keywords) >= 11:
                break
            keywords.append(str(i+1)+"위 : "+ title[i] +" / "+ artist[i] + " / 평점 : " + score[i] )

    elif "sat" in text:
        data = soup.find("div", class_="list_area daily_img")
        title = [dt_data.get_text().strip('\n') for dt_data in data.find_all("dt")]
        artist = [dd_data.get_text().strip('\n') for dd_data in data.find_all("dd", class_="desc")]
        score = [sc_data.get_text().strip('\n') for sc_data in data.find_all("strong")]
        keywords.append("토요웹툰 순위\n")
    
        for i in range(10):
            if len(keywords) >= 11:
                break
            keywords.append(str(i+1)+"위 : "+ title[i] +" / "+ artist[i] + " / 평점 : " + score[i] )
    elif "sun" in text:
        data = soup.find("div", class_="list_area daily_img")
        title = [dt_data.get_text().strip('\n') for dt_data in data.find_all("dt")]
        artist = [dd_data.get_text().strip('\n') for dd_data in data.find_all("dd", class_="desc")]
        score = [sc_data.get_text().strip('\n') for sc_data in data.find_all("strong")]
        keywords.append("일요웹툰 순위\n")
    
        for i in range(10):
            if len(keywords) >= 11:
                break
            keywords.append(str(i+1)+"위 : "+ title[i] +" / "+ artist[i] + " / 평점 : " + score[i] )
   # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)

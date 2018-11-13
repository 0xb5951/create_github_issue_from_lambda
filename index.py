import json
import os
import logging
import requests
from urllib.request import urlopen, Request
from urllib.parse import parse_qs

from post_message_to_slack import post_message_to_slack

# lambda function
def lambda_handler(event, content):
    print(event)
    token = os.environ["GITHUB_ACCESS_TOKEN"]
    print(token)
    create_issue = {
    "title": "Found a bug",
    "body": "create test issue.", #issueの中身
    "assignee": "", #assigneeの設定
    # "milestone": "", #指定した番号のマイルストーンを設定
    "labels": [] #ラベルの指定
    }

    bot_name = 'slack_tenki'
    msg = "slackとgithubが正しくつながってるよ！"

    post_message_to_slack(msg, event["event"]["channel"])

    url = "https://api.github.com/repos/odrum428/create_github_issue_from_lambda/issues?access_token=" + token
    print(url)
    res = requests.post(url, create_issue)
    print(res)

    # url = "http://api.github.com/repos/:user/:reponame/issues"
    response = {
    'statusCode': 200,
    'body': msg
    }

    return response

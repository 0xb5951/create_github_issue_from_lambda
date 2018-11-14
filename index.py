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
    create_issue = {
    "title": "Found a bug",
    "body": "create test issue." #issueの中身
    }
    params = json.dumps(create_issue)

    bot_name = 'slack_tenki'

    url = "https://api.github.com/repos/odrum428/create_github_issue_from_lambda/issues?access_token=" + token
    res = requests.post(url, params)
    if (res.status_code == 201) {
        msg = "issueを作成したよ！"
    } else
        msg = "エラーが起こってるよ.ログを確認してみてね。"
        print(res.text)
    }
    post_message_to_slack(msg, event["event"]["channel"])
    # url = "http://api.github.com/repos/:user/:reponame/issues"
    # response = {
    # 'statusCode': 200,
    # 'body': msg
    # }

    return res.status_code

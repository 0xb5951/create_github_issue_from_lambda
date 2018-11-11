import json
import os
import livedoor_tenki
import logging
from urllib.request import urlopen, Request
from urllib.parse import parse_qs

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# lambda function
def lambda_handler(event, content):
    #受け取った情報をCloud Watchログに出力
    logging.info(json.dumps(event, indent=4))
    print(event)
    token = os.environ.get("SLACK_TOKEN")

    bot_name = 'slack_tenki'

    response = {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

    msg = "slackとgithubが正しくつながってるよ！"

    # Slackにメッセージを投稿する
    post_message_to_slack_channel(msg, event["event"]["channel"])

    return response

def post_message_to_slack_channel(message: str, channel: str):
    # Slackのchat.postMessage APIを利用して投稿する
    # ヘッダーにはコンテンツタイプとボット認証トークンを付与する
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    data = {
        "token": os.environ["SLACK_APP_AUTH_TOKEN"],
        "channel": channel,
        "text": message
    }
    req = Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    urlopen(req)
    return

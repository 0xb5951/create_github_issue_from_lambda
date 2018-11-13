from urllib.request import urlopen, Request
import json
import os

def post_message_to_slack(message: str, channel: str):
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

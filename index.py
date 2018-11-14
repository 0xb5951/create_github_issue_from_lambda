import json
import os
import logging
import requests
from urllib.request import urlopen, Request
from urllib.parse import parse_qs

from post_message_to_slack import post_message_to_slack
from controll_github_info import setting,getting

#lambda function
def lambda_handler(event, content):
    print(event)
    token = os.environ["GITHUB_ACCESS_TOKEN"]

    # slackからの投稿を slack_input_text へ格納
    slack_text = str(event["event"]["text"]).split()
    print(slack_text)
    title = slack_text[1]

    if title == "setting":
        owner = slack_text[2]
        repo = slack_text[3]
        setting(owner, repo)

    if not getting():
        msg = "GitHubの情報が登録されてないよ！ownerとRepository情報を登録してね。\n" \
        "このボットに以下の形でメンションを飛ばしてね.\n" \
        "setting REPOSITORY_OWNER REPOSITORY_NAME"
        post_message_to_slack(msg, event["event"]["channel"])
        return
    else:
        github_info = getting()
        owner = github_info[0]
        repo = github_info[1]

        msg = "Issueの作成先" + "\n" + "owner:" + owner + "\n" + "repo:" + repo
        post_message_to_slack(msg, event["event"]["channel"])

        url = "https://api.github.com/repos/" + owner + "/" + repo+ "/issues?access_token=" + token
        print(url)

        title = slack_text[1]
        body = slack_text[2]

        create_issue = {
        "title": str(title),
        "body": str(body)
        }

        params = json.dumps(create_issue)
        print(params)
    # res = requests.post(url, params)
    # print(res)
    # print(res.text)
    #
    # if res.status_code == 201:
    #     msg = "issueを作成したよ！"
    # else:
    #     msg = "エラーが起こってるよ.ログを確認してみてね。"

    msg = "動作テストだよ！"
    post_message_to_slack(msg, event["event"]["channel"])
    # url = "http://api.github.com/repos/:user/:reponame/issues"
    # response = {
    # 'statusCode': 200,
    # 'body': msg
    # }

    return res.status_code

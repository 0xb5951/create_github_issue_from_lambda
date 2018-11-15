import json
import os
import logging
import requests
from urllib.request import urlopen, Request
from urllib.parse import parse_qs

from post_message_to_slack import post_message_to_slack
from controll_dynamodb import write_dynamodb,read_dynamodb,update_dynamodb

#lambda function
def lambda_handler(event, content):
    print(event)
    token = os.environ["GITHUB_ACCESS_TOKEN"]

    # slackからの投稿を slack_input_text へ格納
    slack_text = str(event["event"]["text"]).split()
    print(slack_text)
    command = slack_text[1]

    if command == "setting":
        title = slack_text[2]
        owner = slack_text[3]
        repo = slack_text[4]
        body = ""
        for text in slack_text[5:]:
            body += text
            body += '\n'

        print(title, owner, repo, body)
        write_dynamodb(title, owner, repo, body)

    elif command == "update":
        title = slack_text[2]
        owner = slack_text[3]
        repo = slack_text[4]
        body = ""
        for text in slack_text[5:]:
            body += text
            body += '\n'

        print(title, owner, repo, body)
        update_dynamodb(title, owner, repo, body)


    elif command == "create":
        title = slack_text[2]
        owner = slack_text[3]
        res = read_dynamodb(title, owner)


        # if not getting():
        #     msg = "GitHubの情報が登録されてないよ！ownerとRepository情報を登録してね。\n" \
        #     "このボットに以下の形でメンションを飛ばしてね.\n" \
        #     "setting REPOSITORY_OWNER REPOSITORY_NAME"
        #     post_message_to_slack(msg, event["event"]["channel"])
        #     return

        print(res)
        msg = "Issueの作成先" + "\n" + "owner:" + res[0]['owner'] + "\n" + "repo:" + res[0]['repo']
        post_message_to_slack(msg, event["event"]["channel"])

        url = "https://api.github.com/repos/" + res[0]['owner'] + "/" + res[0]['repo'] + "/issues?access_token=" + token
        print(url)

        create_issue = {
        "title": res[0]['title'],
        "body": res[0]['body'],
        # 'label': [] # お好みでlabelをつけて下さい
        }

        params = json.dumps(create_issue)
        print(params)
        ret = requests.post(url, params)
        print(ret)

        if ret.status_code == 201:
            msg = "issueを作成したよ！"
        else:
            msg = "エラーが起こってるよ.ログを確認してみてね。"


        post_message_to_slack(msg, event["event"]["channel"])

        return ret.status_code

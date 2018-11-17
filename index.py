import json
import os
import logging
import requests
from urllib.request import urlopen, Request
from urllib.parse import parse_qs

from post_message_to_slack import post_message_to_slack
from controll_dynamodb import write_dynamodb,read_dynamodb,update_dynamodb,get_issue_list

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

    elif command == "get_issue_list":
        issue_list = get_issue_list()
        count = 0
        msg = []

        for issue in issue_list:
            print(issue.items())
            msg += issue.items()

        post_message_to_slack(msg, event["event"]["channel"])

    elif command == "help":
        msg = "*概要*\nSlackからIssueを作成できるBotだよ。定期的に作成するissueをこいつに任せると便利になるよ！\n" \
        "作成するissueの情報をDynamoDBに登録することで簡単にissueを作成できるよ！\n\n" \
        "*使い方*\nissue情報の登録: このボットにメンションを飛ばして各種情報を入力してね。issueの中身はスペース区切りに入力することで改行できるよ。\n" \
        "コマンド例 `@このボット setting Issueのタイトル 作成先のowner 作成先のリポジトリ issueの中身...`\n" \
        "ex. `@このボット setting Sampleisuue odrum428 create_github_issue_from_lambda ##目的 slackからissueを作成する`\n\n" \
        "issue情報の更新 : 基本的には登録の時と同じ。updateコマンドに変えるだけ。\n" \
        "コマンド例 `@このボット update Issueのタイトル 作成先のowner 作成先のリポジトリ issueの中身...`\n" \
        "ex. `@このボット update Sampleisuue odrum428 create_github_issue_from_lambda ##目的 slackからissueを作成する`\n\n" \
        "登録したissue一覧の取得 : get_issue_listとだけ入力すると取得できるよ。\n" \
        "コマンド例 `@このボット get_issue_list`\n" \
        "ex. `@このボット get_issue_list`\n\n" \
        "issueの作成 : 登録した情報を元にissueを作成するよ。DynamoDBに登録したissueのタイトルとowner情報が必要だよ。\n" \
        "コマンド例 `@このボット create isuueのタイトル 作成先のowner`\n" \
        "ex. `@このボット create Sampleissue odrum428`"

        post_message_to_slack(msg, event["event"]["channel"])


    elif command == "create":
        title = slack_text[2]
        owner = slack_text[3]
        res = read_dynamodb(title, owner)['Items'][0]
        if not res:
            msg = "Issueの情報が登録されてないよ！作成したいIssueの情報を登録してね。\n" \
            "*使い方*\nissue情報の登録: このボットにメンションを飛ばして各種情報を入力してね。issueの中身はスペース区切りに入力することで改行できるよ。\n" \
            "コマンド例 `@このボット setting Issueのタイトル 作成先のowner 作成先のリポジトリ issueの中身...`\n"
            post_message_to_slack(msg, event["event"]["channel"])
            return

        print(res)
        msg = "Issueの作成先" + "\n" + "owner:" + res['owner'] + "\n" + "repo:" + res['repo']
        post_message_to_slack(msg, event["event"]["channel"])

        post_url = "https://api.github.com/repos/" + res['owner'] + "/" + res['repo'] + "/issues?access_token=" + token

        create_issue = {
        "title": res['title'],
        "body": res['body'],
        # 'label': [] # お好みでlabelをつけて下さい
        }

        params = json.dumps(create_issue)
        ret = requests.post(post_url, params)
        ret_json = ret.json()

        print(ret_json)
        print(ret_json['html_url'])

        if ret.status_code == 201:
            msg = "issueを作成したよ！\n作成先のURL : " + ret_json['html_url']
        else:
            msg = "エラーが起こってるよ.ログを確認してみてね。"


        post_message_to_slack(msg, event["event"]["channel"])

        return ret.status_code

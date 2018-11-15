# 最初はlambda関数内にテキストファイルを用意して、そこにownerとrepoを保存させればいいと思った。
# しかし、lambda関数はステートレスなので、tmp領域は呼び出しごとに異なるし、設計としてイケてないと思った.
# そのため、issueを作るのに必要な諸々の情報はDynamoDBに書き込ませればいいってことに気づいたのでそっちに移す
# こっちは経緯を忘れないように残しておく。

from post_message_to_slack import post_message_to_slack

def setting(owner, repo):
    with open('/tmp/github_setting.txt', mode='w') as set_f: #withで開くと自動的にcloseされる
        set_f.write(owner)
        set_f.write('\n')
        set_f.write(repo)

def getting():
    with open('/tmp/github_setting.txt', mode='r') as set_f: #withで開くと自動的にcloseされる
        data = [v.rstrip('\n') for v in set_f.readlines()]
        print(data)
        return data

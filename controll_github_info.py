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

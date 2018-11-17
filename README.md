## 概要
slackから自動的にGitHubのissueを生成してくれるbot.
定期的に作成するIssueの情報をDynamoDBに保存しておき、ボットにメンションを飛ばすことでIssueを作成してくれるようになる。

## 必要なもの
- AWSアカウント
- GitHubのPersonal access token
- Slack API のOAuth Access TokenとBot User OAuth Access Token

## 使い方
- issue情報の登録: このボットにメンションを飛ばして各種情報を入力してね。issueの中身はスペース区切りに入力することで改行できるよ。
コマンド例 `@このボット setting Issueのタイトル 作成先のowner 作成先のリポジトリ issueの中身...`
ex. `@このボット setting Sampleisuue odrum428 create_github_issue_from_lambda ##目的 slackからissueを作成する`

- issue情報の更新 : 内容を更新したいIssueのtitleとownerを指定して、リポジトリとIssueの中身を変更できるよ！
コマンド例 `@このボット update Issueのタイトル 作成先のowner 作成先のリポジトリ issueの中身...`
ex. `@このボット update Sampleisuue odrum428 create_github_issue_from_lambda ##目的 slackからissueを作成する`

- 登録したissue一覧の取得 : get_issue_listとだけ入力すると取得できるよ。
コマンド例 `@このボット get_issue_list`
ex. `@このボット get_issue_list`

- issueの作成 : 登録した情報を元にissueを作成するよ。DynamoDBに登録したissueのタイトルとowner情報が必要だよ。
コマンド例 `@このボット create isuueのタイトル 作成先のowner`
ex. `@このボット create Sampleissue odrum428`"


## 導入
### GitHubからcloneしてくる。
```
git clone git@github.com:odrum428/create_github_issue_from_lambda.git
```

### GitHubトークンの取得
https://github.com/settings/tokens/new でアクセストークンを生成する。
適当にトークンの値をつけて、権限を与える。
今回与える権限は`repo`トークンを生成したら、メモっておく。

### プロジェクトファイル内だけをzip化してまとめる
プロジェクトファイルの中身だけをzipファイルにしておく。

## AWS
### IAMロールを作成する
ここからAWSの設定を行っていく。AWSに登録するところは割愛。 まずはambda関数にアクセス許可を与えるためにロールを作成する。
ロール名は適当につけてください。与える権限は以下の通り。
- AmazonDynamoDBFullAccess
- CloudWatchLogsFullAccess
- AmazonAPIGatewayAdministrator

### AWS Lambdaで関数を作成する
Lambdaに移動し、関数を作成する。  `関数の作成`を選択し、`一から関数を作成`を選ぶ。 ランタイムは`Python 3.6`.ロールは先ほど作成したロールを割り当てる。
例によって関数名は好きにつけてください。

ページが遷移したら、`関数コード`にある`コードエントリタイプ`の中から`.zipファイルをアップロード`を選択。 先ほど作成したzipファイルを選択し、アップロードする。

### API Gatewayの作成
`API Gateway`に移動し、`APIの作成`をクリック。
名前は...以下略.

作成完了後は、`アクション`から`メソッドの作成`をクリックし、POSTメソッドを選択。 設定はデフォルトで`Lambda関数`の部分を先ほど作成したLambda関数名を入力。

### API Gatewayのデプロイ
APIにアクセスできるようにするためにデプロイを行う。  `アクション`から`APIのデプロイ`を選択。  `デプロイされるステージ`は`新しいステージ`を選択し、適当な名前を付ける。

デプロイしたら、URLが表示されるので、コピーしておく。

## Slack側の設定
### Slack Botの作成

以下のURLにアクセスする。  
[https://api.slack.com/apps/](https://api.slack.com/apps/)

ここで`Create New App`か`Building start`を選択する。
 あらかじめワークスペースを持ってないとダメなのでない人はつくってください。 botの名前はお好きにどうぞ。

アプリを作成したら、ページが遷移するはず。 サイドメニューにある`Bot User`から`Add Bot User`をクリックし、Botを作成する。

### Eventの設定
サイドメニューにある`Event Subscriptions`をクリックし、`Enable Events`をオンにする。
`Request URL`に先ほどコピーしたAPI GatewayのURLを貼り付ける。

この時、Request URLの認証でエラーがでることがあるかもしれない。原因は対象のURLに対してPOSTされるChallengeパラメータがかえってきていないことが考えられる。
Request URLを登録するときにURLの動作確認として、以下のパラメータがURLに対してPOSTされる。
```
POST
"body": {
	 "type": "url_verification",
	 "token": "XXXXXXXXXXXXXXXXXXXXXXXXXXX",
	 "challenge": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx"
}
```

Slack APIはこの`challenge`パラメータがresponseとして正しくかえってきているかの確認を行っており、challengeをそのまま返す必要がある。
もし、このエラーが出た場合はindex内に`return event`を追記してやると`Verify`になると思う。

`Subscribe to Bot Events`以下の`Add Bot User Event`をクリックし、ボットへのメンションを意味する`app_mention`を選択し、  `Save Changes`をクリックして、保存する。

### Botをワークスペースに追加する
上記の設定が完了したら、Botをワークスペースに追加する。
`OAuth & Permissions`に移動し、`Install App`を選択する。
このページでSlackの認証に必要なトークンが書いてある。

## Lambdaの環境変数を設定する
Lambda内で以下の環境変数を設定する。

- GITHUB_ACCESS_TOKEN : GitHubのPersonal access token
- SLACK_OAUTH_ACCESS_TOKEN : SlackのOAuth Access Token
- SLACK_BOT_USER_ACCESS_TOKEN : SlackのBot User OAuth Access Token

## LICENSE
Copyright 2018 odrum428.

Licensed under the MIT License.

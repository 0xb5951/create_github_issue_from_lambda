# DynamoDBの処理をまとめて書いておく。

import boto3
from boto3.dynamodb.conditions import Key

def write_dynamodb(title, owner, repo, body):
    try:
        dynamoDB = boto3.resource("dynamodb")
        table = dynamoDB.Table("github_issue") # DynamoDBのテーブル名

        # DynamoDBへデータを書き込む
        res = table.put_item(
        Item = {
        "title": title, # primarykey : issueのタイトルを入れる
        "owner": owner, # sortedkey : owner情報を入れる
        "repo": repo,  # repositoryの名前
        "body": body # issueの中身を入れる
        }
        )
        return res
    except Exception as e:
        return e

def read_dynamodb(title, owner):
  try:
    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table("github_issue") # DynamoDBのテーブル名

    # DynamoDBからデータを持ってくる
    queryData = table.query(
      KeyConditionExpression = Key("title").eq(title) & Key("owner").eq(owner) # 取得するKey情報
    )
    return queryData
  except Exception as e:
      return e

def update_dynamodb(title, owner, repo, body):
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table('github_issue')
        res = table.update_item(
            Key = {
                'title': title,
                'owner': owner
            },
            AttributeUpdates = {
                'repo':{
                    'Action': 'PUT',
                    'Value': repo
                },
                'body':{
                    'Action': 'PUT',
                    'Value': body
                }
            }
        )
        return res
    except Exception as e:
        return e

def get_issue_list():
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table('github_issue')
        res = table.scan()['Items']

        return res
    except Exception as e:
        return e

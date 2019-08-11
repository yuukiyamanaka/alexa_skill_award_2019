# alexa_skill_award_2019
## セットアップ
開発には[ASK CLI](https://developer.amazon.com/ja/docs/smapi/ask-cli-command-reference.html)を利用します。
ASK CLIのセットアップの詳細は、[クイックスタート:ASK CLI](https://developer.amazon.com/ja/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html)を参照してください。
ASK CLIでは、
- skillの作成、開発
- skillのデプロイ
- skillのテスト
などがサポートされています。

### ASK CLIのインストール
```
npm install -g ask-sli
```
### ASK CLIを自分のアカウントとひもづける（デプロイ時に必要）
1. ASK CLIが、AWS Lambdaにデプロイするために、IAMユーザーを新規作成する
[AWSの資格情報とASK CLIとの関連付け](https://developer.amazon.com/ja/docs/smapi/set-up-credentials-for-an-amazon-web-services-account.html)を参考に作成する。
最終的にユーザーのアクセスキーとシークレットキーをゲットする（ask init時に使用）
ちょっとややこしい箇所なのでわからなければ聞いてください

2. ASK CLIの初期設定
以下のコマンドを実行する
```
ask init
```
先ほどゲットしたアクセスキーとシークレットキーの入力が必要。

### スキルのデプロイ
```
ask deploy
```
.ask/configファイルが更新されるはず。この更新されたファイルはgit commitしないように。

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

3. venvの作成
レポジトリをcloneしたあと、レポジトリのフォルダーの一つ上の階層に移動。
```
./alexa_skill_award_2019/hooks/post_new_hook.sh alexa_skill_award_2019 true
```
.venvフォルダが作成されていればok

### スキルのデプロイ
skill.jsonが置いてある階層で、
```
./hooks/pre_deploy_hook.sh alexa_skill_award_2019 true all && ask deploy 
```
lambda/py/lamnda_uploadフォルダが作成される。
また、.ask/configファイルが更新されるが、この更新されたファイルはgit commitしないように。

#### ブラウザ側での確認
- [Alexa Console](https://developer.amazon.com/alexa/console/ask)
- [AWS Console](https://us-west-2.console.aws.amazon.com/console/home)
AWS lambdaはオレゴン（us-west-2）でホストされている。Alaxa SkillとLambda Funcが作成されていることがわかる。

#### テスト
deployされた環境にCLIからアクセスしてテストすることができる。ローカルで実行されるわけではないので注意。
エラー情報などはCloudWatchでチェックできる。
```
ask dialog -l ja-JP
```
# Serverless, FaaS 概要
↓

+++

## serverless architecture ？
- 「 ~~サーバーが本当に不要~~ 」
- 「サーバーに直接アクセスしなくても仕事ができる」アーキテクチャ
- 究極の目標は、開発者がサーバーやインフラを気にかけずにコードに全力を注げるようにすること
- もたらす効果
    - スケールを気にしなくて良い（auto-scaling）
    - 従量課金

+++

### Serverless と FaaS の関係性

<img src="faas/presentation/assets/img/serverless_and_faas.png" width="50%">

+++

#### On-prem/IaaS/CaaS/PaaS/FaaS

<img src="faas/presentation/assets/img/faas_comparison.png" width="50%">

source: [Introduction to Serverless: What is Serverless?](https://www.youtube.com/watch?v=4caavWtJLfc&feature=share)

+++

## FaaS とは？

- 関数をコードで定義するだけ
- 使用した分だけ課金される
- イベントドリブン
- サーバダウンの概念がない
- ステートレスに書くのが通例
   - 何か保持するなら backend で


+++

<img src="faas/presentation/assets/img/lambda.png" width="20%">
### AWS Lambda
- 言わずと知れたKing of FaaS
- イベントドリブン(非常駐型)でコードを実行
- 実行されたリソース分の課金/オートスケール
- GITからデプロイはできない
- トリガーは自社サービスやSDKのみ

+++

<img src="faas/presentation/assets/img/apigw.png" width="20%">
### Amazon API Gateway
- API作成/管理サービス
- 流量制限や認証などを行う
- LambdaをAPI(HTTP)でリクエスト際は必須
- リクエスト数による従量課金/オートスケール
- 2015年7月サービス開始(Lambda GAから3ヵ月)

+++

<img src="faas/presentation/assets/img/dynamodb.png" width="20%">
### Amazon DynamoDB
- マネージドなNoSQLデータベース
- データは3か所のAZに保存
- データ容量の増加に応じた増設作業は不要
- 使った分だけの従量課金
- 2012年1月サービス開始

+++

<img src="faas/presentation/assets/img/cloudwatch.png" width="20%">
### Amazon CloudWatch
- AWSリソースの死活/性能/ログ監視
- 取得メトリックをグラフ化
- メトリックからアラーム等のアクションを設定可能
- 使った分だけの従量課金
- 2009年5月サービス開始

+++

#### (参考)主要4社比較
<img src="faas/presentation/assets/img/faas4.png" width="80%">

+++

以下、小ネタ

+++

### メテオフォール型開発
神の前ではウォーターフォールもアジャイルも通じないらしい
<img src="faas/presentation/assets/img/meteor-fall.png" width="80%">

- 参考: http://eiki.hatenablog.jp/entry/meteo_fall

+++

### 有効な手段
メテオフォール型開発には サーバレスが正義
![serverless-logo](faas/presentation/assets/img/serverless-logo.png)

- 参考: https://www.slideshare.net/ssuser084061/x-117338837

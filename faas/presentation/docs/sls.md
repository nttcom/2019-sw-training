# Serverless Framework でローカルからAWSにデプロイする場合
今までWebコンソールで苦労していたものが、一発で設定・デプロイ出来ます。 Infrastructure as Code!

## ハンズオン環境ごとに予め決めておくパラメータ
- 講師等の指示に従って以下のパラメータを決めてください:
    ```
    REGION: ____ (例: `シンガポール`, `ap-southeast-1`)
    PROFILE: ____ (`faas01` など )
    REGION: ____ (`faas01` など )
    ```

## ハンズオン手順
- ここでディレクトリとファイル解説
    ```
    backend/
    ├── README.md  # このファイル！
    ├── lambda_handler.py  # lambda function がトリガーされた時に最初に読まれるファイル
    ├── package.json  # sls自体が node.js 製なので必要なライブラリを
    ├── node_modules/  # node.js ライブラリの入る場所 (serverless framework 自身は node.js 製)
    ├── serverless.yml  # deploy等に必要な設定ファイル（これが sls のキモ）
    ├── migrations/  # 応用編のための
    ├── src/
    │   └── todo.py  # コアのロジックを書いたファイル（あんまり分離するボリュームじゃなかった）
    └── rf/  # robot framework でのテスト (参考程度)
    ```

- Installation: npm と pip で一通り使うものをインストールする (pip はテストのためのライブラリをいっぱい入れている)
    ```sh
    # faas/application/backend で作業
    $ npm install
    $ pip install boto3 pytest robotframework RESTinstance
    ```

- デプロイ
    ```sh
    # faas/application/backend で作業
    $ sls deploy --profile ${PROFILE} --stage ${STAGE} --region ${REGION}
      # パラメータは各自の環境に合わせて変更してね！
    ```

- 出力例 ( profile & stage: `demo`, region: `ap-southeast-1`, 解説を `# foobar` で )
    ```sh
    # faas/application/backend で作業
    $ sls deploy --profile demo --stage demo --region ap-southeast-1  # 実行！
    Serverless: Packaging service...
    Serverless: Excluding development dependencies...
    Serverless: Uploading CloudFormation file to S3...
    Serverless: Uploading artifacts...
    Serverless: Uploading service todo.zip file to S3 (1.73 KB)...
    Serverless: Validating template...
    Serverless: Updating Stack...
    Serverless: Checking Stack update progress...
    ..............
    Serverless: Stack update finished...  # ココまでくれば deploy 完了。 Congrats!
    Service Information
    service: todo
    stage: demo  # apigw stage name == profile name にしている
    region: ap-southeast-1  # ラクサ美味いよラクサ
    stack: todo-demo  # CloudFormation Stack name
    resources: 15
    api keys:
    None
    endpoints:  # 以下エンドポイントのURL報告して貰うかも。5つあることも確認
    GET - https://hogehoge.execute-api.ap-southeast-1.amazonaws.com/demo/tasks
    POST - https://hogehoge.execute-api.ap-southeast-1.amazonaws.com/demo/tasks
    GET - https://hogehoge.execute-api.ap-southeast-1.amazonaws.com/demo/tasks/{id}
    PUT - https://hogehoge.execute-api.ap-southeast-1.amazonaws.com/demo/tasks/{id}
    DELETE - https://hogehoge.execute-api.ap-southeast-1.amazonaws.com/demo/tasks/{id}
    functions:
    todo: todo-function-demo  # あなた用の Lambda function を探す時にここの名前で
    layers:
    None
    Serverless: Removing old service artifacts from S3...  # upload packege がたまりすぎないように rotate してる
    ```

- tips: デプロイでエラーが出たら `export SLS_DEBUG='*'` してデバッグメッセージを出す。 消すときは `export SLS_DEBUG=''`

- 動作確認の方法
    - postman/curl など API 自身を叩く
    - frontend アプリも動きます。

## Test
ユニットテスト、ローカルに AWS を再現することでテスト、更に robot framework を組み合わせて自動テスト、などのバリエーションを紹介する。

### Serverless Offline
ローカルに apigw, lambda, dynamodb をエミュレートして TDD できるお（完全おまけコンテンツ）

- java 1.8 以上をインストール
- 初回は dynamodb-local のインストールも必要
    ```sh
    # dynamodb-local をインストール
    $ sls dynamodb install --profile ${PROFILE} --stage ${STAGE} --region ${REGION}

    # もし何かの都合でやり直したい場合、 remove dynamodb-local
    $ sls dynamodb remove --profile ${PROFILE} --stage ${STAGE} --region ${REGION}
    ```

- execute sls offline
    ```sh
    $ sls offline start --profile ${PROFILE} --stage ${STAGE} --region ${REGION}
    ```

- これで、 http://127.0.0.1:3000 の配下に API のエンドポイントが生成され、裏ではlambda, dynamodb もエミュレートされる。 curl などで楽しんでください。

### Robot Framework でのテスト
rotob framework とその REST API 用の拡張である RESTinstance を用いれば、ローカルの API エンドポイントに対して受入試験のように動作確認が行える。
- ローカルでのテストのサンプルは以下:
    ```sh
    $ cd /path/to/backend/rf/1_sls_local/
    $ robot main.robot
    ```

### pytest によるユニットテスト
今回は lambda handler にパラメータを送り込んでテストを行う。

- serverlss offline が起動していること

- 環境変数を設定
    ```sh
    $ export REGION_NAME=${REGION}; export TABLE_NAME=todo-table-${STAGE}-sls
    ```

- テスト実行！
    ```sh
    $ pytest -v
    ```

- 出力例 (成功の場合):
    ```sh
    ============================= test session starts ==============================
    platform darwin -- Python 3.6.5, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
    cachedir: .pytest_cache
    rootdir: /Users/george/shugyo/2019-sw-training/faas/application/backend
    collected 7 items
    application/backend/tests/test_sls_offline.py::test_POST PASSED          [ 14%]
    application/backend/tests/test_sls_offline.py::test_GET_0 PASSED         [ 28%]
    application/backend/tests/test_sls_offline.py::test_PUT PASSED           [ 42%]
    application/backend/tests/test_sls_offline.py::test_GET_1 PASSED         [ 57%]
    application/backend/tests/test_sls_offline.py::test_LIST PASSED          [ 71%]
    application/backend/tests/test_sls_offline.py::test_DELETE_0 PASSED      [ 85%]
    application/backend/tests/test_sls_offline.py::test_GET_404 PASSED       [100%]
    =========================== 7 passed in 3.60 seconds ===========================
    ```

- note:
  event オブジェクト, 環境変数の設定 あたりが癖がある感じ。
  コード規模が大きくないので、 unit test が必ずしも必要とは限らない。また、 unit といいながら DynamoDB Local が必須だし、ちょっとハードル高めでは有る。
  本気で開発するときは pytest-watch を仕掛けて、 ファイル更新のたびに unit test が回るようにしておくとだいぶ素早く開発が進む。

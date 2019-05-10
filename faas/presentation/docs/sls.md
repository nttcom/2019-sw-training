### Serverless Framework でローカルからAWSにデプロイする場合
今までWebコンソールで苦労していたものが、一発で設定・デプロイ出来ます。 Infrastructure as Code!

- 重要な環境の情報
    ```
    profile: faasXX (XX 部分は自分の番号を確認)
    stage  : faasXX (XX 部分は自分の番号を確認)
    region : ap-southeast-1 (今回はシンガポールを全員共通にしました)
    ```

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

- デプロイ
    ```sh
    (このプロジェクトを git clone して faas/application/backend へ移動)
    $ sls deploy --profile faasXX --stage faasXX --region ap-southeast-1
      # パラメータは各自の環境に合わせて変更してね！
    ```

- 出力例 ( profile & stage: `demo`, region: `ap-southeast-1`, 解説を `# foobar` で )
    ```sh
    (このプロジェクトの faas/application/backend で作業)
    $ sls deploy --profile demo  # 実行！
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

### おまけ: Serverless Framework でローカルでテスト環境を立てる（ハンズオン範囲外）
ローカルでのテストも頑張ってみたい場合は、読んでね。ローカルに apigw, lambda, dynamodb をエミュレートして TDD できるお（完全おまけコンテンツ）

- java 1.8 以上をインストール
- 初回は dynamodb-local のインストールも必要
    ```sh
    # install dynamodb-local
    sls dynamodb install --profile <your_profile_name> --stage <your_profile_name> --region <our_region_name>
    # もし何かの都合でやり直したい場合、 remove dynamodb-local
    sls dynamodb remove --profile <your_profile_name> --stage <your_profile_name> --region <our_region_name>
    ```

- execute sls offline
    ```sh
    $ sls offline start --profile <your_profile_name> --stage <your_profile_name> --region <our_region_name>
    ```

- これで、 http://127.0.0.1:3000 の配下に API のエンドポイントが生成され、裏ではlambda, dynamodb もエミュレートされる。
- テスト方法は省略。
    - 単体テスト: ちょっとどこに対してやるのか難しいところ。 src/todo.py に対してテストを書くなどが現実的か。 lambda handler を直接叩くテストは結構難しい（event, contextを完全に再現することが難しい）
    - 結合テスト: API に対するテストをするのが良い。 robot framework 等
        ```sh
        cd rf/1_sls_local/
        robot main.robot
        ```


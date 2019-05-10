### AWS コンソールでひとつずつセットアップする場合
#### 前提
  - リージョン
    - 名称: `アジアパシフィック(シンガポール)`, ID: `ap-southeast-1`
    - 間違いやすいので注意

#### dynamoDB
- サービス -> dynamoDB -> テーブルの作成
    - テーブル名: `todo-table-faasXX-gui` (XX 部分は自分の番号を確認)
    - パーティションキー: `id`
    - 右下の`作成`をクリック

#### lambda
- サービス -> lambda -> 関数の作成
    - 一から作成
    - 関数名: `todo-function-faasXX-gui` (XX 部分は自分の番号を確認)
    - ランタイム: `python3.6`
    - アクセス権限
      - 実行ロール: `基本的なlambdaアクセス権限で新しいロールを作成`
    - 右下の`関数の作成`をクリック

- Designerの`todo-function-faasXX-gui`をクリック
    - 関数コード -> コードエントリータイプ: zipファイルをアップロード
        - zip ファイル: (本プロジェクトの `faas/application/backend` をzipして選択)
        - ランタイム: `python3.6`
        - ハンドラ: `lambda_handler.lambda_handler`
    - 環境変数
        - `REGION_NAME: ap-southeast-1`
        - `TABLE_NAME: todo-table-faasXX-gui`
    - 実行ロール
        - IAMコンソールで`todo-function-faasXX-gui-role-XXロールを表示`をクリック
            - permissions policies -> `ポリシーをアタッチします`をクリック
            - 検索窓で`dynamoDB`を検索し、 `dynamoDBFullAccess`をチェック、右下の`ポリシーのアタッチ`をクリック
    - 右上の`保存`をクリック

#### API Gateway
- サービス -> API Gateway
    - `+APIの作成`をクリック
        - Choose the protocol: `REST`
        - 新しいAPIの作成: `新しいAPI`
        - 名前と説明
            - API名: `todo-api-faasXX-gui` (XX 部分は自分の番号を確認)
            - 説明: `適当にどうぞ`
            - エンドポイントタイプ: `エッジ最適化`
        - 右下の`作成`をクリック
    - /を選択し、アクション -> リソースの作成
        - プロキシリソースとして設定: `チェックしない`
        - リソース名: `tasks`
        - リソースパス: `tasks`
        - API Gateway CORS を有効にする: `チェックしない`
        - `リソースの作成`をクリック
    - /tasksを選択し、アクション -> メソッドの追加
        - 以下を作成
           - GET
               - 統合タイプ: `lambda関数`
               - lambdaプロキシ統合の使用: `チェックする`
               - lambdaリージョン: `ap-southeast-1`
               - lambda関数: `todo-function-faasXX-gui`
               - デフォルトタイムアウトの使用: `チェックする`
           - POST
               - 統合タイプ: `lambda関数`
               - lambdaプロキシ統合の使用: `チェックする`
               - lambdaリージョン: `ap-southeast-1`
               - lambda関数: `todo-function-faasXX-gui`
               - デフォルトタイムアウトの使用: `チェックする`
   - /tasksを選択し、アクション -> リソースの作成
        - プロキシリソースとして設定: `チェックしない`
        - リソース名: `{id}`
        - リソースパス: `{id}`
        - API Gateway CORS を有効にする: `チェックしない`
        - `リソースの作成`をクリック
    - /{id}を選択し、アクション -> メソッドの追加
        - 以下を作成
           - GET
               - 統合タイプ: `lambda関数`
               - lambdaプロキシ統合の使用: `チェックする`
               - lambdaリージョン: `ap-southeast-1`
               - lambda関数: `todo-function-faasXX-gui`
               - デフォルトタイムアウトの使用: `チェックする`
           - PUT
               - 統合タイプ: `lambda関数`
               - lambdaプロキシ統合の使用: `チェックする`
               - lambdaリージョン: `ap-southeast-1`
               - lambda関数: `todo-function-faasXX-gui`
               - デフォルトタイムアウトの使用: `チェックする`
           - DELETE
               - 統合タイプ: `lambda関数`
               - lambdaプロキシ統合の使用: `チェックする`
               - lambdaリージョン: `ap-southeast-1`
               - lambda関数: `todo-function-faasXX-gui`
               - デフォルトタイムアウトの使用: `チェックする`

-  アクション -> APIのデプロイ
    - デプロイされるステージ: `新しいステージ`
    - ステージ名: faasXX-gui
    - ステージの説明: `適当`
    - デプロイメントの説明: `適当`
    - `デプロイ`をクリック
    - `todo-api-faasXX-gui` -> ステージ -> `faasXX-gui`をクリックし、`ログ/トレース`を選択
      - `CloudWatch ログを有効化`にチェック
      - ``変更を保存``をクリック
    - ステージをクリックし、表示されるURLがエンドポイント

- 動作確認の方法
    - postman/curl など API 自身を叩く
    - ~~frontend アプリも動きます。~~ frontend を使うには APIGW で CORS の設定が必要です。自力でお願いします。（Part.2 では対応しています）

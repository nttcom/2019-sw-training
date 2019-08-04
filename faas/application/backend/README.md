
# APP 紹介
シンプルなTodo APPであり、バックエンドのみである。（フロントエンドはIaaS, CaaS, FaaS共通のものを利用）
下記のAPI仕様書を読み、Backendコードを完成してほしい
言語はPython、FlameworkはFlaskとする

## API Interfaces ##
- `1. GET /tasks`
- `2. POST /tasks`
- `3. GET /tasks/{id}`
- `4. DELETE /tasks/{id}`
- `5. PUT /tasks/{id}`


### 1. List all Todo Items ###

**Definition**

`GET /tasks`

**Response**

- `200 OK` when success

```json
[
	{
        "id": "1",
        "item": "Training Preps #1",
        "is_done": false
	},
	{
	    "id": "2",
	    "item": "Training Preps #2",
        "is_done": true
    }
]
```


### 2. Insert a Todo Item ###

**Definition**

`POST /tasks`

**Arguments**

- `"item":string` context of todo item
- `"is_done":boolean` flag to specify if todo is done. default value is False

**Response**

- `201 Created` when success

```json
{
    "id": "1",
    "item": "Training Preps #1",
    "is_done": false
}
```

### 3. Get a Todo Item ###

**Definition**

`GET /tasks/<id>`

**Arguments**

- `"id":integer` identifier of todo item

**Response**

- `200 OK` when success
- `404 Not Found` if id does not exist

```json
{
    "id": "1",
    "item": "Training Preps #1",
    "is_done": false
}
```


### 4. Delete a Todo Item ###

**Definition**

`DELETE /tasks/<id>`

**Arguments**

- `"id":integer` identifier of todo item

**Response**

- `204 No Content` when success
- `404 Not Found` if id does not exist

### 5. Update a Todo Item ###

**Definition**

`PUT /tasks/<id>`

**Arguments**

- `"id":integer` identifier of todo item
- `"item":string` context of todo item
- `"is_done":boolean` flag to specify if todo is done. default value is False

**Response**

- `200 OK` when success
- `404 Not Found` if id does not exist

```json
{
    "id": "1",
    "item": "Training Preps #1",
    "is_done": false
}
```


# Usage
## 重要なパラメーター
- our_regionname: ap-southeast-1 (東京じゃなくてシンガポール)
- your_profile_name: faas01 -- faas40 (自分の番号で！間違うと楽しいです)

## recommended environment
- mac or linux (2019年ハンズオンでは 1人1台 EC2 インスタンスを提供します)
- python version: `3.6.x`
    - Lambda の runtime を python 3.6 としている
    - `2` はムリです、 `3.7` は動くかも、コードに手を加える必要があるので要相談
- Node.js version: `v8.10.0`
    - serverless framework で offline test, deploy するのに必要
    - それより新しくても動くかも


## Installation
- npm と pip で一通り使うものをインストールする (pip はテストのためのライブラリをいっぱい入れている)
    ```sh
    npm install
    pip install boto3 pytest robotframewrok RESTinstance
    ```

## test
ユニットテスト、ローカルに AWS を再現することでテスト、更に robot framework を組み合わせて自動テスト、などのバリエーションを紹介する。

### Serverless Offline
ローカルに apigw, lambda, dynamodb をエミュレートして TDD できるお（完全おまけコンテンツ）

- java 1.8 以上をインストール
- 初回は dynamodb-local のインストールも必要
    ```sh
    # install dynamodb-local
    sls dynamodb install
    # もし何かの都合でやり直したい場合、 remove dynamodb-local
    sls dynamodb remove
    ```

- execute sls offline
    ```sh
    $ sls offline start --profile <your_profile_name> --stage <your_profile_name> --region <our_region_name>
    ```

- これで、 http://127.0.0.1:3000 の配下に API のエンドポイントが生成され、裏ではlambda, dynamodb もエミュレートされる。 curl などで楽しんでください。

### Robot Framework でのテスト
rotob framework とその REST API 用の拡張である RESTinstance を用いれば、ローカルの API エンドポイントに対して受入試験のように動作確認が行える。
- ローカルでのテストのサンプルは以下:
    ```sh
    cd /path/to/backend/rf/1_sls_local/
    robot main.robot
    ```

### pytest によるユニットテスト
今回は lambda handler にパラメータを送り込んでテストを行う。

- serverlss offline が起動していること

- 環境変数を設定
    ```sh
    export REGION_NAME=<our_region_name>; export TABLE_NAME=todo-table-<your_profile_name>-sls
    ```

- テスト実行！
    ```sh
    pytest
    ```

- 出力 (成功の場合):
    ```sh
    ============================= test session starts ==============================
    platform darwin -- Python 3.6.5, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
    rootdir: /Users/george/shugyo/2019-sw-training/faas/application/backend
    collected 7 items

    tests/test_sls_offline.py .......                                        [100%]

    =========================== 7 passed in 3.60 seconds ===========================
    ```

- note:
  event オブジェクト, 環境変数の設定 あたりが癖がある感じ。
  コード規模が大きくないので、 unit test が必ずしも必要とは限らない。また、 unit といいながら DynamoDB Local が必須だし、ちょっとハードル高めでは有る。
  本気で開発するときは pytest-watch を仕掛けて、 ファイル更新のたびに unit test が回るようにしておくとだいぶ素早く開発が進む。

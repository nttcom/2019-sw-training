
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

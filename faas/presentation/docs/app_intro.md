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

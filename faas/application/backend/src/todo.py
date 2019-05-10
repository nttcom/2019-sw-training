import boto3
import os
import json
import jsonschema


class Todo:
    """
    Todo tasks class
    """

    def __init__(self, is_offline):
        # region and table name from Lambda environment variables,
        # which derives from serverelss.yml!
        region_name = os.getenv('REGION_NAME')
        table_name = os.getenv('TABLE_NAME')

        if is_offline:
            dynamodb = boto3.resource(
                'dynamodb',
                region_name='localhost',
                endpoint_url='http://localhost:8000'
            )
        else:
            dynamodb = boto3.resource(
                'dynamodb',
                region_name=region_name
            )

        self.table = dynamodb.Table(table_name)

        # validation schema
        self.request_schema = {
            "type": "object",
            "required": [
                "id",
                "item",
                "is_done"
            ],
            "properties": {
                "id": {
                    "type": "string",
                    "pattern": "^[0-9]+$"
                },
                "item": {
                    "type": "string"
                },
                "is_done": {
                    "type": "boolean",
                    "default": False
                }
            },
            "additionalProperties": False
        }

    # list tasks
    def list(self):
        # read from DynamoDB
        result = self.table.scan()
        tasks = result['Items']
        return tasks

    # get task
    def get(self, id):
        # read from DynamoDB
        result = self.table.get_item(Key={'id': id})

        if 'Item' in result.keys():
            task = result['Item']
            return task
        else:
            return None

    # create tasks
    def create(self, body):
        next_id = self.update_counter()
        task = body
        task['id'] = next_id
        task['is_done'] = False

        try:
            jsonschema.validate(instance=task, schema=self.request_schema)
        except jsonschema.ValidationError as e:
            error = {'error': e.message}
            return False, error

        # write to DynamoDB
        res = self.table.put_item(
            Item=task,
            ConditionExpression='attribute_not_exists(id)'
        )
        print(res)

        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True, task
        else:
            error = {'error': 'creation failed'}
            return False, error

    # edit tasks
    def edit(self, id, body):
        # To allow client to send only keys to update,
        # you first need to get existing record.
        task = self.get(id)
        for k, v in body.items():
            task[k] = v

        try:
            jsonschema.validate(instance=task, schema=self.request_schema)
        except jsonschema.ValidationError as e:
            error = {'error': e.message}
            return False, error

        # write to DynamoDB
        res = self.table.put_item(
            Item=task
        )
        print(res)

        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True, task
        else:
            error = {'error': 'creation failed'}
            return False, error

    # delete tasks
    def delete(self, id):
        # write to DynamoDB
        is_ok = self.table.delete_item(Key={'id': id})
        return is_ok

    # update counter in order not to re-use past numbers
    def update_counter(self):
        tasks = self.list()

        if len(tasks) > 0:
            tasks.sort(key=lambda x: int(x['id']))
            max_id = tasks[-1]['id']
        else:
            max_id = '-1'

        if os.getenv('LASTID') is None:
            next_id = str(int(max_id) + 1)
        elif int(os.getenv('LASTID')) > int(max_id):
            next_id = str(int(os.getenv('LASTID')) + 1)
        else:
            next_id = str(int(max_id) + 1)

        os.environ['LASTID'] = next_id
        return next_id

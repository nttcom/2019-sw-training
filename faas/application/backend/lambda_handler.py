import json
from src.todo import Todo


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event : dict
        event object from trigger (apigw in this project)
        for sample, see test file.
    context : dict
        Lambda runtime information.
        for details, see https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-programming-model.html

    Returns
    -------
    statusCode : int
    body : jsonstr

    {
        'statusCode': 200,
        'headers': {'aaa': 'AAA', 'bbb': 'BBB', ...}
        'body': json.dumps(task)
    }
    """

    # to judge if the environment is real AWS or sls offline
    is_offline = True if ('isOffline', True) in event.items() else False
    todo = Todo(is_offline)

    # logging anyway
    print('--event object: ')
    if is_offline is False:
        print(json.dumps(event))
    else:
        import pprint
        pprint.pprint(event)

    # for CORS
    response_headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # list tasks
    if event['httpMethod'] == 'GET' and event['resource'] == '/tasks':
        tasks = todo.list()
        return {
            'statusCode': 200,
            'headers': response_headers,
            'body': json.dumps(tasks)
        }

    # get a task
    if event['httpMethod'] == 'GET' and event['resource'] == '/tasks/{id}':
        id = event['pathParameters']['id']
        task = todo.get(id)

        if task is None:
            return {
                'statusCode': 404,
                'headers': response_headers,
                'body': json.dumps({'error': 'not found.'})
            }
        else:
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(task)
            }

    # create a task
    if event['httpMethod'] == 'POST' and event['resource'] == '/tasks':
        body = json.loads(event['body'])
        is_ok, task = todo.create(body)

        if is_ok:
            return {
                'statusCode': 201,
                'headers': response_headers,
                'body': json.dumps(task)
            }
        else:
            return {
                'statusCode': 400,
                'headers': response_headers,
                'body': json.dumps(task)
            }

    # edit a task
    if event['httpMethod'] == 'PUT' and event['resource'] == '/tasks/{id}':
        id = event['pathParameters']['id']
        body = json.loads(event['body'])
        is_ok, task = todo.edit(id, body)

        if is_ok:
            return {
                'statusCode': 200,
                'headers': response_headers,
                'body': json.dumps(task)
            }
        else:
            return {
                'statusCode': 400,
                'headers': response_headers,
                'body': json.dumps(task)
            }

    # delete a task
    if event['httpMethod'] == 'DELETE' and event['resource'] == '/tasks/{id}':
        id = event['pathParameters']['id']
        is_ok = todo.delete(id)

        if is_ok:
            return {
                'statusCode': 204,
                'headers': response_headers
            }
        else:
            return {
                'statusCode': 500,
                'headers': response_headers,
                'error': 'deletion was not OK: {}'.format(is_ok)
            }

    # exception: no definition matches
    return {
        'statusCode': 400,
        'headers': response_headers,
        'body': '{"error": "request method x endpoint does not exist."}'
    }

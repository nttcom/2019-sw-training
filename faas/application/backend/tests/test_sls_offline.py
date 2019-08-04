import pytest
import json
from lambda_handler import lambda_handler

############################################################
############################################################
# This test won't work for thie project as it is difficult
# to reproduce the 'context' object...
# So ddb table name cannot be passed from serverless.yml
# to these tests.
############################################################
############################################################
############################################################

# common constant objects
context = {}
task = {
    'id': '0',
    'item': 'do a job',
    'is_done': False
}
task_done = {
    'id': '0',
    'item': 'do a job',
    'is_done': True
}

# object 'event' is also common obj, but needs to be initialized each time
@pytest.fixture(scope='function', autouse=True)
def event_init():
    event = {
        'headers': {
            'Host': 'localhost:3000',
            'User-Agent': 'curl/7.54.0',
            'Accept': '*/*'
        },
        'path': '/tasks/0',
        'pathParameters': {
            'id': '0'
        },
        'requestContext': {
            'accountId': 'offlineContext_accountId',
            'resourceId': 'offlineContext_resourceId',
            'apiId': 'offlineContext_apiId',
            'stage': 'hogehoge',
            'requestId': 'offlineContext_requestId_',
            'identity': {
                'cognitoIdentityPoolId': 'offlineContext_cognitoIdentityPoolId',
                'accountId': 'offlineContext_accountId',
                'cognitoIdentityId': 'offlineContext_cognitoIdentityId',
                'caller': 'offlineContext_caller',
                'apiKey': 'offlineContext_apiKey',
                'sourceIp': '127.0.0.1',
                'cognitoAuthenticationType': 'offlineContext_cognitoAuthenticationType',
                'cognitoAuthenticationProvider': 'offlineContext_cognitoAuthenticationProvider',
                'userArn': 'offlineContext_userArn',
                'userAgent': 'curl/7.54.0',
                'user': 'offlineContext_user'
            },
            'authorizer': {
                'principalId': 'offlineContext_authorizer_principalId'
            },
            'resourcePath': '/tasks/{id}',
            'httpMethod': 'GET'
        },
        'resource': '/tasks/{id}',
        'httpMethod': 'GET',
        'queryStringParameters': None,
        'stageVariables': None,
        'body': None,
        'isOffline': True
    }
    yield event


def test_POST(event_init):
    event_init['httpMethod'] = 'POST'
    event_init['path'] = '/tasks'
    event_init['resource'] = '/tasks'
    event_init['pathParameters'] = None
    event_init['body'] = '{"item": "do a job"}'

    _r = lambda_handler(event_init, context)

    assert _r['statusCode'] == 201
    assert json.loads(_r['body']) == task


def test_GET_0(event_init):
    event_init['httpMethod'] = 'GET'
    event_init['path'] = '/tasks/0'
    event_init['resource'] = '/tasks/{id}'
    event_init['pathParameters'] = {'id': '0'}
    event_init['body'] = None

    _r = lambda_handler(event_init, context)

    assert _r['statusCode'] == 200
    assert json.loads(_r['body']) == task


def test_PUT(event_init):
    event_init['httpMethod'] = 'PUT'
    event_init['path'] = '/tasks/0'
    event_init['resource'] = '/tasks/{id}'
    event_init['pathParameters'] = {'id': '0'}
    event_init['body'] = '{"is_done": true}'

    _r = lambda_handler(event_init, context)

    assert _r['statusCode'] == 200
    assert json.loads(_r['body']) == task_done


def test_GET_1(event_init):
    event_init['httpMethod'] = 'GET'
    event_init['path'] = '/tasks/0'
    event_init['resource'] = '/tasks/{id}'
    event_init['pathParameters'] = {'id': '0'}
    event_init['body'] = None

    _r = lambda_handler(event_init, context)

    assert _r['statusCode'] == 200
    assert json.loads(_r['body']) == task_done


def test_LIST(event_init):
    event_init['httpMethod'] = 'GET'
    event_init['path'] = '/tasks'
    event_init['resource'] = '/tasks'
    event_init['pathParameters'] = None
    event_init['body'] = None

    _r = lambda_handler(event_init, context)

    assert _r['statusCode'] == 200
    assert json.loads(_r['body']) == [task_done]


def test_DELETE_0(event_init):
    event_init['httpMethod'] = 'DELETE'
    event_init['path'] = '/tasks/0'
    event_init['resource'] = '/tasks/{id}'
    event_init['pathParameters'] = {'id': '0'}
    event_init['body'] = None

    _r = lambda_handler(event_init, context)

    assert _r['statusCode'] == 204


def test_GET_404(event_init):
    event_init['httpMethod'] = 'GET'
    event_init['path'] = '/tasks/0'
    event_init['resource'] = '/tasks/{id}'
    event_init['pathParameters'] = {'id': '0'}
    event_init['body'] = None

    _r = lambda_handler(event_init, context)

    assert _r['statusCode'] == 404

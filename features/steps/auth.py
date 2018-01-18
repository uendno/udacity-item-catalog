from behave import *
import jwt
from app import config


@given('no access token provided')
def step_impl(context):
    pass


@when('sending a DELETE request to /items/1')
def step_impl(context):
    headers = {}

    if hasattr(context, 'access_token'):
        headers['Authorization'] = context.access_token

    context.response = context.client.delete('/items/1', headers=headers)


@then('receive 401 error code')
def step_impl(context):
    assert context.response.status_code == 401


@when('sending a GET request to /items?mode=latest')
def step_impl(context):
    context.response = context.client.get('/items?mode=latest')


@then('receive 200 code')
def step_impl(context):
    assert context.response.status_code == 200


@given('a valid access token')
def step_impl(context):
    context.access_token = jwt.encode({'id': 1}, config.JWT_SECRET_KEY, algorithm='HS256')


@then('response status code is not 401')
def step_impl(context):
    assert context.response.status_code != 401

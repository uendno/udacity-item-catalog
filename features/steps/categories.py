from behave import *

from features.steps.utils import get_json


@when('sending GET request to /categories')
def step_impl(context):
    context.response = context.client.get('/categories')


@then('receive a list of 9 available categories')
def step_impl(context):
    response = context.response
    json = get_json(response)

    assert json['success'] is True
    assert len(json['data']) == 9


@when('sending a GET request to /categories/soccer')
def step_impl(context):
    context.response = context.client.get('/categories/soccer')


@then('receive details for Soccer category')
def step_impl(context):
    response = context.response
    json = get_json(response)

    assert response.status_code == 200
    assert json['success'] is True
    assert json['data']['name'] == 'Soccer'


@when('sending GET request to /categories/unknown')
def step_impl(context):
    context.response = context.client.get('/categories/unknown')


@then('receive 400 error code for unknown category')
def step_impl(context):
    response = context.response

    assert response.status_code == 400

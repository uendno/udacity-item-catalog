from behave import *

from features.steps.utils import get_json, add_items, remove_items


@given('DB has 3 items')
def step_impl(context):
    responses = add_items([
        {
            'name': 'Item 1',
            'category_id': 1
        },
        {
            'name': 'Item 2',
            'category_id': 2
        },
        {
            'name': 'Item 3',
            'category_id': 3
        }
    ], client=context.client)

    for response in responses:
        assert response.status_code == 200


@when('sending GET request to /items')
def step_impl(context):
    context.response = context.client.get('/items')


@then('receive a list of 3 available items')
def step_impl(context):
    response = context.response
    json = get_json(response)

    assert len(json['data']) == 3
    assert json['data'][0]['slug'] == 'item-1'
    assert json['data'][1]['slug'] == 'item-2'
    assert json['data'][2]['slug'] == 'item-3'

    responses = remove_items([1, 2, 3], client=context.client)

    for response in responses:
        assert response.status_code == 200


@when('sending a GET request to /items?mode=latest&limit=2')
def step_impl(context):
    context.response = context.client.get('/items?mode=latest&limit=2')


@then('receive a list of 2 most recent items')
def step_impl(context):
    response = context.response
    json = get_json(response)

    assert len(json['data']) == 2
    assert json['data'][0]['slug'] == 'item-3'
    assert json['data'][1]['slug'] == 'item-2'

    responses = remove_items([1, 2, 3], client=context.client)

    for response in responses:
        assert response.status_code == 200


@given('DB has 1 item which has id = 1')
def step_impl(context):
    responses = add_items([
        {
            'name': 'Item 1',
            'category_id': 1
        },
    ], client=context.client)

    for response in responses:
        assert response.status_code == 200


@when('sending a GET request to /items/1')
def step_impl(context):
    context.response = context.client.get('/items/1')


@then('receive details for the right item')
def step_impl(context):
    response = context.response
    json = get_json(response)

    assert json['data']['slug'] == 'item-1'
    assert json['data']['category']['id'] == 1

    responses = remove_items([1], client=context.client)

    for response in responses:
        assert response.status_code == 200


@given('DB does not have any item which has id = 123')
def step_impl(context):
    pass


@when('sending GET request to /items/123')
def step_impl(context):
    context.response = context.client.get('/items/123')


@then('receive 400 error code for unknown item')
def step_impl(context):
    response = context.response

    assert response.status_code == 400


@given('DB does not have any item which has the name Item 1')
def step_impl(context):
    pass


@when('sending a POST request to /items to add an item with the name Item 1')
def step_impl(context):
    responses = add_items([{
        'name': 'Item 1',
        'category_id': '1'
    }], client=context.client)

    context.response = responses[0]


@then('receive 200 status code and item details')
def step_impl(context):
    response = context.response
    assert response.status_code == 200

    responses = remove_items([1], client=context.client)
    assert responses[0].status_code == 200


@given('DB has an item which has the name Item 1')
def step_impl(context):
    responses = add_items([{
        'name': 'Item 1',
        'category_id': '1'
    }], client=context.client)

    for response in responses:
        assert response.status_code == 200


@then('receive 400 status code because of the invalid name')
def step_impl(context):
    response = context.response
    assert response.status_code == 400

    responses = remove_items([1], client=context.client)
    assert responses[0].status_code == 200

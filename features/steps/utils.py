import json

import jwt

from app import config

access_token = jwt.encode({'id': 1}, config.JWT_SECRET_KEY, algorithm='HS256')


def get_json(response):
    return json.loads(response.get_data(as_text=True))


def add_items(items, client):
    responses = []

    for item in items:
        response = client.post('/items', headers={
            'Authorization': access_token,
        }, data=json.dumps({
            'name': item['name'],
            'description': '%s description' % item['name'],
            'category_id': item['category_id']
        }), content_type='application/json')

        responses.append(response)

    return responses


def remove_items(item_ids, client):
    responses = []

    for item_id in item_ids:
        response = client.delete('/items/%d' % item_id, headers={
            'Authorization': access_token,
        })

        responses.append(response)

    return responses


def update_item(item_id, data, client):
    return client.put('/items/%d' % item_id, headers={
        'Authorization': access_token,
    }, data=json.dumps(data), content_type='application/json')

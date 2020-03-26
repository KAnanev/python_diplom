import requests
import time
import json

API_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
GET_URL = 'https://api.vk.com/method/'
user_id = '171691064'

if isinstance(user_id, str):
    response = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': API_TOKEN,
            'user_ids': user_id,
            'v': '5.103'
        })
    user_id = response.json()['response'][0]['id']
else:
    user_id = user_id


def get_req(execute, user):
    res = requests.post(f'{GET_URL}/execute',
                        params={
                                'code': 'return ' + execute + '({"user_id": "' + str(user) + '"}).items;',
                                'access_token': API_TOKEN,
                                'v': '5.103'
                            })
    print('|', end='')
    return res


list_friends = get_req('API.friends.get', user_id).json()['response']
list_groups_user = get_req('API.groups.get', user_id).json()['response']

list_groups_friends = []

for i in list_friends:
    try:
        response = get_req('API.groups.get', str(i)).json()['response']
        if isinstance(response, list):
            list_groups_friends.extend(response)
    except KeyError:
        pass
user_groups = set(list_groups_user)
friends_groups = set(list_groups_friends)
groups = ', '.join(str(i) for i in list(user_groups.difference(friends_groups)))


def get_gr(execute, list_groups):
    time.sleep(3)
    res = requests.post(f'{GET_URL}/execute',
                        params={
                                'code': 'return ' + execute +
                                        '({"group_ids": "' + list_groups + '", "fields": "members_count"});',
                                'access_token': API_TOKEN,
                                'v': '5.103'
                            })
    print('|', end='')
    list_end_groups = []
    for item in res.json()['response']:
        list_end_groups.append({'name': item['name'], 'gid': item['id'], 'members_count': item['members_count']})
    with open('groups.json', 'w') as f:
        f.write(json.dumps(list_end_groups, ensure_ascii=False))


get_gr('API.groups.getById', groups)

print('\n Процесс завершён')



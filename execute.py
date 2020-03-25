import requests
import time
from pprint import pprint
API_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
GET_URL = 'https://api.vk.com/method/'
USER_ID = '171691064'


def get_req(execute, user_id):
    res = requests.post(f'{GET_URL}/execute',
                        params={
                                'code': 'return ' + execute + '({"user_id": "' + user_id + '"}).items;',
                                'access_token': API_TOKEN,
                                'v': '5.103'
                            })
    print('|', end='.'),
    return res


list_friends = get_req('API.friends.get', USER_ID).json()['response']
list_groups_user = get_req('API.groups.get', USER_ID).json()['response']

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
                                'code': 'return ' + execute + '({"group_ids": "' + list_groups + '", "fields": "members_count"});',
                                'access_token': API_TOKEN,
                                'v': '5.103'
                            })
    print('|', end='.'),
    pprint(res.json())


get_gr('API.groups.getById', groups)



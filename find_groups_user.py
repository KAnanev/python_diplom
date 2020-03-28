# -*- coding: utf8 -*-
import requests
import json
import time

API_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
GET_URL = 'https://api.vk.com/method/'


class User:

    def __init__(self, user_id):
        if isinstance(user_id, str):
            response = requests.get(
                'https://api.vk.com/method/users.get',
                params={
                    'access_token': API_TOKEN,
                    'user_ids': user_id,
                    'v': '5.103'
                })
            self.user_id = str(response.json()['response'][0]['id'])
        else:
            self.user_id = user_id

    def print_slash(self):
        print('|', end='')

    def get_user_data(self, value):
        response = requests.post(f'{GET_URL}/execute',
                                 params={
                                     'code': 'return API.' + value + '.get({"user_id": "' + obj_user.user_id + '"}).items;',
                                     'access_token': API_TOKEN,
                                     'v': '5.103'
                                 })
        obj_user.print_slash()
        return response.json()['response']

    def get_friends_group(self, list_friends):
        list_groups_friends = []
        count = 0
        for i in range(0, len(list_friends), 25):
            response = requests.post(f'{GET_URL}/execute',
                                     params={
                                         'code': 'return [' + ', '.join(
                                             ['API.groups.get({"user_id": "' + str(i) + '"}).items' for i in
                                              list_friends[i: i + 25]]) + '];',
                                         'access_token': API_TOKEN,
                                         'v': '5.103'
                                     })
            obj_user.print_slash()
            count += 1
            if count == 3:
                time.sleep(1)
                count == 0
            for item in response.json()['response']:
                if isinstance(item, list):
                    list_groups_friends.extend(item)

        return list_groups_friends

    def get_unique_groups(self, user_groups, friends_groups):
        user_groups = set(user_groups)
        friends_groups = set(friends_groups)
        unique_groups = ', '.join(str(i) for i in list(user_groups.difference(friends_groups)))
        res = requests.post(f'{GET_URL}/execute',
                            params={
                                'code': 'return API.groups.getById'
                                        '({"group_ids": "' + unique_groups + '", "fields": "members_count"});',
                                'access_token': API_TOKEN,
                                'v': '5.103'
                            })
        obj_user.print_slash()
        list_end_groups = []
        for item in res.json()['response']:
            list_end_groups.append({'name': item['name'], 'gid': item['id'], 'members_count': item['members_count']})
        with open('groups.json', 'w') as f:
            f.write(json.dumps(list_end_groups, ensure_ascii=False))


obj_user = User(input("Введите id пользователя: "))
friends = obj_user.get_user_data('friends')
groups = obj_user.get_user_data('groups')
friends_groups = obj_user.get_friends_group(friends)
obj_user.get_unique_groups(groups, friends_groups)

# -*- coding: utf8 -*-
import requests
import json
import time

API_TOKEN = 'token'
GET_URL = 'https://api.vk.com/method/'


def print_slash():
    print('|', end='')


class User:

    def __init__(self, user_id, api_token):
        """Инициализирует атрибут user_id и токен vk"""
        if isinstance(user_id, str):
            response = requests.get(
                'https://api.vk.com/method/users.get',
                params={
                    'access_token': API_TOKEN,
                    'user_ids': user_id,
                    'v': '5.103'
                })
            print_slash()
            self.user_id = str(response.json()['response'][0]['id'])
        else:
            self.user_id = user_id

    def get_user_data(self, value):
        """Функция запроса получения данных пользователя"""
        response = requests.post(f'{GET_URL}/execute',
                                 params={
                                     'code': 'return API.' + value + '.get({"user_id": "' + obj_user.user_id + '"}).items;',
                                     'access_token': API_TOKEN,
                                     'v': '5.103'
                                 })
        print_slash()
        return response.json()['response']

    def get_friends_group(self, list_friends):
        """Функция получает список друзуй, формирует запрос, возвращает список групп друзей"""
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
            print_slash()
            count += 1
            if count == 3:
                time.sleep(1)
                count == 0
            for item in response.json()['response']:
                if isinstance(item, list):
                    list_groups_friends.extend(item)

        return list_groups_friends

    def get_unique_groups(self, user_groups, friends_groups):
        """Функция получает список групп пользователя и список групп друзей, выводит уникальные группы"""
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
        print_slash()
        list_end_groups = []
        for item in res.json()['response']:
            list_end_groups.append({'name': item['name'], 'gid': item['id'], 'members_count': item['members_count']})
        with open('groups.json', 'w') as f:
            f.write(json.dumps(list_end_groups, ensure_ascii=False))


if __name__ == '__main__':
    obj_user = User(input("Введите id пользователя: "))
    friends = obj_user.get_user_data('friends')
    groups = obj_user.get_user_data('groups')
    friends_groups = obj_user.get_friends_group(friends)
    obj_user.get_unique_groups(groups, friends_groups)


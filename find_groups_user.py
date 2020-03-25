import requests

API_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
GET_URL = 'https://api.vk.com/method/'

user = 'eshmargunov'
list_users = []


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
            self.user_id = response.json()['response'][0]['id']
        else:
            self.user_id = user_id

    def __str__(self):
        return str(self.user_id)

    def get_only_my_groups(self):
        response = requests.post(f'{GET_URL}/execute',
                                 params={
                                     'code': 'return [API.groups.get({"user_id": "' + str(self.user_id) + '"}).items, '
                                                                                                          'API.groups.get({"user_id": API.friends.get'
                                                                                                          '({"user_id": "' + str(
                                         self.user_id) + '"})@.items}).items];',
                                     'access_token': API_TOKEN,
                                     'v': '5.103'
                                 })
        user_groups = set(response.json()['response'][0])
        friends_groups = set(response.json()['response'][1])
        return user_groups.difference(friends_groups)

    def get_group_info(self, id_group):
        if not isinstance(id_group, list):
            id_group = ', '.join(str(i) for i in list(id_group))
            print(id_group)
        # for i in id_group:
        #     response = requests.post(f'{GET_URL}/execute',
        #                              params={
        #                                  'code': 'return [API.groups.get().items;',
        #                                  'access_token': API_TOKEN,
        #                                  'v': '5.103'
        #                              })


obj_user = User(user)
obj_user.get_group_info(obj_user.get_only_my_groups())

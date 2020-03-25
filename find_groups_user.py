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

    def get_user_groups(self):
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params={
                'access_token': API_TOKEN,
                'user_id': self.user_id,
                'v': '5.103'
            })
        return response.json()

    def get_user_friends(self):
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params={
                'access_token': API_TOKEN,
                'user_id': self.user_id,
                'v': '5.103'
            })
        for i in response.json()['response']['items']:
            user = User(i)
            list_users.append(user)


obj_user = User(user)
obj_user.get_user_friends()

for i in list_users:
    print(i.get_user_groups())

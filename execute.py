import requests

API_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
GET_URL = 'https://api.vk.com/method/'

# response_friends = requests.post(f'{GET_URL}/execute',
#                          params={
#                              'code': 'var b = API.friends.get({"user_id": "577250478"}); return b.items;',
#                              'access_token': API_TOKEN,
#                              'v': '5.103'
#                          })
# print(response_friends.json())


response = requests.post(f'{GET_URL}/execute',
                         params={
                             'code': 'return [API.groups.get({"user_id": "171691064"}).items, API.groups.get({"user_id": API.friends.get({"user_id": "171691064"})@.items}).items];',
                             'access_token': API_TOKEN,
                             'v': '5.103'
                         })
user_groups = set(response.json()['response'][0])
friends_groups = set(response.json()['response'][1])
print(user_groups.difference(friends_groups))

# response_group = requests.post(f'{GET_URL}/execute',
#                                params={
#                                    'code': 'return API.friends.get({"user_id": "577250478"}).items;',
#                                    'access_token': API_TOKEN,
#                                    'v': '5.103'
#                                })
# list_friend = response_group.json()['response']
# print(list_friend)
#
# response_group = requests.post(f'{GET_URL}/execute',
#                                params={
#                                    'code': 'return API.groups.get({"user_id": "2178068"}).items;',
#                                    'access_token': API_TOKEN,
#                                    'v': '5.103'
#                                })
# print(response_group.json())



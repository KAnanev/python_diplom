from urllib.parse import urlencode
APP_ID = 7350471
OAUTH_URL = 'https://oauth.vk.com/authorize'
OAUTH_PARAMS = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'friends',
    'response_type': 'token',
    'v': '5.103'
}

print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))
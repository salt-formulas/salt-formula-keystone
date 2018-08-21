from keystonev3.common import send
from keystonev3.arg_converter import get_by_name_or_uuid_multiple
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@get_by_name_or_uuid_multiple([('user', 'user_id')])
@send('get')
def user_get_details(user_id, **kwargs):
    url = '/users/{}?{}'.format(user_id, urlencode(kwargs))
    return url, None


@get_by_name_or_uuid_multiple([('user', 'user_id')])
@send('patch')
def user_update(user_id, **kwargs):
    url = '/users/{}'.format(user_id)
    json = {
        'user': kwargs,
    }
    return url, json


@get_by_name_or_uuid_multiple([('user', 'user_id')])
@send('delete')
def user_delete(user_id, **kwargs):
    url = '/users/{}'.format(user_id)
    return url, None


@send('post')
def user_create(**kwargs):
    url = '/users'
    json = {
        'user': kwargs,
    }
    return url, json

from keystonev3.common import send
from keystonev3.arg_converter import get_by_name_or_uuid_multiple
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@get_by_name_or_uuid_multiple([('domain', 'domain_id')])
@send('post')
def group_create(domain_id, name, **kwargs):
    url = '/groups'
    json = {
        'group':{
            'name': name,
            'domain_id': domain_id,
        }
    }
    json['group'].update(kwargs)
    return url, json


@get_by_name_or_uuid_multiple([('group', 'group_id')])
@send('get')
def group_get_details(group_id, **kwargs):
    url = '/groups/{}'.format(group_id)
    return url, None


@get_by_name_or_uuid_multiple([('group', 'group_id')])
@send('patch')
def group_update(group_id, **kwargs):
    url = '/groups/{}'.format(group_id)
    json = {
        'group': kwargs,
    }
    return url, json


@get_by_name_or_uuid_multiple([('group', 'group_id')])
@send('delete')
def group_delete(group_id, **kwargs):
    url = '/groups/{}'.format(group_id)
    return url, None

@get_by_name_or_uuid_multiple([('group', 'group_id')])
@send('get')
def group_user_list(group_id, **kwargs):
    url = '/groups/{}?{}'.format(group_id, urlencode(kwargs))
    return url, None


@get_by_name_or_uuid_multiple([('group', 'group_id'), ('user', 'user_id')])
@send('put')
def group_user_add(group_id, user_id, **kwargs):
    url = '/groups/{}/users/{}'.format(group_id, user_id)
    return url, None


@get_by_name_or_uuid_multiple([('group', 'group_id'), ('user', 'user_id')])
@send('head')
def group_user_check(group_id, user_id, **kwargs):
    url = '/groups/{}/users/{}'.format(group_id, user_id)
    return url, None


@get_by_name_or_uuid_multiple([('group', 'group_id'), ('user', 'user_id')])
@send('delete')
def group_user_remove(group_id, user_id, **kwargs):
    url = '/groups/{}/users/{}'.format(group_id, user_id)
    return url, None

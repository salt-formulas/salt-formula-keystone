from keystonev3.common import send

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@send('get')
def endpoint_get_details(endpoint_id, **kwargs):
    url = '/endpoints/{}?{}'.format(endpoint_id, urlencode(kwargs))
    return url, None


@send('patch')
def endpoint_update(endpoint_id, **kwargs):
    url = '/endpoints/{}'.format(endpoint_id)
    json = {
        'endpoint': kwargs,
    }
    return url, json


@send('delete')
def endpoint_delete(endpoint_id, **kwargs):
    url = '/endpoints/{}'.format(endpoint_id)
    return url, None


@send('get')
def endpoint_list(**kwargs):
    url = '/endpoints?{}'.format(urlencode(kwargs))
    return url, None


@send('post')
def endpoint_create(**kwargs):
    url = '/endpoints'
    json = {
        'endpoint': kwargs,
    }
    return url, json

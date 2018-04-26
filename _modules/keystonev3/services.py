from keystonev3.common import get_by_name_or_uuid, send

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@send('get')
def service_list(**kwargs):
    url = '/services?{}'.format(urlencode(kwargs))
    return url, None


@get_by_name_or_uuid(service_list, 'services', 'service_id')
@send('get')
def service_get_details(service_id, **kwargs):
    url = '/services/{}?{}'.format(service_id, urlencode(kwargs))
    return url, None


@get_by_name_or_uuid(service_list, 'services', 'service_id')
@send('patch')
def service_update(service_id, **kwargs):
    url = '/services/{}'.format(service_id)
    json = {
        'service': kwargs,
    }
    return url, json


@get_by_name_or_uuid(service_list, 'services', 'service_id')
@send('delete')
def service_delete(service_id, **kwargs):
    url = '/services/{}'.format(service_id)
    return url, None


@send('post')
def service_create(**kwargs):
    url = '/services'
    json = {
        'service': kwargs,
    }
    return url, json

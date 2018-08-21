from keystonev3.common import send
from keystonev3.arg_converter import get_by_name_or_uuid_multiple
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


@get_by_name_or_uuid_multiple([('service', 'service_id')])
@send('post')
def endpoint_create(service_id, url, interface, **kwargs):
    api_url = '/endpoints'
    json = {
        'endpoint': {
            'service_id': service_id,
            'url': url,
            'interface': interface,
        }
    }
    json['endpoint'].update(kwargs)
    return api_url, json

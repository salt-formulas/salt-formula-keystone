from keystonev3.common import send
from keystonev3.arg_converter import get_by_name_or_uuid_multiple


@send('post')
def domain_create(name, **kwargs):
    url = '/domains'
    json = {
        'domain': kwargs,
    }
    json['domain']['name'] = name
    return url, json


@get_by_name_or_uuid_multiple([('domain', 'domain_id')])
@send('get')
def domain_get_details(domain_id, **kwargs):
    url = '/domains/{}'.format(domain_id)
    return url, None


@get_by_name_or_uuid_multiple([('domain', 'domain_id')])
@send('patch')
def domain_update(domain_id, **kwargs):
    url = '/domains/{}'.format(domain_id)
    json = {
        'domain': kwargs,
    }
    return url, json


@get_by_name_or_uuid_multiple([('domain', 'domain_id')])
@send('delete')
def domain_delete(domain_id, **kwargs):
    url = '/domains/{}'.format(domain_id)
    return url, None

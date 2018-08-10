from keystonev3.common import send
from keystonev3.arg_converter import get_by_name_or_uuid_multiple

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@get_by_name_or_uuid_multiple([('project', 'project_id')])
@send('get')
def project_get_details(project_id, **kwargs):
    url = '/projects/{}?{}'.format(project_id, urlencode(kwargs))
    return url, None


@get_by_name_or_uuid_multiple([('project', 'project_id')])
@send('patch')
def project_update(project_id, **kwargs):
    url = '/projects/{}'.format(project_id)
    json = {
        'project': kwargs,
    }
    return url, json


@get_by_name_or_uuid_multiple([('project', 'project_id')])
@send('delete')
def project_delete(project_id, **kwargs):
    url = '/projects/{}'.format(project_id)
    return url, None


@get_by_name_or_uuid_multiple([('domain', 'domain_id')])
@send('post')
def project_create(domain_id, name,**kwargs):
    url = '/projects'
    json = {
        'project': {
            'name': name,
            'domain_id': domain_id,
        }
    }
    json['project'].update(kwargs)
    return url, json

from keystonev3.common import get_by_name_or_uuid, send
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@send('get')
def project_list(**kwargs):
    url = '/projects?{}'.format(urlencode(kwargs))
    return url, None


@get_by_name_or_uuid(project_list, 'projects', 'project_id')
@send('get')
def project_get_details(project_id, **kwargs):
    url = '/projects/{}?{}'.format(project_id, urlencode(kwargs))
    return url, None


@get_by_name_or_uuid(project_list, 'projects', 'project_id')
@send('patch')
def project_update(project_id, **kwargs):
    url = '/projects/{}'.format(project_id)
    json = {
        'project': kwargs,
    }
    return url, json


@get_by_name_or_uuid(project_list, 'projects', 'project_id')
@send('delete')
def project_delete(project_id, **kwargs):
    url = '/projects/{}'.format(project_id)
    return url, None


@send('post')
def project_create(**kwargs):
    url = '/projects'
    json = {
        'project': kwargs,
    }
    return url, json

from keystonev3.common import get_by_name_or_uuid, send
from keystonev3.common import KeystoneException

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@send('get')
def role_list(**kwargs):
    url = '/roles?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def role_assignment_list(**kwargs):
    url = '/role_assignments?{}'.format(urlencode(kwargs))
    return url, None


@send('put')
def role_add(user_id, role_id, project_id=None, domain_id=None, **kwargs):
    if (project_id and domain_id) or (not project_id and not domain_id):
        raise KeystoneException('Role can be assigned either to project '
                                'or domain.')
    if project_id:
        url = '/projects/{}/users/{}/roles/{}'.format(project_id, user_id,
                                                      role_id)
    elif domain_id:
        url = '/domains/{}/users/{}/roles/{}'.format(domain_id, user_id,
                                                     role_id)
    return url, None


@send('delete')
def role_delete(user_id, role_id, project_id=None, domain_id=None, **kwargs):
    if (project_id and domain_id) or (not project_id and not domain_id):
        raise KeystoneException('Role can be unassigned either from project '
                                'or domain.')
    if project_id:
        url = '/projects/{}/users/{}/roles/{}'.format(project_id, user_id,
                                                      role_id)
    elif domain_id:
        url = '/domains/{}/users/{}/roles/{}'.format(domain_id, user_id,
                                                     role_id)
    return url, None


@send('head')
def role_assignment_check(user_id, role_id, project_id=None,
                          domain_id=None, **kwargs):
    if (project_id and domain_id) or (not project_id and not domain_id):
        raise KeystoneException('Role can be assigned either to project '
                                'or domain.')
    if project_id:
        url = '/projects/{}/users/{}/roles/{}'.format(project_id, user_id,
                                                      role_id)
    elif domain_id:
        url = '/domains/{}/users/{}/roles/{}'.format(domain_id, user_id,
                                                     role_id)
    return url, None


@get_by_name_or_uuid(role_list, 'roles', 'role_id')
@send('get')
def role_get_details(role_id, **kwargs):
    url = '/roles/{}?{}'.format(role_id, urlencode(kwargs))
    return url, None


@get_by_name_or_uuid(role_list, 'roles', 'role_id')
@send('patch')
def role_update(role_id, **kwargs):
    url = '/roles/{}'.format(role_id)
    json = {
        'role': kwargs,
    }
    return url, json


@get_by_name_or_uuid(role_list, 'roles', 'role_id')
@send('delete')
def role_remove(role_id, **kwargs):
    url = '/roles/{}'.format(role_id)
    return url, None


@send('post')
def role_create(**kwargs):
    url = '/roles'
    json = {
        'role': kwargs,
    }
    return url, json

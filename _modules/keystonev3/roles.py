from keystonev3.common import send
from keystonev3.arg_converter import get_by_name_or_uuid_multiple


try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@get_by_name_or_uuid_multiple([('project', 'project_id'), ('user', 'user_id'),
                               ('role', 'role_id')])
@send('put')
def role_assign_for_user_on_project(project_id, user_id, role_id, **kwargs):
    url = '/projects/{}/users/{}/roles/{}'.format(project_id, user_id, role_id)
    return url, None


@get_by_name_or_uuid_multiple([('domain', 'domain_id'), ('user', 'user_id'),
                               ('role', 'role_id')])
@send('put')
def role_assign_for_user_on_domain(domain_id, user_id, role_id, **kwargs):
    url = '/domains/{}/users/{}/roles/{}'.format(domain_id, user_id, role_id)
    return url, None


@get_by_name_or_uuid_multiple([('project', 'project_id'), ('user', 'user_id'),
                               ('role', 'role_id')])
@send('delete')
def role_unassign_for_user_on_project(project_id, user_id, role_id, **kwargs):
    url = '/projects/{}/users/{}/roles/{}'.format(project_id, user_id, role_id)
    return url, None


@get_by_name_or_uuid_multiple([('domain', 'domain_id'), ('user', 'user_id'),
                               ('role', 'role_id')])
@send('delete')
def role_unassign_for_user_on_domain(domain_id, user_id, role_id, **kwargs):
    url = '/domains/{}/users/{}/roles/{}'.format(domain_id, user_id, role_id)
    return url, None


@get_by_name_or_uuid_multiple([('project', 'project_id'), ('user', 'user_id'),
                               ('role', 'role_id')])
@send('head')
def role_assign_check_for_user_on_project(project_id, user_id, role_id,
                                          **kwargs):
    url = '/projects/{}/users/{}/roles/{}'.format(project_id, user_id, role_id)
    return url, None


@get_by_name_or_uuid_multiple([('domain', 'domain_id'), ('user', 'user_id'),
                               ('role', 'role_id')])
@send('head')
def role_assign_check_for_user_on_domain(domain_id, user_id, role_id,
                                         **kwargs):
    url = '/domains/{}/users/{}/roles/{}'.format(domain_id, user_id, role_id)
    return url, None


@get_by_name_or_uuid_multiple([('role', 'role_id')])
@send('get')
def role_get_details(role_id, **kwargs):
    url = '/roles/{}?{}'.format(role_id, urlencode(kwargs))
    return url, None


@get_by_name_or_uuid_multiple([('role', 'role_id')])
@send('patch')
def role_update(role_id, **kwargs):
    url = '/roles/{}'.format(role_id)
    json = {
        'role': kwargs,
    }
    return url, json


@get_by_name_or_uuid_multiple([('role', 'role_id')])
@send('delete')
def role_delete(role_id, **kwargs):
    url = '/roles/{}'.format(role_id)
    return url, None


@send('post')
def role_create(**kwargs):
    url = '/roles'
    json = {
        'role': kwargs,
    }
    return url, json


@get_by_name_or_uuid_multiple([('role', 'prior_role_id')])
@send('get')
def role_inference_rule_for_role_list(prior_role_id, **kwargs):
    url = '/roles/{}/implies'.format(prior_role_id)
    return url, None


@get_by_name_or_uuid_multiple([('role', 'prior_role_id'),
                               ('role', 'implies_role_id')])
@send('put')
def role_inference_rule_create(prior_role_id, implies_role_id, **kwargs):
    url = '/roles/{}/implies/{}'.format(prior_role_id, implies_role_id)
    return url, None


@get_by_name_or_uuid_multiple([('role', 'prior_role_id'),
                               ('role', 'implies_role_id')])
@send('get')
def role_inference_rule_get(prior_role_id, implies_role_id, **kwargs):
    url = '/roles/{}/implies/{}'.format(prior_role_id, implies_role_id)
    return url, None


@get_by_name_or_uuid_multiple([('role', 'prior_role_id'),
                               ('role', 'implies_role_id')])
@send('head')
def role_inference_rule_confirm(prior_role_id, implies_role_id, **kwargs):
    url = '/roles/{}/implies/{}'.format(prior_role_id, implies_role_id)
    return url, None


@get_by_name_or_uuid_multiple([('role', 'prior_role_id'),
                               ('role', 'implies_role_id')])
@send('delete')
def role_inference_rule_delete(prior_role_id, implies_role_id, **kwargs):
    url = '/roles/{}/implies/{}'.format(prior_role_id, implies_role_id)
    return url, None

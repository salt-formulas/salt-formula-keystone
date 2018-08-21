import logging


def __virtual__():
    return 'keystonev3' if 'keystonev3.endpoint_list' in __salt__ else False  # noqa


log = logging.getLogger(__name__)


def _keystonev3_call(fname, *args, **kwargs):
    return __salt__['keystonev3.{}'.format(fname)](*args, **kwargs)  # noqa


def endpoint_present(name, url, interface, service_id, cloud_name, **kwargs):

    service_id = _keystonev3_call(
        'service_get_details', service_id,
        cloud_name=cloud_name)['service']['id']

    endpoints = _keystonev3_call(
        'endpoint_list', name=name, service_id=service_id, interface=interface,
        cloud_name=cloud_name)['endpoints']

    if not endpoints:
        try:
            resp = _keystonev3_call(
                'endpoint_create', url=url, interface=interface,
                service_id=service_id, cloud_name=cloud_name, **kwargs
            )
        except Exception as e:
            log.error('Keystone endpoint create failed with {}'.format(e))
            return _create_failed(name, 'endpoint')
        return _created(name, 'endpoint', resp)
    elif len(endpoints) == 1:
        exact_endpoint = endpoints[0]
        endpoint_id = exact_endpoint['id']
        changable = (
            'url', 'region', 'interface', 'service_id'
        )
        to_update = {}
        to_check = {'url': url}
        to_check.update(kwargs)

        for key in to_check:
            if (key in changable and (key not in exact_endpoint or
                                      to_check[key] != exact_endpoint[key])):
                to_update[key] = to_check[key]
        if to_update:
            try:
                resp = _keystonev3_call(
                    'endpoint_update', endpoint_id=endpoint_id,
                    cloud_name=cloud_name, **to_update
                )
            except Exception as e:
                log.error('Keystone endpoint update failed with {}'.format(e))
                return _update_failed(name, 'endpoint')
            return _updated(name, 'endpoint', resp)
        else:
            return _no_changes(name, 'endpoint')
    else:
        return _find_failed(name, 'endpoint')


def endpoint_absent(name, service_id, interface, cloud_name):
    service_id = _keystonev3_call(
        'service_get_details', service_id,
        cloud_name=cloud_name)['service']['id']

    endpoints = _keystonev3_call(
        'endpoint_list', name=name, service_id=service_id, interface=interface,
        cloud_name=cloud_name)['endpoints']
    if not endpoints:
        return _absent(name, 'endpoint')
    elif len(endpoints) == 1:
        try:
            _keystonev3_call(
                'endpoint_delete', endpoints[0]['id'], cloud_name=cloud_name
            )
        except Exception as e:
            log.error('Keystone delete endpoint failed with {}'.format(e))
            return _delete_failed(name, 'endpoint')
        return _deleted(name, 'endpoint')
    else:
        return _find_failed(name, 'endpoint')


def service_present(name, type, cloud_name, **kwargs):

    service_id = ''

    try:
        exact_service = _keystonev3_call(
            'service_get_details', name,
            cloud_name=cloud_name)['service']
        service_id = exact_service['id']
    except Exception as e:
        if 'ResourceNotFound' in repr(e):
            pass
        else:
            log.error('Failed to get service {}'.format(e))
            return _create_failed(name, 'service')

    if not service_id:
        try:
            resp = _keystonev3_call(
                'service_create', name=name, type=type,
                cloud_name=cloud_name, **kwargs
            )
        except Exception as e:
            log.error('Keystone service create failed with {}'.format(e))
            return _create_failed(name, 'service')
        return _created(name, 'service', resp)

    else:
        changable = ('type', 'enabled', 'description')
        to_update = {}
        to_check = {'type': type}
        to_check.update(kwargs)

        for key in to_check:
            if (key in changable and (key not in exact_service or
                                      to_check[key] != exact_service[key])):
                    to_update[key] = to_check[key]
        if to_update:
            try:
                resp = _keystonev3_call(
                    'service_update', service_id=service_id,
                    cloud_name=cloud_name, **to_update
                )
            except Exception as e:
                log.error('Keystone service update failed with {}'.format(e))
                return _update_failed(name, 'service')
            return _updated(name, 'service', resp)
        else:
            return _no_changes(name, 'service')
    return _find_failed(name, 'service')


def service_absent(name, cloud_name):
    try:
        _keystonev3_call(
            'service_get_details', name,
            cloud_name=cloud_name)['service']
    except Exception as e:
        if 'ResourceNotFound' in repr(e):
            return _absent(name, 'service')
        else:
            log.error('Failed to get service {}'.format(e))
            return _find_failed(name, 'service')
    try:
        _keystonev3_call('service_delete', name, cloud_name=cloud_name)
    except Exception:
        return _delete_failed(name, 'service')
    return _deleted(name, 'service')



def project_present(name, domain_id, cloud_name, **kwargs):

    projects = _keystonev3_call(
        'project_list', name=name, domain_id=domain_id, cloud_name=cloud_name
    )['projects']

    if not projects:
        try:
            resp = _keystonev3_call(
                'project_create', domain_id=domain_id, name=name,
                cloud_name=cloud_name, **kwargs
            )
        except Exception as e:
            log.error('Keystone project create failed with {}'.format(e))
            return _create_failed(name, 'project')
        return _created(name, 'project', resp)
    elif len(projects) == 1:
        exact_project = projects[0]
        project_id = exact_project['id']
        changable = (
            'is_domain', 'description', 'domain_id', 'enabled',
            'parent_id', 'tags'
        )
        to_update = {}

        for key in kwargs:
            if (key in changable and (key not in exact_project or
                                      kwargs[key] != exact_project[key])):
                    to_update[key] = kwargs[key]

        if to_update:
            try:
                resp = _keystonev3_call(
                    'project_update', project_id=project_id,
                    cloud_name=cloud_name, **to_update
                )
            except Exception as e:
                log.error('Keystone project update failed with {}'.format(e))
                return _update_failed(name, 'project')
            return _updated(name, 'project', resp)
        else:
            return _no_changes(name, 'project')
    else:
        return _find_failed(name, 'project')


def project_absent(name, cloud_name):
    try:
        _keystonev3_call('project_get_details',
                         project_id=name, cloud_name=cloud_name)
    except Exception as e:
        if 'ResourceNotFound' in repr(e):
            return _absent(name, 'project')
        else:
            log.error('Failed to get project {}'.format(e))
            return _find_failed(name, 'project')
    try:
        _keystonev3_call('project_delete', project_id=name,
                         cloud_name=cloud_name)
    except Exception:
        return _delete_failed(name, 'project')
    return _deleted(name, 'project')


def user_present(name, cloud_name, password_reset=False, **kwargs):

    users = _keystonev3_call(
        'user_list', name=name, cloud_name=cloud_name
    )['users']

    if 'default_project_id' in kwargs:
        kwargs['default_project_id'] = _keystonev3_call(
             'project_get_details', kwargs['default_project_id'],
             cloud_name=cloud_name)['project']['id']

    if not users:
        try:
            resp = _keystonev3_call(
                'user_create', name=name, cloud_name=cloud_name, **kwargs
            )
        except Exception as e:
            log.error('Keystone user create failed with {}'.format(e))
            return _create_failed(name, 'user')
        return _created(name, 'user', resp)

    elif len(users) == 1:
        exact_user = users[0]
        user_id = exact_user['id']
        changable = (
            'default_project_id', 'domain_id', 'enabled', 'email'
        )
        if password_reset:
            changable += ('password',)
        to_update = {}

        for key in kwargs:
            if (key in changable and (key not in exact_user or
                                      kwargs[key] != exact_user[key])):
                    to_update[key] = kwargs[key]

        if to_update:
            log.info('Updating keystone user {} with: {}'.format(user_id,
                                                                 to_update))
            try:
                resp = _keystonev3_call(
                    'user_update', user_id=user_id,
                    cloud_name=cloud_name, **to_update
                )
            except Exception as e:
                log.error('Keystone user update failed with {}'.format(e))
                return _update_failed(name, 'user')
            return _updated(name, 'user', resp)
        else:
            return _no_changes(name, 'user')
    else:
        return _find_failed(name, 'user')


def user_absent(name, cloud_name):
    try:
        _keystonev3_call('user_get_details', user_id=name,
                         cloud_name=cloud_name)
    except Exception as e:
        if 'ResourceNotFound' in repr(e):
            return _absent(name, 'user')
        else:
            log.error('Failed to get user {}'.format(e))
            return _find_failed(name, 'user')
    try:
        _keystonev3_call('user_delete', user_id=name, cloud_name=cloud_name)
    except Exception:
        return _delete_failed(name, 'user')
    return _deleted(name, 'user')


def user_role_assigned(name, role_id, cloud_name, project_id=None,
                       domain_id=None, role_domain_id=None, **kwargs):

    user_id = _keystonev3_call(
              'user_get_details', name,
              cloud_name=cloud_name)['user']['id']

    if project_id:
        project_id = _keystonev3_call(
                 'project_get_details', project_id,
                 cloud_name=cloud_name)['project']['id']

    if domain_id:
        domain_id  = _keystonev3_call(
            'domain_get_details', domain_id,
            cloud_name=cloud_name)['domain']['id']


    if (project_id and domain_id) or (not project_id and not domain_id):
        return {
            'name': name,
            'changes': {},
            'result': False,
            'comment': 'Use project_id or domain_id (only one of them)'
        }


    if role_domain_id:
        role_domain_id  = _keystonev3_call(
            'domain_get_details', role_domain_id,
            cloud_name=cloud_name)['domain']['id']

    if role_id:
        role_id = _keystonev3_call(
            'role_get_details', role_id, domain_id=role_domain_id,
            cloud_name=cloud_name)['role']['id']

    req_kwargs = {'role.id': role_id, 'user.id': user_id,
                  'cloud_name': cloud_name}
    if domain_id:
        req_kwargs['domain_id'] = domain_id
    if project_id:
        req_kwargs['project_id'] = project_id

    role_assignments = _keystonev3_call(
                 'role_assignment_list', **req_kwargs)['role_assignments']

    req_kwargs = {'cloud_name': cloud_name, 'user_id': user_id,
                  'role_id': role_id}
    if domain_id:
        req_kwargs['domain_id'] = domain_id
    if project_id:
        req_kwargs['project_id'] = project_id

    if not role_assignments:
        method_type = 'project' if project_id else 'domain'
        method = 'role_assign_for_user_on_{}'.format(method_type)
        try:
            resp = _keystonev3_call(method, **req_kwargs)
        except Exception as e:
            log.error('Keystone user role assignment with {}'.format(e))
            return _create_failed(name, 'user_role_assignment')
        # We check for exact assignment when did role_assignment_list
        # on this stage we already just assigned role if it was missed.
        return _created(name, 'user_role_assignment', resp)
    return _no_changes(name, 'user_role_assignment')


def user_role_unassign(name, role_id, cloud_name, project_id=None,
                       domain_id=None, role_domain_id=None):
    user_id = _keystonev3_call(
        'user_get_details', name,
        cloud_name=cloud_name)['user']['id']

    if project_id:
        project_id = _keystonev3_call(
            'project_get_details', project_id,
            cloud_name=cloud_name)['project']['id']

    if domain_id:
        domain_id = _keystonev3_call(
            'domain_get_details', domain_id,
            cloud_name=cloud_name)['domain']['id']

    if (project_id and domain_id) or (not project_id and not domain_id):
        return {
            'name': name,
            'changes': {},
            'result': False,
            'comment': 'Use project_id or domain_id (only one of them)'
        }

    if role_domain_id:
        role_domain_id = _keystonev3_call(
            'domain_get_details', role_domain_id,
            cloud_name=cloud_name)['domain']['id']

    if role_id:
        role_id = _keystonev3_call(
            'role_get_details', role_id, domain_id=role_domain_id,
            cloud_name=cloud_name)['role']['id']

    req_kwargs = {'role.id': role_id, 'user.id': user_id,
                  'cloud_name': cloud_name}
    if domain_id:
        req_kwargs['domain_id'] = domain_id
    if project_id:
        req_kwargs['project_id'] = project_id

    role_assignments = _keystonev3_call(
        'role_assignment_list', **req_kwargs)['role_assignments']

    req_kwargs = {'cloud_name': cloud_name, 'user_id': user_id,
                  'role_id': role_id}
    if domain_id:
        req_kwargs['domain_id'] = domain_id
    if project_id:
        req_kwargs['project_id'] = project_id

    if not role_assignments:
        return _absent(name, 'user_role_assignment')
    else:
        method_type = 'project' if project_id else 'domain'
        method = 'role_unassign_for_user_on_{}'.format(method_type)
        try:
            _keystonev3_call(method, **req_kwargs)
        except Exception:
            return _delete_failed(name, 'user_role_assignment')
    return _deleted(name, 'user_role_assignment')


def role_present(name, cloud_name, **kwargs):

    roles = _keystonev3_call(
        'role_list', name=name, cloud_name=cloud_name
    )['roles']

    if 'domain_id' in kwargs:
        kwargs['domain_id'] = _keystonev3_call(
            'domain_get_details', kwargs['domain_id'],
            cloud_name=cloud_name)['domains']

    if not roles:
        try:
            resp = _keystonev3_call(
                'role_create', name=name, cloud_name=cloud_name, **kwargs
            )
        except Exception as e:
            log.error('Keystone role create failed with {}'.format(e))
            return _create_failed(name, 'role')
        return _created(name, 'role', resp)
    elif len(roles) == 1:
        exact_role = roles[0]
        role_id = exact_role['id']
        changable = ('domain_id')
        to_update = {}

        for key in kwargs:
            if (key in changable and (key not in exact_role or
                                      kwargs[key] != exact_role[key])):
                to_update[key] = kwargs[key]

        if to_update:
            try:
                resp = _keystonev3_call(
                    'role_update', role_id=role_id,
                    cloud_name=cloud_name, **to_update
                )
            except Exception as e:
                log.error('Keystone role update failed with {}'.format(e))
                return _update_failed(name, 'role')
            return _updated(name, 'role', resp)
        else:
            return _no_changes(name, 'role')
    else:
        return _find_failed(name, 'role')


def role_absent(name, cloud_name):
    try:
        _keystonev3_call('role_get_details', role_id=name,
                         cloud_name=cloud_name)
    except Exception as e:
        if 'ResourceNotFound' in repr(e):
            return _absent(name, 'role')
        else:
            log.error('Failed to get role {}'.format(e))
            return _find_failed(name, 'role')
    try:
        _keystonev3_call('role_delete', role_id=name, cloud_name=cloud_name)
    except Exception:
        return _delete_failed(name, 'role')
    return _deleted(name, 'role')


def _created(name, resource, resource_definition):
    changes_dict = {
        'name': name,
        'changes': resource_definition,
        'result': True,
        'comment': '{}{} created'.format(resource, name)
    }
    return changes_dict


def _updated(name, resource, resource_definition):
    changes_dict = {
        'name': name,
        'changes': resource_definition,
        'result': True,
        'comment': '{}{} updated'.format(resource, name)
    }
    return changes_dict


def _no_changes(name, resource):
    changes_dict = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': '{}{} is in desired state'.format(resource, name)
    }
    return changes_dict


def _deleted(name, resource):
    changes_dict = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': '{}{} removed'.format(resource, name)
    }
    return changes_dict


def _absent(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} not present'.format(resource, name),
                    'result': True}
    return changes_dict


def _delete_failed(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} failed to delete'.format(resource,
                                                                 name),
                    'result': False}
    return changes_dict


def _create_failed(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} failed to create'.format(resource,
                                                                 name),
                    'result': False}
    return changes_dict


def _update_failed(name, resource):
    changes_dict = {'name': name,
                    'changes': {},
                    'comment': '{0} {1} failed to update'.format(resource,
                                                                 name),
                    'result': False}
    return changes_dict


def _find_failed(name, resource):
    changes_dict = {
        'name': name,
        'changes': {},
        'comment': '{0} {1} found multiple {0}'.format(resource, name),
        'result': False,
    }
    return changes_dict

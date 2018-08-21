import uuid
from keystonev3 import common
from keystonev3 import lists


class CheckId(object):
    def check_id(self, val):
        try:
            return str(uuid.UUID(val)).replace('-', '') == val
        except (TypeError, ValueError, AttributeError):
            return False


class DomainCheckId(CheckId):
    def check_id(self, val):
        if val == 'default':
            return True
        return super(DomainCheckId, self).check_id(val)


resource_lists = {
    'project': lists.project_list,
    'role': lists.role_list,
    'service': lists.service_list,
    'user': lists.user_list,
    'domain': lists.domain_list,
    'group': lists.group_list,
}


response_keys = {
    'project': 'projects',
    'role': 'roles',
    'service': 'services',
    'user': 'users',
    'domain': 'domains',
    'group': 'groups'
}


def get_by_name_or_uuid_multiple(resource_arg_name_pairs):
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            results = []
            args_start = 0
            for index, (resource, arg_name) in enumerate(
                    resource_arg_name_pairs):
                if arg_name in kwargs:
                    ref = kwargs.pop(arg_name, None)
                else:
                    ref = args[index]
                    args_start += 1
                cloud_name = kwargs['cloud_name']
                if resource == 'domain':
                    checker = DomainCheckId()
                else:
                    checker = CheckId()
                if checker.check_id(ref):
                    results.append(ref)
                else:
                    # Then we have name not uuid
                    resp_key = response_keys[resource]
                    resp = resource_lists[resource](
                        name=ref, cloud_name=cloud_name)[resp_key]
                    if len(resp) == 0:
                        raise common.ResourceNotFound(resp_key, ref)
                    elif len(resp) > 1:
                        raise common.MultipleResourcesFound(resp_key, ref)
                    results.append(resp[0]['id'])
                results.extend(args[args_start:])
            return func(*results, **kwargs)
        return wrapped_f
    return wrap
try:
    import os_client_config  # noqa
    from keystoneauth1 import exceptions as ka_exceptions  # noqa
    REQUIREMENTS_MET = True
except ImportError:
    REQUIREMENTS_MET = False

from keystonev3 import endpoints
from keystonev3 import roles
from keystonev3 import services
from keystonev3 import projects
from keystonev3 import users

endpoint_get_details = endpoints.endpoint_get_details
endpoint_update = endpoints.endpoint_update
endpoint_delete = endpoints.endpoint_delete
endpoint_list = endpoints.endpoint_list
endpoint_create = endpoints.endpoint_create

role_assignment_list = roles.role_assignment_list
role_assignment_check = roles.role_assignment_check
role_add = roles.role_add
role_delete = roles.role_delete
role_get_details = roles.role_get_details
role_update = roles.role_update
role_delete = roles.role_delete
role_list = roles.role_list
role_create = roles.role_create

service_get_details = services.service_get_details
service_update = services.service_update
service_delete = services.service_delete
service_list = services.service_list
service_create = services.service_create

project_get_details = projects.project_get_details
project_update = projects.project_update
project_delete = projects.project_delete
project_list = projects.project_list
project_create = projects.project_create

user_get_details = users.user_get_details
user_update = users.user_update
user_delete = users.user_delete
user_list = users.user_list
user_create = users.user_create


__all__ = (
    'endpoint_get_details',
    'endpoint_update',
    'endpoint_delete',
    'endpoint_list',
    'endpoint_create',
    'role_assignment_list',
    'role_assignment_check',
    'role_add',
    'role_delete',
    'role_get_details',
    'role_update',
    'role_delete',
    'role_list',
    'role_create',
    'service_get_details',
    'service_update',
    'service_delete',
    'service_list',
    'service_create',
    'project_get_details',
    'project_update',
    'project_delete',
    'project_list',
    'project_create',
    'user_get_details',
    'user_update',
    'user_delete',
    'user_list',
    'user_create'
)


def __virtual__():
    """Only load keystonev3 if requirements are available."""
    if REQUIREMENTS_MET:
        return 'keystonev3'
    else:
        return False, ("The keystonev3 execution module cannot be loaded: "
                       "os_client_config or keystoneauth are unavailable.")

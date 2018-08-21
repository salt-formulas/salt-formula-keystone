try:
    import os_client_config  # noqa
    from keystoneauth1 import exceptions as ka_exceptions  # noqa
    REQUIREMENTS_MET = True
except ImportError:
    REQUIREMENTS_MET = False

from keystonev3 import lists
from keystonev3 import endpoints
from keystonev3 import roles
from keystonev3 import services
from keystonev3 import projects
from keystonev3 import users
from keystonev3 import domains
from keystonev3 import regions
from keystonev3 import groups


domain_list = lists.domain_list
domain_create = domains.domain_create
domain_update = domains.domain_update
domain_get_details = domains.domain_get_details
domain_delete = domains.domain_delete

endpoint_get_details = endpoints.endpoint_get_details
endpoint_update = endpoints.endpoint_update
endpoint_delete = endpoints.endpoint_delete
endpoint_list = lists.endpoint_list
endpoint_create = endpoints.endpoint_create

role_assignment_list = lists.role_assignment_list
role_assign_for_user_on_project = roles.role_assign_for_user_on_project
role_assign_for_user_on_domain = roles.role_assign_for_user_on_domain
role_unassign_for_user_on_project = roles.role_unassign_for_user_on_project
role_unassign_for_user_on_domain = roles.role_unassign_for_user_on_domain
role_assign_check_for_user_on_project = roles.\
    role_assign_check_for_user_on_project
role_assign_check_for_user_on_domain = roles.\
    role_assign_check_for_user_on_domain
role_get_details = roles.role_get_details
role_update = roles.role_update
role_list = lists.role_list
role_create = roles.role_create
role_delete = roles.role_delete

role_inference_rule_list = lists.role_inference_rule_list
role_inference_rule_for_role_list = roles.role_inference_rule_for_role_list
role_inference_rule_create = roles.role_inference_rule_create
role_inference_rule_get = roles.role_inference_rule_get
role_inference_rule_confirm = roles.role_inference_rule_confirm
role_inference_rule_delete = roles.role_inference_rule_delete


service_get_details = services.service_get_details
service_update = services.service_update
service_delete = services.service_delete
service_list = lists.service_list
service_create = services.service_create

project_get_details = projects.project_get_details
project_update = projects.project_update
project_delete = projects.project_delete
project_list = lists.project_list
project_create = projects.project_create

user_get_details = users.user_get_details
user_update = users.user_update
user_delete = users.user_delete
user_list = lists.user_list
user_create = users.user_create


region_list = lists.region_list
region_create = regions.region_create
region_get_details = regions.region_get_details
region_update = regions.region_update
region_delete = regions.region_delete

group_list = lists.group_list
group_create = groups.group_create
group_get_details = groups.group_get_details
group_update = groups.group_update
group_delete = groups.group_delete
group_user_list = groups.group_user_list
group_user_add = groups.group_user_add
group_user_check = groups.group_user_check
group_user_remove = groups.group_user_remove


__all__ = (
    'domain_list',
    'domain_create',
    'domain_get_details',
    'domain_update',
    'domain_delete',
    'endpoint_get_details',
    'endpoint_update',
    'endpoint_delete',
    'endpoint_list',
    'endpoint_create',
    'role_assignment_list',
    'role_assign_for_user_on_project',
    'role_assign_for_user_on_domain',
    'role_assign_check_for_user_on_domain',
    'role_assign_check_for_user_on_project',
    'role_unassign_for_user_on_domain',
    'role_unassign_for_user_on_project',
    'role_get_details',
    'role_update',
    'role_delete',
    'role_list',
    'role_create',
    'role_inference_rule_confirm',
    'role_inference_rule_create',
    'role_inference_rule_delete',
    'role_inference_rule_for_role_list',
    'role_inference_rule_get',
    'role_inference_rule_list',
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
    'user_create',
    'region_create',
    'region_delete',
    'region_get_details',
    'region_list',
    'region_update',
    'group_list',
    'group_create',
    'group_delete',
    'group_get_details',
    'group_update',
    'group_user_add',
    'group_user_check',
    'group_user_list',
    'group_user_remove',
)


def __virtual__():
    """Only load keystonev3 if requirements are available."""
    if REQUIREMENTS_MET:
        return 'keystonev3'
    else:
        return False, ("The keystonev3 execution module cannot be loaded: "
                       "os_client_config or keystoneauth are unavailable.")

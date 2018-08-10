from keystonev3.common import send

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


@send('get')
def project_list(**kwargs):
    url = '/projects?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def domain_list(**kwargs):
    url = '/domains?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def endpoint_list(**kwargs):
    url = '/endpoints?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def service_list(**kwargs):
    url = '/services?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def user_list(**kwargs):
    url = '/users?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def role_list(**kwargs):
    url = '/roles?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def role_assignment_list(**kwargs):
    url = '/role_assignments?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def role_inference_rule_list(**kwargs):
    url = '/role_inferences'
    return url, None


@send('get')
def region_list(**kwargs):
    url = '/regions?{}'.format(urlencode(kwargs))
    return url, None


@send('get')
def group_list(**kwargs):
    url = '/groups?{}'.format(urlencode(kwargs))
    return url, None
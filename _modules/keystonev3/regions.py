from keystonev3.common import send


@send('get')
def region_get_details(region_id, **kwargs):
    url = '/regions/{}'.format(region_id)
    return url, None


@send('patch')
def region_update(region_id, **kwargs):
    url = '/regions/{}'.format(region_id)
    json = {
        'region': kwargs
    }
    return url, json


@send('delete')
def region_delete(region_id, **kwargs):
    url = '/regions/{}'.format(region_id)
    return url, None


@send('post')
def region_create(**kwargs):
    url = '/regions'
    json = {
        'region': kwargs
    }
    return url, json
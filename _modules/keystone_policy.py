import io
import json
import logging

LOG = logging.getLogger(__name__)

import yaml
import yaml.constructor

try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    from ordereddict import OrderedDict

# https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


def __virtual__():
    return True


def rule_list(path, **kwargs):
    try:
        with io.open(path, 'r') as file_handle:
            rules = yaml.load(file_handle, OrderedDictYAMLLoader) or OrderedDict()
    except Exception as e:
        msg = "Unable to load policy file %s: %s" % (path, repr(e))
        LOG.debug(msg)
        rules = {'Error': msg}
    return rules


def rule_delete(name, path, **kwargs):
    ret = {}
    rules = __salt__['keystone_policy.rule_list'](path, **kwargs)
    if 'Error' not in rules:
        if name not in rules:
            return ret
        del rules[name]
        try:
            with io.open(path, 'w') as file_handle:
                if path.endswith('json'):
                    serialized = json.dumps(rules, indent=4)
                else:
                    serialized = yaml.safe_dump(rules, indent=4)
                file_handle.write(unicode(serialized))
        except Exception as e:
            msg = "Unable to save policy file: %s" % repr(e)
            LOG.error(msg)
            return {'Error': msg}
        ret = 'Rule {0} deleted'.format(name)
    return ret


def rule_set(name, rule, path, **kwargs):
    rules = __salt__['keystone_policy.rule_list'](path, **kwargs)
    if 'Error' not in rules:
        if name in rules and rules[name] == rule:
            return {name: 'Rule %s already exists and is in correct state' % name}
        rules.update({name: rule})
        try:
            with io.open(path, 'w') as file_handle:
                if path.endswith('json'):
                    serialized = json.dumps(rules, indent=4)
                else:
                    serialized = yaml.safe_dump(rules, indent=4)
                file_handle.write(unicode(serialized))
        except Exception as e:
            msg = "Unable to save policy file %s: %s" % (path, repr(e))
            LOG.error(msg)
            return {'Error': msg}
        return rule_get(name, path, **kwargs)
    return rules


def rule_get(name, path, **kwargs):
    ret = {}
    rules = __salt__['keystone_policy.rule_list'](path, **kwargs)
    if 'Error' in rules:
        ret['Error'] = rules['Error']
    elif name in rules:
        ret[name] = rules.get(name)

    return ret


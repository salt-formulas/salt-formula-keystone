#!/usr/bin/env python
'''
Management of policy.json
=========================

Merge user defined hash to policy.json
--------------------------------------

.. code-block:: yaml

  my_rule_present:
    keystone_policy.rule_present:
      - name: rule_name
      - rule: rule
      - path: /etc/keystone/policy.json

  my_rule_absent:
    keystone_policy.rule_absent:
      - name: rule_name
      - path: /etc/keystone/policy.json

'''
import logging

log = logging.getLogger(__name__)


def __virtual__():
    return True


def rule_present(name, rule, path, **kwargs):
    '''
    Ensures that the policy rule exists

    :param name: Rule name
    :param rule: Rule
    :param path: Path to policy file
    '''
    rule = rule or ""
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Rule "{0}" already exists and is in correct state'.format(name)}
    rule_check = __salt__['keystone_policy.rule_get'](name, path, **kwargs)
    if not rule_check:
        if __opts__.get('test'):
            ret['result'] = None
            ret['comment'] = 'Rule {0} will be created'.format(name)
        else:
            __salt__['keystone_policy.rule_set'](name, rule, path, **kwargs)
            ret['comment'] = 'Rule {0} has been created'.format(name)
            ret['changes']['Rule'] = 'Rule %s: "%s" has been created' % (name, rule)
    elif 'Error' in rule_check:
        ret['comment'] = rule_check.get('Error')
        ret['result'] = False
    elif rule_check[name] != rule:
        if __opts__.get('test'):
            ret['result'] = None
            ret['comment'] = 'Rule %s will be changed' % (name,)
        else:
            __salt__['keystone_policy.rule_set'](name, rule, path, **kwargs)
            ret['comment'] = 'Rule %s has been changed' % (name,)
            ret['changes']['Old Rule'] = '%s: "%s"' % (name, rule_check[name])
            ret['changes']['New Rule'] = '%s: "%s"' % (name, rule)
    return ret


def rule_absent(name, path, **kwargs):
    '''
    Ensures that the policy rule does not exist

    :param name: Rule name
    :param path: Path to policy file
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Rule "{0}" is already absent'.format(name)}
    rule_check = __salt__['keystone_policy.rule_get'](name, path, **kwargs)
    if rule_check:
        if __opts__.get('test'):
            ret['result'] = None
            ret['comment'] = 'Rule {0} will be deleted'.format(name)
        else
            __salt__['keystone_policy.rule_delete'](name, path, **kwargs)
            ret['comment'] = 'Rule {0} has been deleted'.format(name)
            ret['changes']['Rule'] = 'Rule %s: "%s" has been deleted' % (name, rule_check[name])
    elif 'Error' in rule_check:
        ret['comment'] = rule_check.get('Error')
        ret['result'] = False
    return ret


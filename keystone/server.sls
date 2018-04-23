{%- from "keystone/map.jinja" import server with context %}
{%- if server.enabled %}

keystone_packages:
  pkg.installed:
  - names: {{ server.pkgs }}

{%- set ldap = {'enabled': False} %}
{%- if server.get('backend') == 'ldap' %}
  {%- do ldap.update({'enabled': True}) %}
{%- else %}
  {%- for domain in server.get('domain', {}).itervalues() %}
    {%- if domain.get('ldap') %}
      {%- do ldap.update({'enabled': True}) %}
    {%- endif %}
  {%- endfor %}
{%- endif %}

{%- if ldap.enabled %}
keystone_ldap_packages:
  pkg.installed:
  - names:
    - python-ldap
    - python-ldappool
{% endif %}

{%- if server.service_name in ['apache2', 'httpd'] %}
{%- set keystone_service = 'apache_service' %}

purge_not_needed_configs:
  file.absent:
    - names: ['/etc/apache2/sites-enabled/keystone.conf', '/etc/apache2/sites-enabled/wsgi-keystone.conf']
    - watch_in:
      - service: {{ keystone_service }}

include:
- apache

{%- if grains.os_family == "Debian" %}
keystone:
{%- endif %}
{%- if grains.os_family == "RedHat" %}
openstack-keystone:
{%- endif %}
  service.dead:
    - enable: False
    - watch:
      - pkg: keystone_packages

{%- else %}

{%- set keystone_service = 'keystone_service' %}

{%- endif %}

{%- if not salt['user.info']('keystone') %}

keystone_user:
  user.present:
    - name: keystone
    - home: /var/lib/keystone
    - uid: 301
    - gid: 301
    - shell: /bin/false
    - system: True
    - require_in:
      - pkg: keystone_packages

keystone_group:
  group.present:
    - name: keystone
    - gid: 301
    - system: True
    - require_in:
      - pkg: keystone_packages
      - user: keystone_user

{%- endif %}

/etc/keystone/keystone.conf:
  file.managed:
  - source: salt://keystone/files/{{ server.version }}/keystone.conf.{{ grains.os_family }}
  - template: jinja
  - require:
    - pkg: keystone_packages
  - watch_in:
    - service: {{ keystone_service }}

{% if server.federation is defined %}

/etc/keystone/sso_callback_template.html:
  file.managed:
  - source: salt://keystone/files/sso_callback_template.html
  - require:
    - pkg: keystone_packages
  - watch_in:
    - service: {{ keystone_service }}

{%- endif %}

/etc/keystone/keystone-paste.ini:
  file.managed:
  - source: salt://keystone/files/{{ server.version }}/keystone-paste.ini.{{ grains.os_family }}
  - user: keystone
  - group: keystone
  - template: jinja
  - require:
    - pkg: keystone_packages
  - watch_in:
    - service: {{ keystone_service }}

{%- if server.logging.log_appender %}

{%- if server.logging.log_handlers.get('fluentd', {}).get('enabled', False) %}
keystone_fluentd_logger_package:
  pkg.installed:
    - name: python-fluent-logger
{%- endif %}

/etc/keystone/logging.conf:
  file.managed:
    - user: keystone
    - group: keystone
    - source: salt://keystone/files/logging.conf
    - template: jinja
    - defaults:
        values: {{ server }}
    - require:
      - pkg: keystone_packages
{%- if server.logging.log_handlers.get('fluentd', {}).get('enabled', False) %}
      - pkg: keystone_fluentd_logger_package
{%- endif %}
    - watch_in:
      - service: {{ keystone_service }}

/var/log/keystone/keystone.log:
  file.managed:
    - user: keystone
    - group: keystone
    - watch_in:
      - service: {{ keystone_service }}

{%- endif %}

/etc/keystone/policy.json:
  file.managed:
  - user: keystone
  - group: keystone
  - require:
    - pkg: keystone_packages
  - watch_in:
    - service: {{ keystone_service }}

{%- for name, rule in server.get('policy', {}).items() %}

{%- if rule != None %}

rule_{{ name }}_present:
  keystone_policy.rule_present:
  - path: /etc/keystone/policy.json
  - name: {{ name }}
  - rule: {{ rule }}
  - require:
    - pkg: keystone_packages
  - watch_in:
    - service: {{ keystone_service }}

{%- else %}

rule_{{ name }}_absent:
  keystone_policy.rule_absent:
  - path: /etc/keystone/policy.json
  - name: {{ name }}
  - require:
    - pkg: keystone_packages
  - watch_in:
    - service: {{ keystone_service }}

{%- endif %}

{%- endfor %}

{%- if server.get("domain", {}) %}

/etc/keystone/domains:
  file.directory:
    - mode: 0755
    - require:
      - pkg: keystone_packages

{%- for domain_name, domain in server.domain.items() %}

/etc/keystone/domains/keystone.{{ domain_name }}.conf:
  file.managed:
    - source: salt://keystone/files/keystone.domain.conf
    - template: jinja
    - require:
      - file: /etc/keystone/domains
    - watch_in:
      - service: {{ keystone_service }}
    - defaults:
        domain_name: {{ domain_name }}

{%- if domain.get('ldap', {}).get('tls', {}).get('cacert', False) %}

keystone_domain_{{ domain_name }}_cacert:
  file.managed:
    - name: /etc/keystone/domains/{{ domain_name }}.pem
    - contents_pillar: keystone:server:domain:{{ domain_name }}:ldap:tls:cacert
    - require:
      - file: /etc/keystone/domains
    {%- if not grains.get('noservices', False) %}
    - watch_in:
      - service: {{ keystone_service }}
    {%- endif %}

{%- endif %}

{#- can't use RC file here as identity endpoint may not be present in keystone #}
{#- as we will add it later in keystone.client state. Use endpoint override here. #}
{#- will be fixed when switched to keystone bootstrap. #}
{#- TODO: move domain creation to keystone.client state. #}
keystone_domain_{{ domain_name }}:
  cmd.run:
    - name: openstack --os-identity-api-version 3
            --os-endpoint {{ server.bind.get('private_protocol', 'http') }}://{{ server.bind.private_address }}:{{ server.bind.private_port }}/v3
            --os-token {{ server.service_token }}
            --os-auth-type admin_token
            domain create --description "{{ domain.description }}" {{ domain_name }}
    - unless: {% if grains.get('noservices') %}/bin/true{% else %}
            openstack --os-identity-api-version 3
            --os-endpoint {{ server.bind.get('private_protocol', 'http') }}://{{ server.bind.private_address }}:{{ server.bind.private_port }}/v3
            --os-token {{ server.service_token }}
            --os-auth-type admin_token
            domain show "{{ domain_name }}"{% endif %}
    - shell: /bin/bash
    - require:
      - file: /root/keystonercv3
      - service: {{ keystone_service }}

{%- endfor %}

{%- endif %}

{%- if server.get('ldap', {}).get('tls', {}).get('cacert', False) %}

keystone_ldap_default_cacert:
  file.managed:
    - name: {{ server.ldap.tls.cacertfile }}
    - contents_pillar: keystone:server:ldap:tls:cacert
    - require:
      - pkg: keystone_packages
    - watch_in:
      - service: {{ keystone_service }}

{%- endif %}

{%- if server.service_name not in ['apache2', 'httpd'] %}
keystone_service:
  service.running:
  - name: {{ server.service_name }}
  - enable: True
  {%- if grains.get('noservices') %}
  - onlyif: /bin/false
  {%- endif %}
  - watch:
    {%- if server.notification and server.message_queue.get('ssl',{}).get('enabled', False) %}
    - file: rabbitmq_ca_keystone_server
    {%- endif %}
    - file: /etc/keystone/keystone.conf
{%- endif %}

{%- if grains.get('virtual_subtype', None) == "Docker" %}
keystone_entrypoint:
  file.managed:
  - name: /entrypoint.sh
  - template: jinja
  - source: salt://keystone/files/entrypoint.sh
  - mode: 755
{%- endif %}

/root/keystonerc:
  file.managed:
  - source: salt://keystone/files/keystonerc
  - template: jinja
  - require:
    - pkg: keystone_packages

/root/keystonercv3:
  file.managed:
  - source: salt://keystone/files/keystonercv3
  - template: jinja
  - require:
    - pkg: keystone_packages

{%- if not grains.get('noservices', False) %}
keystone_syncdb:
  cmd.run:
  - name: keystone-manage db_sync && sleep 1
  - timeout: 120
  - require:
    - service: {{ keystone_service }}
{%- endif %}

{% if server.tokens.engine == 'fernet' %}

keystone_fernet_keys:
  file.directory:
  - name: {{ server.tokens.location }}
  - mode: 750
  - user: keystone
  - group: keystone
  - require:
    - pkg: keystone_packages
  - require_in:
    - service: keystone_fernet_setup

{%- if not grains.get('noservices', False) %}
keystone_fernet_setup:
  cmd.run:
  - name: keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
  - require:
    - service: {{ keystone_service }}
    - file: keystone_fernet_keys
{%- endif %}

{% endif %}

{%- if server.version in ['newton', 'ocata', 'pike'] %}
keystone_credential_keys:
  file.directory:
  - name: {{ server.credential.location }}
  - mode: 750
  - user: keystone
  - group: keystone
  - require:
    - pkg: keystone_packages

{%- if not grains.get('noservices', False) %}
keystone_credential_setup:
  cmd.run:
  - name: keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
  - require:
    - service: {{ keystone_service }}
    - file: keystone_credential_keys
{%- endif %}
{%- endif %}

{%- if not grains.get('noservices', False) %}

{%- if not salt['pillar.get']('linux:system:repo:mirantis_openstack', False) %}

keystone_service_tenant:
  keystoneng.tenant_present:
  - name: {{ server.service_tenant }}
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - cmd: keystone_syncdb

keystone_admin_tenant:
  keystoneng.tenant_present:
  - name: {{ server.admin_tenant }}
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_service_tenant

keystone_roles:
  keystoneng.role_present:
  - names: {{ server.roles }}
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_service_tenant

{%- if not server.get('ldap', {}).get('read_only', False) %}

keystone_admin_user:
  keystoneng.user_present:
  - name: {{ server.admin_name }}
  - password: {{ server.admin_password }}
  - email: {{ server.admin_email }}
  - tenant: {{ server.admin_tenant }}
  - roles:
      {{ server.admin_tenant }}:
      - admin
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_admin_tenant
    - keystoneng: keystone_roles

{%- endif %}

{%- endif %}

{%- for service_name, service in server.get('service', {}).items() %}

keystone_{{ service_name }}_service:
  keystoneng.service_present:
  - name: {{ service_name }}
  - service_type: {{ service.type }}
  - description: {{ service.description }}
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_roles

keystone_{{ service_name }}_{{ service.get('region', 'RegionOne') }}_endpoint:
  keystoneng.endpoint_present:
  - name: {{ service.get('service', service_name) }}
  - publicurl: '{{ service.bind.get('public_protocol', 'http') }}://{{ service.bind.public_address }}:{{ service.bind.public_port }}{{ service.bind.public_path }}'
  - internalurl: '{{ service.bind.get('internal_protocol', 'http') }}://{{ service.bind.internal_address }}:{{ service.bind.internal_port }}{{ service.bind.internal_path }}'
  - adminurl: '{{ service.bind.get('admin_protocol', 'http') }}://{{ service.bind.admin_address }}:{{ service.bind.admin_port }}{{ service.bind.admin_path }}'
  - region: {{ service.get('region', 'RegionOne') }}
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_{{ service_name }}_service

{% if service.user is defined %}

keystone_user_{{ service.user.name }}:
  keystoneng.user_present:
  - name: {{ service.user.name }}
  - password: {{ service.user.password }}
  - email: {{ server.admin_email }}
  - tenant: {{ server.service_tenant }}
  - roles:
      {{ server.service_tenant }}:
      - admin
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_roles

{% endif %}

{%- endfor %}

{%- for tenant_name, tenant in server.get('tenant', {}).items() %}

keystone_tenant_{{ tenant_name }}:
  keystoneng.tenant_present:
  - name: {{ tenant_name }}
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_roles

{%- for user_name, user in tenant.get('user', {}).items() %}

keystone_user_{{ user_name }}:
  keystoneng.user_present:
  - name: {{ user_name }}
  - password: {{ user.password }}
  - email: {{ user.get('email', 'root@localhost') }}
  - tenant: {{ tenant_name }}
  - roles:
      {{ tenant_name }}:
      {%- if user.get('roles', False) %}
      {{ user.roles }}
      {%- else %}
      - Member
      {%- endif %}
  - connection_token: {{ server.service_token }}
  - connection_endpoint: 'http://{{ server.bind.address }}:{{ server.bind.private_port }}/v2.0'
  - require:
    - keystoneng: keystone_tenant_{{ tenant_name }}

{%- endfor %}

{%- endfor %}
{%- endif %} {# end noservices #}

{%- if server.database.get('ssl',{}).get('enabled',False)  %}
mysql_ca_keystone_server:
{%- if server.database.ssl.cacert is defined %}
  file.managed:
    - name: {{ server.database.ssl.cacert_file }}
    - contents_pillar: keystone:server:database:ssl:cacert
    - mode: 0444
    - makedirs: true
    - require_in:
      - file: /etc/keystone/keystone.conf
{%- else %}
  file.exists:
   - name: {{ server.database.ssl.get('cacert_file', server.cacert_file) }}
   - require_in:
     - file: /etc/keystone/keystone.conf
{% endif %}
{% endif %}


{%- if server.notification and server.message_queue.get('ssl',{}).get('enabled', False) %}
rabbitmq_ca_keystone_server:
{%- if server.message_queue.ssl.cacert is defined %}
  file.managed:
    - name: {{ server.message_queue.ssl.cacert_file }}
    - contents_pillar: keystone:server:message_queue:ssl:cacert
    - mode: 0444
    - makedirs: true
{%- else %}
  file.exists:
   - name: {{ server.message_queue.ssl.get('cacert_file', server.cacert_file) }}
{%- endif %}
{%- endif %}

{%- endif %}

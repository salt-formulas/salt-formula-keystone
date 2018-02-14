{%- from "keystone/map.jinja" import client with context %}
{%- if client.enabled %}

{%- if client.tenant is defined %}

keystone_client_roles:
  keystoneng.role_present:
  - names: {{ client.roles }}
  - connection_user: {{ client.server.user }}
  - connection_password: {{ client.server.password }}
  - connection_tenant: {{ client.server.tenant }}
  - connection_auth_url: 'http://{{ client.server.host }}:{{ client.server.public_port }}/v2.0/'

{%- for tenant_name, tenant in client.get('tenant', {}).items() %}

keystone_tenant_{{ tenant_name }}:
  keystoneng.tenant_present:
  - name: {{ tenant_name }}
  - connection_user: {{ client.server.user }}
  - connection_password: {{ client.server.password }}
  - connection_tenant: {{ client.server.tenant }}
  - connection_auth_url: 'http://{{ client.server.host }}:{{ client.server.public_port }}/v2.0/'
  - require:
    - keystoneng: keystone_client_roles

{%- for user_name, user in tenant.get('user', {}).items() %}

keystone_{{ tenant_name }}_user_{{ user_name }}:
  keystoneng.user_present:
  - name: {{ user_name }}
  - password: {{ user.password }}
  - email: {{ user.get('email', 'root@localhost') }}
  - tenant: {{ tenant_name }}
  - roles:
      "{{ tenant_name }}":
        {%- if user.get('is_admin', False) %}
        - admin
        {%- elif user.get('roles', False) %}
        {{ user.roles }}
        {%- else %}
        - Member
        {%- endif %}
  - connection_user: {{ client.server.user }}
  - connection_password: {{ client.server.password }}
  - connection_tenant: {{ client.server.tenant }}
  - connection_auth_url: 'http://{{ client.server.host }}:{{ client.server.public_port }}/v2.0/'
  - require:
    - keystoneng: keystone_tenant_{{ tenant_name }}

{%- endfor %}

{%- endfor %}

{%- endif %}

{%- endif %}

{%- from "keystone/map.jinja" import client with context %}
{%- set resources = client.get('resources', {}).get('v3', {}) %}

{%- if resources.get('enabled', False) %}

{% for role_name,role  in resources.get('roles', {}).iteritems() %}

{%- if role.enabled %}
keystone_role_{{ role_name }}:
  keystonev3.role_present:
    - cloud_name: {{ role.get('cloud_name', resources.cloud_name) }}
    {#- The role name is not uniq among domains, use name here to have ability create #}
    {#- roles with the same name in different domains #}
    - name: {{ role.name }}
    {%- if role.domain_id is defined %}
    - domain_id: {{ role.domain_id }}
    {%- endif %}
{%- else %}
keystone_role_{{ role_name }}:
  keystonev3.role_absent:
    - cloud_name: {{ role.get('cloud_name', resources.cloud_name) }}
    - name: {{ role_name }}
{%- endif %}

{%- endfor %}

{% for service_name,service  in resources.get('services', {}).iteritems() %}
keystone_service_{{ service_name }}_{{ service.type }}:
  keystonev3.service_present:
    - cloud_name: {{ service.get('cloud_name', resources.cloud_name) }}
    - name: {{ service_name }}
    - type: {{ service.type }}
    {%- if service.description is defined %}
    - description: {{ service.description }}
    {%- endif %}
    {%- if service.enabled is defined %}
    - enabled: {{ service.enabled }}
    {%- endif %}

    {% for endpoint_name, endpoint  in service.get('endpoints', {}).iteritems() %}

keystone_endpoint_{{ endpoint_name }}_{{ endpoint.interface }}_{{ endpoint.region }}:
  keystonev3.endpoint_present:
  - name: {{ endpoint_name }}
  - cloud_name: {{ endpoint.get('cloud_name', resources.cloud_name) }}
  - url: {{ endpoint.url }}
  - interface: {{ endpoint.interface }}
  - service_id: {{ service_name }}
  - region: {{ endpoint.region }}
  - require:
    - keystone_service_{{ service_name }}_{{ service.type }}

    {%- endfor %}
{% endfor %}

{% for domain_name, domain  in resources.get('domains', {}).iteritems() %}

{#- TODO: Add domain support #}
    {%- for project_name, project in domain.get('projects', {}).iteritems() %}
keystone_project_{{ project_name }}:
  keystonev3.project_present:
  - cloud_name: {{ project.get('cloud_name', resources.cloud_name) }}
  - name: {{ project_name }}
  {%- if project.is_domain is defined %}
  - is_domain: {{ project.is_domain }}
  {%- endif %}
  {%- if project.description is defined %}
  - description: {{ project.description }}
  {%- endif %}
{# TODO unkomment when domain support is added. #}
{#  {- if project.domain_id is defined %} #}
{#  - domain_id: {{ project.domain_id }} #}
{#  {%- endif %} #}
  {%- if project.enabled is defined %}
  - enabled: {{ project.enabled }}
  {%- endif %}
  {%- if project.parent_id is defined %}
  - parent_id: {{ project.parent_id }}
  {%- endif %}
  {%- if project.tags is defined %}
  - tags: {{ project.tags }}
  {%- endif %}

    {%- endfor %}

{%- endfor %}

{%- for user_name, user in resources.get('users', {}).iteritems() %}

keystone_user_{{ user_name }}:
  keystonev3.user_present:
  - cloud_name: {{ user.get('cloud_name', resources.cloud_name) }}
  - name: {{ user_name }}
  {%- if user.default_project_id is defined %}
  - default_project_id: {{ user.default_project_id }}
  {%- endif %}
  {%- if user.domain_id is defined %}
  - domain_id: {{ user.domain_id }}
  {%- endif %}
  {%- if user.enabled is defined %}
  - enabled: {{ user.enabled }}
  {%- endif %}
  {%- if user.password is defined %}
  - password: {{ user.password }}
  {%- endif %}
  {%- if user.email is defined %}
  - email: {{ user.email }}
  {%- endif %}
  {%- if user.password_reset is defined %}
  - password_reset: {{ user.password_reset }}
  {%- endif %}

    {%- for role_name,role in user.get('roles', {}).iteritems() %}
keystone_user_{{ user_name }}_role_{{ role.name }}_assigned:
  keystonev3.user_role_assigned:
    - name: {{ user_name }}
    - role_id: {{ role.name }}
    - cloud_name: {{ user.get('cloud_name', resources.cloud_name) }}
    {%- if role.domain_id is defined %}
    - domain_id: {{ role.domain_id }}
    {%- endif %}
    {%- if role.project_id is defined %}
    - project_id: {{ role.project_id }}
    {%- endif %}
    {%- if role.role_domain_id is defined %}
    - role_domain_id: {{ role.role_domain_id }}
    {%- endif %}
    {%- endfor %}

{%- endfor %}

{%- endif %}

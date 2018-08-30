{%- from "keystone/map.jinja" import client with context %}
{%- if client.enabled and client.get('os_client_config', {}).get('enabled', False)  %}

keystone_os_client_config_packages:
  pkg.installed:
  - names: {{ client.os_client_config.pkgs }}

{%- for conf_name, config in client.get('os_client_config', {}).get('cfgs', {}).items() %}

keystone_os_client_config_{{ conf_name }}:
  file.managed:
    - name: {{ config.get('file', '/root/.config/openstack/clouds.yml') }}
    - contents: |
        {{ client.os_client_config.cfgs.get(conf_name).content |yaml(False)|indent(8) }}
    - user: {{ config.get('user', 'root') }}
    - group: {{ config.get('group', 'root') }}
    - makedirs: True

{%- endfor %}

{%- endif %}

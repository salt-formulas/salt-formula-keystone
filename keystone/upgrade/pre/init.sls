{%- from "keystone/map.jinja" import server,client with context %}

keystone_pre:
  test.show_notification:
    - text: "Running keystone.upgrade.pre"

{%- if server.enabled %}

keystone_doctor:
  cmd.run:
    - name: keystone-manage doctor
  {%- if grains.get('noservices') or server.get('role', 'primary') == 'secondary' %}
    - onlyif: /bin/false
  {%- endif %}
{%- endif %}

{%- if client.get('os_client_config', {}).get('enabled') %}
keystone_send_os_client_config:
  module.run:
    - name: mine.send
    - func: keystone_os_client_config
    - kwargs:
        mine_function: pillar.get
    - args:
      - 'keystone:client:os_client_config:cfgs:root:content'
{%- else %}
  {%- set os_content = salt['mine.get']('I@keystone:client:os_client_config:enabled:true', 'keystone_os_client_config', 'compound').values()[0] %}
keystone_os_client_config:
  file.managed:
    - name: /etc/openstack/clouds.yml
    - contents: |
        {{ os_content |yaml(False)|indent(8) }}
    - user: 'root'
    - group: 'root'
    - makedirs: True
    - unless: /etc/openstack/clouds.yml
{%- endif %}

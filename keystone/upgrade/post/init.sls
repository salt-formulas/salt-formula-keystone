{%- from "keystone/map.jinja" import server,client with context %}

keystone_post:
  test.show_notification:
    - text: "Running keystone.upgrade.post"

{%- if server.enabled %}

keystone_doctor:
  cmd.run:
    - name: keystone-manage doctor
  {%- if grains.get('noservices') or server.get('role', 'primary') == 'secondary' %}
    - onlyif: /bin/false
  {%- endif %}
{%- endif %}

{%- if client.get('os_client_config', {}).get('enabled') %}
keystone_delete_os_client_config:
  module.run:
    - name: mine.delete
    - m_fun: keystone_os_client_config
{%- else %}
keystone_os_client_config_absent:
  file.absent:
    - name: /etc/openstack/clouds.yml
{%- endif %}

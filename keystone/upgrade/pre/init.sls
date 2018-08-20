{%- from "keystone/map.jinja" import server with context %}

keystone_pre:
  test.show_notification:
    - text: "Running keystone.upgrade.pre"

include:
 - keystone.upgrade.verify.api

{%- if server.enabled %}

keystone_doctor:
  cmd.run:
    - name: keystone-manage doctor
  {%- if grains.get('noservices') or server.get('role', 'primary') == 'secondary' %}
    - onlyif: /bin/false
  {%- endif %}
{%- endif %}
